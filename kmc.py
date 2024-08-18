import sys
if len(sys.argv) != 2:
    print("usage kmc.py <strucutre files in xyz, with reaction sites marked by ar>")
    exit(1)

f_str = sys.argv[1]

import random
import numpy as np
from ase.io import read, write
from visit_all_bonds_and_sites import get_ar_bonds, get_ar_sites
from build_event_dic import build_event_dic
from mapping import adbname_to_numindex, numindex_to_adbname
from file_operation import mkdir

from regroup_rate_list import regroup_rate_list

class KMC:
    def __init__(self, f_str):
        """
        Initialize the KMC simulation.

        :param rates: Dictionary of reaction rates. Keys are reaction names, values are rates.
        """
        #self.rates = rates
        self.time = 0.0
        self.step = 0
        self.prefix = ".".join(f_str.split(".")[:-1])
        #self.total_rate = sum(rates.values())
        
        self.atoms = read(f_str)
        self.sites = get_ar_sites(f_str)
        self.bonds = get_ar_bonds(f_str)
        self.event_dic = build_event_dic()
        
        self.build_event_list()

        


    def build_event_list(self):
        '''
        build event list for each site and each bond
        '''
 
        self.K_list = []

        for site in self.sites:
            # format of site: array, n*1, indicates n sites

            atm_id = site
            prefix = str(atm_id)
            #print("site = ", site)
            property = "site"

            site_pair = [str(self.atoms.get_tags()[atm_id])]  # site_pair is the site name 
            adb_pair  = [numindex_to_adbname(self.atoms[atm_id].charge)] # adb_pair is the site adb, written in  

            

            site_K_list = self.extract_matching_events(self.event_dic, property, site_pair, adb_pair, prefix) #generate k_event from event_dic

            self.K_list = np.append(self.K_list, site_K_list)
           

       
        for bond in self.bonds:
            # format of bond: array, n*2, indicates n bonds

            atm_id = int(bond[0])
            atm_jd = int(bond[1])
            prefix = str(atm_id)+'-'+str(atm_jd)

            #print("bond = ", bond)
            property = "bond"

            site_pair = [str(self.atoms.get_tags()[atm_id]),   str(self.atoms.get_tags()[atm_jd])] # site_pair is the site name 
            adb_pair  = [numindex_to_adbname(self.atoms[atm_id].charge), numindex_to_adbname(self.atoms[atm_jd].charge)] # adb_pair is the site adb, written in   

            bond_K_list = self.extract_matching_events(self.event_dic, property, site_pair, adb_pair,prefix)

            self.K_list = np.append(self.K_list, bond_K_list)
       



    def select_event(self, K_list):
        """
        Select an event based on the rates.

        :return: Selected event
        """
        RT = 0.025875
        

        Ea_list =  [item['k'] for item in K_list]
        
        rate_list = [np.exp(-Ea/RT) for Ea in Ea_list]
        rate_list = np.array(rate_list)
        regroup_rate_list(rate_list,K_list, self.step)

        self.total_rate = sum(rate_list)

        

        r = random.uniform(0, self.total_rate)
        cumulative_rate = 0.0
        for index, rate in enumerate(rate_list):
            cumulative_rate += rate
            if r <= cumulative_rate:
                return K_list[index]
        return K_list[index]
    

    def advance_time(self):
        """
        Advance the simulation time based on the total rate.

        :return: Time increment
        """
        return np.random.exponential(1.0 / self.total_rate)

    def run(self, steps, reactions_to_recode):
        """
        Run the KMC simulation for a given number of steps.

        :param steps: Number of steps to run the simulation
        :return: List of events and corresponding times
        """
        events = []
        times = []
        mkdir(self.prefix+'.traj')
        f_counter = open(self.prefix+'.goal_reaction_counter','w')
        f_counter = open(self.prefix+'.goal_reaction_counter','a')

        for self.step in range(steps):
            event = self.select_event(self.K_list)
            if event['reaction'] in reactions_to_recode:
                f_counter.write(str(self.time)+" "+event['reaction']+" "+str(event['resutls'])+"\n")

            dt = self.advance_time()
            self.time += dt
            events.append(event)
            self.refresh_str(self.atoms, event)
            self.build_event_list()

                           

            if self.step%100 == 0:
                write(self.prefix+'.traj/'+str(self.step).zfill(5)+'.t'+str(self.time)+'.xyz', self.atoms)
            times.append(self.time)

        return events, times
    
    def extract_matching_events(self, events, target_property, target_site_pair, target_adb_pair, prefix):
        '''
        根据events（events是由event*json文件合并而成的字典），找到target_property和target_pair（比如是bonds，或者sites）， 并形成新的字典
        '''
        K_list = []
        #单个event的格式：
        #{"OH_diff_1_2": {"k": 15, "resutls": ['O'] or ['OH','*']}}

        
        for key, value in events.items():
            if value['property'] == target_property: #see whether target is right
                if np.array_equal(value['site_pair'],target_site_pair):
                     
                    #site_pair是位点序号。位点没有方向
                    if value.get('ordered'):
                        #有方向向量, should match rigrously
                        if np.array_equal(value['rea'],target_adb_pair):
                            
                            k = value["Ea_np"][0]
                            resutls = value['pro']
 
                            K_list.append({"k": k, "resutls": resutls,"reaction":key, "prefix":prefix})

                        elif np.array_equal(value.get('pro'),target_adb_pair):

                            k = value["Ea_np"][1]
                            resutls = value['rea']
 
                            K_list.append({"k": k, "resutls": resutls,"reaction":key, "prefix":prefix})
                           
                    elif not value.get('ordered'):
                        #not 有方向向量
                        if (
                            np.array_equal(value['rea'],target_adb_pair) or \
                            np.array_equal(value['rea'],target_adb_pair[::-1])
                            ): #see whether 'site_pair' is right

                            k = value["Ea_np"][0]
                            resutls = value['pro']
 
                            K_list.append({"k": k, "resutls": resutls, "reaction":key, "prefix":prefix})
                        elif (
                            np.array_equal(value['pro'],target_adb_pair) or \
                            np.array_equal(value['pro'],target_adb_pair[::-1])
                            ): #see whether 'site_pair' is right
                            k = value["Ea_np"][1]
                            resutls = value['rea']
 
                            K_list.append({"k": k, "resutls": resutls, "reaction":key, "prefix":prefix})
                        
        return K_list  #one events for a single site.
    

    def refresh_str(self, atoms, event):

        #单个event的格式：
        #{'k': 0.025, 'results': ['OH'], 'reaction': 'water_ele_diss_1', 'prefix': '480'}

        prefix    = event['prefix']
        reaction  = event['reaction']
        resutls   = event['resutls']
        


        Qs   = self.atoms.get_initial_charges()
        if "-" in prefix:
            # is bond
            atm_id = int(prefix.split("-")[0])
            atm_jd = int(prefix.split("-")[1])

            adb_index_i = adbname_to_numindex(resutls[0])
            adb_index_j = adbname_to_numindex(resutls[1])
            Qs[atm_id] = adb_index_i
            Qs[atm_jd] = adb_index_j

            self.atoms.set_initial_charges(Qs)

        else:
            # is site
            atm_id = int(prefix)

            adb_index_i = adbname_to_numindex(resutls[0])            

            Qs[atm_id] = adb_index_i

            self.atoms.set_initial_charges(Qs)




# Example usage
reactions_to_recode=['water_diss_ni','water_diss_ni3c','OH_diff_1_1', 'OH_diff_1_2', 'OH_diff_2_3', 'OH_diff_3_4', 'OH_diff_4_5', 'OH_diff_5_5', 'OH_diff_2_1', 'OH_diff_3_2', 'OH_diff_4_3']
#Ni-Ni3C_atop_grid.xyz
#Ni_atop_grid.xyz
kmc = KMC(f_str)
events, times = kmc.run(20000,reactions_to_recode)



#events, times = kmc.run(100)

# Print the results
for event, time in zip(events, times):

    print(f"Time: {time:.3f}, Event: {event}")

