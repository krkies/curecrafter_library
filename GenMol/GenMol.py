from .Molecule import Molecule
import numpy as np
import json

#
def generateMolecule(jsonData, gridSize, originX, originY, originZ):
    # parse json data to numpy array
    moleculeArray = applyParse(jsonData, gridSize, originX, originY, originZ)
    # create new molecule by best atom at each grid location
    moleculeCreated = applyGrid(moleculeArray)
    # delete grids with atoms below threshold
    moleculeFiltered = applyThreshold(moleculeCreated, 135)
    # create PDB file from numpy array
    return applyPDB(moleculeFiltered, gridSize, originX, originY, originZ)

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
            moleculeList.append(Molecule('pdb', i[pdbName], i[scoreName], i[dateName], gridSize, originX, originY, originZ))

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

# find best atom type for each grid location
def applyGrid(moleculeArray):
    # count unique grid locations
    uniqueGrids = np.unique(moleculeArray[:,:-1], axis = 0)
    # create empty array of scores, default filled with zero
    uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)
    #
    countGrid = range(len(uniqueGrids))

    atomCount = 0
    printCount = 1
    lengthArray = len(moleculeArray)
    for row in moleculeArray:
        atomCount += 1
        if atomCount == printCount:
            printCount += 100
            remainingCount = lengthArray - atomCount
            print '{} : {} : {}'.format(lengthArray, atomCount, remainingCount)

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

# create PDB file format from CureCrafter grid format
def applyPDB(moleculeArray, gridSize, originX, originY, originZ):
    _moleculePDB = ''

    # overwrite atom type
    _index = 1
    for _row in moleculeArray:
        _sequenceNumber = str(_index).rjust(5)
        _atomName = _row[1]
        if (_atomName == 'NA'):
            _atomName = 'N'.ljust(3)
        elif (_atomName == 'HD'):
            _atomName = 'H'.ljust(3)
        elif (_atomName == 'OA'):
            _atomName = 'O'.ljust(3)
        else:
            _atomName = _atomName.ljust(3)

        # grid coordinates
        # round coordinates to fit in PDB file
        _coords = _row[0].split()
        if (float(_coords[0]) < 0):
            _xCoord = str(round(float(_coords[0]) * gridSize + originX - 0.5 * gridSize,5)).rjust(8)
        else:
            _xCoord = str(round(float(_coords[0]) * gridSize + originX + 0.5 * gridSize,5)).rjust(8)
        if (float(_coords[1]) < 0):
            _yCoord = str(round(float(_coords[1]) * gridSize + originY - 0.5 * gridSize,5)).rjust(8)
        else:
            _yCoord = str(round(float(_coords[1]) * gridSize + originY + 0.5 * gridSize,5)).rjust(8)
        if (float(_coords[2]) < 0):
            _zCoord = str(round(float(_coords[2]) * gridSize + originZ - 0.5 * gridSize,5)).rjust(8)
        else:
            _zCoord = str(round(float(_coords[2]) * gridSize + originZ + 0.5 * gridSize,5)).rjust(8)

        # symbol?
        _symbol = _row[1].ljust(2)

        # construct pdb atom entry
        _alternateIndicator = " "
        _chainIdentifier = " "
        _residueSequence = "1".rjust(4)
        _residueInsertions = " "
        _occupancy = "0".rjust(6)
        _temperatureFactor = "0".rjust(6)
        _segmentIdentifier = "0".ljust(4)
        _atomEntry = "ATOM" + "  " + _sequenceNumber + "  " + _atomName + _alternateIndicator + "LIG" + _chainIdentifier + _residueSequence + _residueInsertions + "   " + _xCoord + _yCoord + _zCoord + _occupancy + _temperatureFactor + "      " + _segmentIdentifier + "  " + _symbol + "\n"

        # insert atom row into pdb molecule
        _moleculePDB += _atomEntry

        # increment row
        _index += 1

    # append pdb termination line
    _moleculePDB += ("END" + "\n")

    return _moleculePDB
