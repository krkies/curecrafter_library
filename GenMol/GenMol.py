from Molecule import Molecule
import numpy as np

# create PDB file format from CureCrafter grid format
def createPDB(self, moleculeArray, gridSize, originX, originY, originZ):
    # overwrite atom type
    _index = 1
    for _row in moleculeArray:
        _sequenceNumber = str(_index).rjust(5)
        _atomName = _row[1]
        if (_atomName == 'NA'):
            _atomName = 'N'.ljust(4)
        elif (_atomName == 'HD'):
            _atomName = 'H'.ljust(4)
        elif (_atomName == 'OA'):
            _atomName = 'O'.ljust(4)
        else:
            _atomName = _atomName.ljust(4)

        # grid coordinates
        _coords = _row[0].split()
        if (float(_coords[0]) < 0):
            _xCoord = str(float(_coords[0]) * gridSize + originX - 0.5 * gridSize).rjust(8)
        else:
            _xCoord = str(float(_coords[0]) * gridSize + originX + 0.5 * gridSize).rjust(8)
        if (float(_coords[1]) < 0):
            _yCoord = str(float(_coords[1]) * gridSize + originY - 0.5 * gridSize).rjust(8)
        else:
            _yCoord = str(float(_coords[1]) * gridSize + originY + 0.5 * gridSize).rjust(8)
        if (float(_coords[2]) < 0):
            _zCoord = str(float(_coords[2]) * gridSize + originZ - 0.5 * gridSize).rjust(8)
        else:
            _zCoord = str(float(_coords[2]) * gridSize + originZ + 0.5 * gridSize).rjust(8)

        # symbol?
        _symbol = row[1].rjust(2)

        # construct pdb atom entry
        _alternateIndicator = " "
        _chainIdentifier = " "
        _residueSequence = "1".rjust(4)
        _residueInsertions = " "
        _occupancy = "0".rjust(6)
        _temperatureFactor = "0".rjust(6)
        _segmentIdentifier = "0".ljust(4)
        _atomEntry = "ATOM" + "  " + _sequenceNumber + " " + _atomName + _alternateIndicator + "LIG" + " " + _chainIdentifier + _residueSequence + _residueInsertions + "   " + xCoord + yCoord + zCoord + _occupancy + _temperatureFactor + "      " + _segmentIdentifier + _symbol + "\n"

        # insert atom row into pdb molecule
        _moleculePDB.append(_atomEntry)

        # increment row
        _index += 1

    # append pdb termination line
    _moleculePDB.append("END" + "\n")

    return _moleculePDB


# find best atom type for each grid location
def generateMolecule(listOfFiles, listOfScores, threshold, gridSize, originX, originY, originZ):
    #  1) Prepare list of input molecules
    #  2) Database of all atoms: type, grid location, and score
    #  3) Database of unique grid/atom type combinations
    #  4) Array of best atom type for each grid location
    #  5) Threshold removes atoms/grids with low scores
    #  6) Create PDB file

    # 1) populate listOfMolecules with pdb files & scores
    listOfMolecules = []
    for i in range(len(listOfFiles)):
        #construct new molecule for each pdb file
        listOfMolecules.append(Molecule('pdb', listOfFiles[i], listOfScores[i], gridSize, originX, originY, originZ))

    # 2) populate scoreBank (rows = atom, columns = type, grid, score)
    totalAtomCount = 0
    for i in listOfMolecules:
        totalAtomCount += i.getAtomCount()
    scoreBank = np.empty([totalAtomCount,3], dtype='<U100')

    index = 0
    for singleMolecule in listOfMolecules:
        currentScore = singleMolecule.getScore()
        for atom in singleMolecule.getAtoms():
            scoreBank[index,0] = str(atom.getAtomType())
            scoreBank[index,1] = str(atom.getGrid().getX()) + " " + str(atom.getGrid().getY()) + " " + str(atom.getGrid().getZ())
            scoreBank[index,2] = currentScore
            index += 1

    # 3) populate atom type grid locations with averages
    uniqueGrids = np.unique(scoreBank[:,:-1], axis = 0)
    uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)

    for row in scoreBank:
        for i in range(len(uniqueGrids)):
            if(np.all(row[:-1] == uniqueGrids[i])):
                temp = (uniqueScores[i,0] * uniqueScores[i,1]) + float(row[2])
                uniqueScores[i,1] += 1
                uniqueScores[i,0] = temp/uniqueScores[i,1]
    uniqueDatabase = np.column_stack((uniqueGrids, uniqueScores))

    # 4) populate new molecule -- best score at each grid location
    uniqueGridLocation = np.unique(uniqueDatabase[:,1])
    gridContents = np.empty(len(uniqueGridLocation))
    molScore = np.zeros(len(uniqueGridLocation))
    newMolecule = np.column_stack((uniqueGridLocation, gridContents, molScore))

    for grid in range(len(uniqueGridLocation)):
        for i in range(len(uniqueDatabase[:,1])):
            if (newMolecule[grid,0] == uniqueDatabase[i,1]):
                if(float(uniqueDatabase[i,2]) > float(newMolecule[grid,2])):
                    newMolecule[grid, 1] = uniqueDatabase[i,0]
                    newMolecule[grid, 2] = float(uniqueDatabase[i,2])

    # 5) delete grids with atoms below threshold
    arrayMolecule = np.delete(newMolecule, np.where(newMolecule[:, 2].astype(float)<threshold), axis = 0)

    # 6) create PDB
    pdbMolecule = createPDB(arrayMolecule, gridSize, originX, originY, originZ)

    return pdbMolecule
