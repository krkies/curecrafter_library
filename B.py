## Step B Goal: Average scores -- Find best atom type for each grid location
## Process:
##  1) Prepare list of input molecules
##  2) Databse of all atoms: type, grid location, and score
##  3) Database of unique grid/atom type combinations
##  4) Array of best atom type for each grid location
##  5) Threshold removes atoms/grids with low scores

# Could put as a method in new class of molecules (MoleculeFiles)
#--------------------------------------------------
from Molecule import Molecule
import numpy as np
thresholdScore = 135

#-------------------------
# 1) Initialize and Populate listOfMolecules with correct pdb files/scores
listOfMolecules = []
filename1 = "Fixtures/molecule03.pdb"
filename2 = "Fixtures/molecule4956.pdb"
filename3 = "Fixtures/molecule5390.pdb"
filename4 = "Fixtures/molecule5570.pdb"
files = [filename1, 100, filename2, 130, filename3, 144, filename4, 101]

for i in range(len(files)//2):
    listOfMolecules.append(Molecule('pdb', open(files[2*i], "r"), files[2*i+1], 0.75, 18, -35, -18))
#-------------------------

#-------------------------
# 2) Initialize and populate scoreBank (rows = atom, columns = type, grid, score)
totalAtomCount = 0
for i in listOfMolecules:
    totalAtomCount += i.getAtomCount()
scoreBank = np.empty([totalAtomCount,3], dtype='<U100')

counter = 0
for singleMolecule in listOfMolecules:
    currentScore = singleMolecule.getScore()
    for atom in singleMolecule.getAtoms():
        scoreBank[counter,0] = str(atom.getAtomType())
        scoreBank[counter,1] = str(atom.getGrid().getX()) + " " + str(atom.getGrid().getY()) + " " + str(atom.getGrid().getZ())
        scoreBank[counter,2] = currentScore
        counter += 1
#-------------------------

#-------------------------
# 3) Initialize and populate atom type grid locations w/ averages
uniqueGrids = np.unique(scoreBank[:,:-1], axis = 0)
uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)

for row in scoreBank:
    for i in range(len(uniqueGrids)):
        if(np.all(row[:-1] == uniqueGrids[i])):
            temp = (uniqueScores[i,0] * uniqueScores[i,1]) + float(row[2])
            uniqueScores[i,1] += 1
            uniqueScores[i,0] = temp/uniqueScores[i,1]
uniqueDatabase = np.column_stack((uniqueGrids, uniqueScores))
#-------------------------

#-------------------------
# 4) Initialize and populate new molecule -- best score at each grid location
uniqueGridLocation = np.unique(uniqueDatabase[:,1])
gridContents = np.empty(len(uniqueGridLocation))
molScore = np.zeros(len(uniqueGridLocation))
newMolecule = np.column_stack((uniqueGridLocation, gridContents, molScore))

for gridspot in range(len(uniqueGridLocation)):
    for i in range(len(uniqueDatabase[:,1])):
        if (newMolecule[gridspot,0] == uniqueDatabase[i,1]):
            if(float(uniqueDatabase[i,2]) > float(newMolecule[gridspot,2])):
                newMolecule[gridspot, 1] = uniqueDatabase[i,0]
                newMolecule[gridspot, 2] = float(uniqueDatabase[i,2])
#-------------------------

#-------------------------
# 5) Delete grids with atoms below threshold
finalMolecule = np.delete(newMolecule, np.where(newMolecule[:, 2].astype(float)<thresholdScore), axis = 0)
#-------------------------
print(newMolecule)
print(len(newMolecule[:,1]))
print("HI")
print("HI")
print(finalMolecule)
print(len(finalMolecule[:,1]))
