# Step B Goal: average each grid position by atom type & molecule score
# Process:
#   Loop through list of molecules/PDB files
#   Initialize each as a molecule object
#   maxScore ; maxAtom ; gridLocation
#   For grid in molecule.grid, for grid.atomType, average score and store in variables
#   Return best atom for given grid location

# Could put as a method in new class of molecules (MoleculeFiles)
#--------------------------------------------------
## Whole thing is rough draft

#Molecules in Fixtures Directory
#molecule3 -- 100
#molecule4956 -- 130
#molecule5390 -- 144
#molecule5570 -- 101

#For multiple:
from Molecule import Molecule

listOfMolecules = []
#MoleculeList-------------
filename1 = "Fixtures/molecule03.pdb"
pdbfile1 = open(filename1, "r")
file1Score = 100
molecule1 = Molecule('pdb', pdbfile1, file1Score, 0.75, 18, -35, -18)
listOfMolecules.append(molecule1)

filename2 = "Fixtures/molecule4956.pdb"
pdbfile2 = open(filename2, "r")
file2Score = 130
molecule2 = Molecule('pdb', pdbfile2, file2Score, 0.75, 18, -35, -18)
listOfMolecules.append(molecule2)

filename3 = "Fixtures/molecule5390.pdb"
pdbfile3 = open(filename3, "r")
file3Score = 144
molecule3 = Molecule('pdb', pdbfile3, file3Score, 0.75, 18, -35, -18)
listOfMolecules.append(molecule3)

filename4 = "Fixtures/molecule5570.pdb"
pdbfile4 = open(filename4, "r")
file4Score = 101
molecule4 = Molecule('pdb', pdbfile4, file4Score, 0.75, 18, -35, -18)
listOfMolecules.append(molecule4)
#-------------------------
totalAtomCount = 0
for i in listOfMolecules:
    totalAtomCount += i.getAtomCount()
    print(i.getAtomCount())


import numpy as np
scoreBank = np.empty([totalAtomCount,3], dtype='<U100')

##Run this on all molecules
counter = 0
for singleMolecule in listOfMolecules:
    currentScore = singleMolecule.getScore()
    for atom in singleMolecule.getAtoms():
        scoreBank[counter,0] = str(atom.getAtomType())
        scoreBank[counter,1] = str(atom.getGrid().getX()) + " " + str(atom.getGrid().getY()) + " " + str(atom.getGrid().getZ())
        scoreBank[counter,2] = currentScore
        counter += 1

#-------
uniqueGrids = np.unique(scoreBank[:,:-1], axis = 0)
uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)
# Find Best


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
