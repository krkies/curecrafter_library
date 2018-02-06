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
uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)
# Find Best

# Pretty sure numpy arrays are much more clever than double loops but
# just getting workable version -- not optimized

#Average scores for each grid location and atom type
for row in scoreBank:
    for i in range(len(uniqueGrids)):
        if(np.all(row[:-1] == uniqueGrids[i])):
            ##Average Score here
            temp = (uniqueScores[i,0] * uniqueScores[i,1]) + float(row[2])
            uniqueScores[i,1] += 1
            uniqueScores[i,0] = temp/uniqueScores[i,1]

#Find best average for each grid location
uniqueDatabase = np.concatenate((uniqueGrids, uniqueScores), axis = 1)
uniqueGridLocation = np.unique(uniqueDatabase[:,1])
#molGrid = np.empty(len(uniqueGridLocation), dtype = '<U100')
gridContents = np.empty(len(uniqueGridLocation))
molScore = np.zeros(len(uniqueGridLocation))
newMolecule = np.column_stack((uniqueGridLocation, gridContents, molScore))

# Test molecule has both HD and NA at grid 0,2,0

for gridspot in range(len(uniqueGridLocation)):
    for i in range(len(uniqueDatabase[:,1])):
        if (newMolecule[gridspot,0] == uniqueDatabase[i,1]):
            #This is where a threshold could be
            if(float(uniqueDatabase[i,2]) > float(newMolecule[gridspot,2])):
                newMolecule[gridspot, 1] = uniqueDatabase[i,0]
                newMolecule[gridspot, 2] = float(uniqueDatabase[i,2])
## Need to compare scores and append the molecule type!!!!!

print(newMolecule)
print(len(newMolecule[:,1]))
