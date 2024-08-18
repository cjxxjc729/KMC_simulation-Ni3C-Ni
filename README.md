# KMC_simulation-Ni3C-Ni
## descriptions:

This project focuses on a kinetic Monte Carlo (KMC) simulation code for the reaction H + OH → H2O on Ni3C-Ni and Ni. The goal is to demonstrate that on pure Ni, the formation of OH through water dissociation is more difficult, making the direct H + OH → H2O reaction less favorable. On the other hand, Ni3C facilitates easier water dissociation to form OH, with faster OH diffusion. Thus, in the presence of Ni3C, Ni can utilize Ni3C as an auxiliary catalyst, absorbing and reacting with OH transferred from Ni3C to facilitate the H + OH → H2O reaction.

## usage : 

python kmc.py Ni_atop_grid.xyz

python kmc.py Ni-Ni3C_atop_grid.xyz

## notes:
The dump traj are in floders of Ni_atop_grid.traj and Ni-Ni3C_atop_grid.traj <br>

The key catalytic reactions, inclding OH diffusion and H+OH-->H2O, once takes place, will be recorded in Ni_atop_grid.goal_reaction_counter and Ni-Ni3C_atop_grid.goal_reaction_counter <br>

all the reaction information needed for running a kmc is in event.*.json

## event list
![image](https://github.com/user-attachments/assets/964143f5-f2cd-48d2-8d1a-159fc3904ce2)  <br>
all the kinetic information used in simulation

## snapshots for Ni3C-Ni and Ni
![image](https://github.com/user-attachments/assets/86e8bb6d-5fb9-40bd-9e5c-8ad09fc22a19)  <br>

![image](https://github.com/user-attachments/assets/35e5f579-12ae-4985-a6e1-eadf8d5d7a70) <br>

Snapshots along the KMC simulation on pristine Ni3C-Ni and Ni catalyst, being sampled every 1000 KMC steps. The red, blue and white dots represent the *OH, *H and * (i.e., surface blank sites) species. The Ni atom is colored in green.

## results count
![image](https://github.com/user-attachments/assets/6aa01a26-92ea-47c1-bc3f-5c7fa7c7a24e) <br>
Counting of the water formation reaction (*OH + *H → H2O + 2*) on (a) Ni3C-Ni and (b) Ni catalysts along the KMC simulation time.


