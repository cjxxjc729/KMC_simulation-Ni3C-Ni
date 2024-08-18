#!/usr/bin/python3
f_atoms=input('enter the str file (cif): ')
#f_id_list=input('enter the surf_id_list file')

import sys
sys.path.append("/home/cjx/script/mimic_suite/")
sys.path.append("/home/cjx/script/ase_based_constraint_opt_suite/")

from ase.io import write
from ase.io import read
from ase import neighborlist
from ase import geometry
import numpy as np
from mimic_functions import *
from project_to_grid_functions import *
import os
import time
import re

from ase import Atoms,Atom



char_length=1.5
atoms=read(f_atoms)
prefix='.'.join(f_atoms.split('.')[:-1])

surf_ids=np.where(atoms.positions[:,2] > 13)[0]
surf_ids=surf_ids-1
surf_ids=surf_ids.astype(int)

for surf_id in surf_ids:
  print("==="+str(surf_id)+"====")
  norm_vec=vect_for_most_sparse_locally(atoms, surf_id)
  surf_id_cor=atoms.get_positions()[surf_id]
  Ar_cor=surf_id_cor+norm_vec*char_length
  Ar=Atom('Ar',position=(Ar_cor[0],Ar_cor[1],Ar_cor[2]))
  atoms.append(Ar)

write(prefix+'_atop_grid.xyz',atoms)
