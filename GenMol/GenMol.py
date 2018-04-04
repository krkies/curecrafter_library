from .Molecule import Molecule
import numpy as np
import json

#
def generateGrid(jsonData, gridSize, originX, originY, originZ):
    # parse json data to numpy array
    return applyParse(jsonData, gridSize, originX, originY, originZ)

#
def generateMolecule(moleculeGrid, gridSize, originX, originY, originZ):
    # create new molecule using best atom at each grid location
    moleculeSelected = applySelection(moleculeGrid)
    # delete grids with atoms below threshold
    moleculeFiltered = applyThreshold(moleculeSelected, 100)
    # create PDB file from numpy array
    moleculeCreated = Molecule(gridSize, originX, originY, originZ)
    moleculePDB = moleculeCreated.generateMolecule(moleculeFiltered)
    return moleculePDB

#
def applyParse(jsonData, gridSize, originX, originY, originZ):
    queryName = 'boardQuery'
    pdbName = 'molDock'
    dateName = 'dockEnded'
    scoreName = 'score'
    # parse json data to python
    parsedJson = json.loads(jsonData)
    # error check for mislabeled data structure
    if not parsedJson['data'][queryName][0][pdbName]:
        print 'JSON Formatting Error - key names should be: {}, {}, {}'.format(pdbName, dateName, scoreName)
        print parsedJson['data'][queryName][0]

    #
    dataArray = parsedJson['data'][queryName]
    # create list of molecule objects
    moleculeList = []
    for i in dataArray:
        if i[pdbName] and i[scoreName]:
            molecule = Molecule(gridSize, originX, originY, originZ)
            molecule.parsePDBfile(i[pdbName], i[scoreName], i[dateName])
            moleculeList.append(molecule)

    # count all atoms in all input files
    totalAtomCount = 0
    for i in moleculeList:
        totalAtomCount += i.getAtomCount()

    # populate moleculeArray (rows = atom, columns = type, grid, score)
    moleculeArray = np.empty([totalAtomCount,3], dtype='<U100')
    index = 0
    for molecule in moleculeList:
        currentScore = molecule.getScore()
        for atom in molecule.getAtoms():
            moleculeArray[index,0] = str(atom.getAtomType())
            moleculeArray[index,1] = str(atom.getGrid().getX()) + " " + str(atom.getGrid().getY()) + " " + str(atom.getGrid().getZ())
            moleculeArray[index,2] = currentScore
            index += 1

    return moleculeArray

# select best atom type for each grid location
def applySelection(moleculeArray):
    # count unique grid locations
    uniqueGrids = np.unique(moleculeArray[:,:-1], axis = 0)
    # create empty array of scores, default filled with zero
    uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)
    # store number of unique grids
    countGrid = range(len(uniqueGrids))

    atomCount = 0
    printCount = 1
    lengthArray = len(moleculeArray)
    for row in moleculeArray:
        # atomCount += 1
        # if atomCount == printCount:
        #     printCount += 100
        #     remainingCount = lengthArray - atomCount
        #     print '{} : {} : {}'.format(lengthArray, atomCount, remainingCount)

        for i in countGrid:
            if (np.all(row[:-1] == uniqueGrids[i])):
                temp = (uniqueScores[i,0] * uniqueScores[i,1]) + float(row[2])
                uniqueScores[i,1] += 1
                uniqueScores[i,0] = temp/uniqueScores[i,1]
    uniqueDatabase = np.column_stack((uniqueGrids, uniqueScores))

    # populate created molecule -- best score at each grid location
    uniqueGridLocation = np.unique(uniqueDatabase[:,1])
    gridContents = np.empty(len(uniqueGridLocation))
    moleculeScore = np.zeros(len(uniqueGridLocation))
    moleculeCreated = np.column_stack((uniqueGridLocation, gridContents, moleculeScore))

    for grid in range(len(uniqueGridLocation)):
        for i in range(len(uniqueDatabase[:,1])):
            if (moleculeCreated[grid,0] == uniqueDatabase[i,1]):
                if (float(uniqueDatabase[i,2]) > float(moleculeCreated[grid,2])):
                    moleculeCreated[grid, 1] = uniqueDatabase[i,0]
                    moleculeCreated[grid, 2] = float(uniqueDatabase[i,2])

    return moleculeCreated

#
def applyThreshold(molecule, threshold):
    return np.delete(molecule, np.where(molecule[:, 2].astype(float)<threshold), axis = 0)
