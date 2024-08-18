# KMC_simulation-Ni3C-Ni
## usage : 

python kmc.py Ni_atop_grid.xyz

python kmc.py Ni-Ni3C_atop_grid.xyz

## notes:
The dump traj are in floders of Ni_atop_grid.traj and Ni-Ni3C_atop_grid.traj <br>
The key catalytic reactions, inclding OH diffusion and H+OH-->H2O, once takes place, will be recorded in Ni_atop_grid.goal_reaction_counter and  Ni-Ni3C_atop_grid.goal_reaction_counter <br>
all the reaction information needed for running a kmc is in event.*.json
