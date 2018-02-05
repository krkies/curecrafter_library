# Step B Goal: average each grid position by atom type & molecule score
# Process:
#   Loop through list of molecules/PDB files
#   Initialize each as a molecule object
#   maxScore ; maxAtom ; gridLocation
#   For grid in molecule.grid, for grid.atomType, average score and store in variables
#   Return best atom for given grid location

# Could put as a method in new class of molecules (MoleculeFiles)
#--------------------------------------------------

# Do we have input array of PDB files?

#For one:
from Molecule import Molecule

filename = "Fixtures/molecule03.pdb"
pdbfile = open(filename, "r")

singleMolecule = Molecule('pdb', pdbfile, 100, 0.75, 18, -35, -18)
atomScore = str(singleMolecule.getScore())

# Just to get a working version, going to use a numpy array
# Obviously not optimized -- object would probably be better
import numpy as np
scoreBank = np.empty([singleMolecule.getAtomCount(),3], dtype='<U100')

counter = 0
for atom in singleMolecule.getAtoms():
    scoreBank[counter,0] = str(atom.getAtomType())
    scoreBank[counter,1] = str(atom.getGrid().getX()) + " " + str(atom.getGrid().getY()) + " " + str(atom.getGrid().getZ())
    scoreBank[counter,2] = atomScore
    counter += 1

# For one molecule, this doesn't do anything (obviously)
# Ideally, run scoreBank on multiple molecules before running unique
uniqueGrids = np.unique(scoreBank[:,:-1], axis = 0)
uniqueScores = len(uniqueGrids)
# Find Best
# Getting workable version -- not optimized


for row in scoreBank:
    for i in range(len(uniqueGrids)):
        if(np.all(row[:-1] == uniqueGrids[i])):
            ##Append score here
            
