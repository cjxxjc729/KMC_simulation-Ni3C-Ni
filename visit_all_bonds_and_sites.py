#!/home/cjx/deepmd-kit-2.2.9/bin/python3.11

import sys


from ase.io import write
from ase.io import read
from ase import neighborlist
from ase import geometry
import numpy as np

import os
import time
import re


def get_ar_bonds(f_in):
    atoms=read(f_in)
    cell=atoms.get_cell()

    D,Dlen=geometry.get_distances(atoms.get_positions(),atoms.get_positions(),cell=cell,pbc=True)

    np.fill_diagonal(Dlen, 1E7)


    # 对矩阵进行按元素排序，并获取排序后的索引
    #sorted_indices = np.argsort(Dlen, axis=None)[:10]
    bond_pair_index = np.where(Dlen < 3)
    print(bond_pair_index)

    
    # 打印排序后的元素和相应位置
    ar_bonds=[]
    for index in range(len(bond_pair_index[0])):

        atm_id = bond_pair_index[0][index]
        atm_jd = bond_pair_index[1][index]

        elei=atoms.symbols[atm_id]
        elej=atoms.symbols[atm_jd]
        if elei == 'Ar' and elej == 'Ar' and atm_id < atm_jd:

            ar_bonds = np.append(ar_bonds, [atm_id, atm_jd])


    ar_bonds = ar_bonds.reshape(-1,2)   
    return ar_bonds

def get_ar_sites(f_in):
    atoms=read(f_in)

    ar_sites = [atom.index for atom in atoms if atom.symbol == 'Ar']

    return ar_sites

if __name__ == "__main__":

    f_in = sys.argv[1]
    ar_bonds = get_bonds(f_in)
    ar_sites = get_sites(f_in)

    
