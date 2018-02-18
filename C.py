#Step C: Produce pdb file

#open file
writeOutFile = open("testPDB.pdb", "w")
gridSize = 0.75
originX = 18
originY = -35
originZ = -18

#_______________________________

from Molecule import Molecule
import numpy as np
thresholdScore = 135

listOfMolecules = []
filename1 = "Fixtures/molecule03.pdb"
filename2 = "Fixtures/molecule4956.pdb"
filename3 = "Fixtures/molecule5390.pdb"
filename4 = "Fixtures/molecule5570.pdb"
files = [filename1, 100, filename2, 130, filename3, 144, filename4, 101]

for i in range(len(files)//2):
    listOfMolecules.append(Molecule('pdb', open(files[2*i], "r"), files[2*i+1], 0.75, 18, -35, -18))

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

uniqueGrids = np.unique(scoreBank[:,:-1], axis = 0)
uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)

for row in scoreBank:
    for i in range(len(uniqueGrids)):
        if(np.all(row[:-1] == uniqueGrids[i])):
            temp = (uniqueScores[i,0] * uniqueScores[i,1]) + float(row[2])
            uniqueScores[i,1] += 1
            uniqueScores[i,0] = temp/uniqueScores[i,1]
uniqueDatabase = np.column_stack((uniqueGrids, uniqueScores))

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

finalMolecule = np.delete(newMolecule, np.where(newMolecule[:, 2].astype(float)<thresholdScore), axis = 0)


#_______________________________

#ATOM      1  C   LIG    1       19.102 -34.723 -16.947  0.00  0.00    +0.172 C
ATOM = "ATOM"
alternateIndicator = " "
residueName = "LIG"
chainIdentifier = " "
residueSequence = "1".rjust(4)
residueInsertions = " "
occupancy = "0".rjust(6)
temperatureFactor = "0".rjust(6)
segmentIdentifier = "0".ljust(4)

pdbCounter = 1
for row in finalMolecule:
    serialNumber = str(pdbCounter).rjust(5)
    atomName = row[1].ljust(4)

    coords = row[0].split()
    if (float(coords[0]) < 0):
        xCoord = str(float(coords[0]) * gridSize + originX - 0.5 * gridSize).rjust(8)
    else:
        xCoord = str(float(coords[0]) * gridSize + originX + 0.5 * gridSize).rjust(8)
    if (float(coords[1]) < 0):
        yCoord = str(float(coords[1]) * gridSize + originY - 0.5 * gridSize).rjust(8)
    else:
        yCoord = str(float(coords[1]) * gridSize + originY + 0.5 * gridSize).rjust(8)
    if (float(coords[2]) < 0):
        zCoord = str(float(coords[2]) * gridSize + originZ - 0.5 * gridSize).rjust(8)
    else:
        zCoord = str(float(coords[2]) * gridSize + originZ + 0.5 * gridSize).rjust(8)

    symbol = row[1].rjust(2)

    lineInformation = ATOM + "  " + serialNumber + " " + atomName + alternateIndicator + residueName + " " + chainIdentifier + residueSequence + residueInsertions + "   " + xCoord + yCoord + zCoord + occupancy + temperatureFactor + "      " + segmentIdentifier + symbol + "\n"
    writeOutFile.write(lineInformation)

    pdbCounter += 1

writeOutFile.write("END")
writeOutFile.close()
