from .Molecule import Molecule
import numpy as np
import json

class Coordinate(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def setCoordinates(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class GenMol(Coordinate):

    def __init__(self, gameNumber, gridSize, receptorData, moleculeData):
        self.gameNumber = gameNumber
        self.gridSize = gridSize
        self.moleculeQuery = 'boardQuery'
        self.moleculePDB = 'molDock'
        self.moleculeDate = 'dockEnded'
        self.moleculeScore = 'score'
        self.receptorQuery = 'receptorQuery'
        self.receptorX = 'receptorX'
        self.receptorY = 'receptorY'
        self.receptorZ = 'receptorZ'
        # self.Origins = self.parseReceptorData(receptorData)
        self.Origins = Coordinate(18, -35, -18)
        # self.MoleculeGrid = self.parseMoleculeData(moleculeData)
        self.MoleculeGrid = self.getGridFile()
        self.threshold = self.getAvgThreshold()

    def saveGridFile(self):
        self.GridFile = np.save('gridFile.npy', self.MoleculeGrid)
        return self.GridFile

    def getGridFile(self):
        return np.load('gridFile.npy')


    #
    def parseMoleculeData(self, jsonData):
        # parse json data to python
        _parsedJson = json.loads(jsonData)
        # error check for mislabeled data structure
        if not _parsedJson['data'][self.moleculeQuery][0][self.moleculePDB]:
            print 'JSON Formatting Error - key names should be: {}, {}, {}'.format(self.moleculePDB, self.moleculeData, self.moleculeScore)
            print data['data'][self.moleculePDB][0]
        #
        _dataArray = _parsedJson['data'][self.moleculeQuery]
        # create list of molecule objects
        _moleculeList = []
        for i in _dataArray:
            if i[self.moleculePDB] and i[self.moleculeScore]:
                _molecule = Molecule(self.gridSize, self.Origins.getX(), self.Origins.getY(), self.Origins.getZ())
                _molecule.parsePDBfile(i[self.moleculePDB], i[self.moleculeScore], i[self.moleculeDate])
                _moleculeList.append(_molecule)

        # count all atoms in all input files
        _totalAtomCount = 0
        for i in _moleculeList:
            _totalAtomCount += i.getAtomCount()

        # populate moleculeArray (rows = atom, columns = type, grid, score)
        _moleculeArray = np.empty([_totalAtomCount,3], dtype='<U100')
        _index = 0
        for _molecule in _moleculeList:
            _currentScore = _molecule.getScore()
            for _atom in _molecule.getAtoms():
                _moleculeArray[_index,0] = str(_atom.getAtomType())
                _moleculeArray[_index,1] = str(_atom.getGrid().getX()) + " " + str(_atom.getGrid().getY()) + " " + str(_atom.getGrid().getZ())
                _moleculeArray[_index,2] = _currentScore
                _index += 1

        self.MoleculeGrid = _moleculeArray
        self.MoleculeGrid = self.getSelectedGrid()
        self.saveGridFile()
        return self.MoleculeGrid

    #
    def parseReceptorData(self, jsonData):
        # parse json data to python
        _parsedJson = json.loads(jsonData)
        #
        _dataArray = _parsedJson['data'][self.receptorQuery]
        #
        _Orient = Coordinate(_dataArray[self.receptorX], _dataArray[self.receptorY], _dataArray[self.receptorZ])
        return _Orient

    #
    def getMoleculeGrid(self):
        return self.MoleculeGrid

    def getSelectedGrid(self):
        _selectedGrid = self.applySelection()
        self.MoleculeGrid = _selectedGrid
        return self.MoleculeGrid

    #
    def getOrigins(self):
        return self.Origins

    #
    def getAvgThreshold(self):
        _scores = self.MoleculeGrid[:,2].astype(np.float)
        self.avgScore = _scores.mean()
        self.stdScore = _scores.std()
        self.threshold = self.avgScore
        return self.threshold

    #
    def getStandardDeviation(self):
        return self.stdScore

    #
    def generateMolecule(self, threshold):
        # delete grids with atoms below threshold
        _moleculeFiltered = self.applyThreshold(threshold)
        # create PDB file from numpy array
        _moleculeCreated = Molecule(self.gridSize, self.Origins.getX(),  self.Origins.getY(),  self.Origins.getZ())
        _moleculePDB = _moleculeCreated.generateMolecule(_moleculeFiltered)
        return _moleculePDB

    # select best atom type for each grid location
    def applySelection(self):
        # count unique grid locations
        uniqueGrids = np.unique(self.MoleculeGrid[:,:-1], axis = 0)
        # create empty array of scores, default filled with zero
        uniqueScores = np.zeros([len(uniqueGrids),2], dtype = float)
        # store number of unique grids
        countGrid = range(len(uniqueGrids))

        atomCount = 0
        printCount = 1
        lengthArray = len(self.MoleculeGrid)
        for row in self.MoleculeGrid:
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
        moleculeSelected = np.column_stack((uniqueGridLocation, gridContents, moleculeScore))

        for grid in range(len(uniqueGridLocation)):
            for i in range(len(uniqueDatabase[:,1])):
                if (moleculeSelected[grid,0] == uniqueDatabase[i,1]):
                    if (float(uniqueDatabase[i,2]) > float(moleculeSelected[grid,2])):
                        moleculeSelected[grid, 1] = uniqueDatabase[i,0]
                        moleculeSelected[grid, 2] = float(uniqueDatabase[i,2])

        return moleculeSelected

    #
    def applyThreshold(self, threshold):
        return np.delete(self.MoleculeGrid, np.where(self.MoleculeGrid[:, 2].astype(float)<threshold), axis = 0)
