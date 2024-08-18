# KMC_simulation-Ni3C-Ni
usage : 

for Ni:  python kmc.py Ni_atop_grid.xyz 

for Ni3C-Ni: python kmc.py   Ni-Ni3C_atop_grid.xyz 

# The dump traj are in floders of Ni_atop_grid.traj and Ni-Ni3C_atop_grid.traj
# The key catalytic reaction, inclding OH diffusion and H+OH-->H2O are recorded in Ni_atop_grid.goal_reaction_counter and  Ni-Ni3C_atop_grid.goal_reaction_counter
# all the reaction information needed for running a kmc is in event.*.json
