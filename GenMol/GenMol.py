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

    def __init__(self, gameNumber, gridSize):
        self.gameNumber = gameNumber
        self.gridSize = gridSize
        # set reference coordinates of molecule in receptor coordinates
        # self.Origins = self.parseReceptorData(receptorData)
        # coordinatesfrom database
        self.Origins = Coordinate(18, -35, -18)
        # generate grid of atoms for each molecule in dataset
        self.MoleculeGrid = self.parseMoleculeData(moleculeData)
        # self.MoleculeGrid = self.getGridFile()
        self.threshold = self.getAvgThreshold()

    # generate molecule (PDB file) from grid by selecting atoms in grid by position
    def generateMolecule(self, threshold):
        # delete grids with atoms below threshold
        _moleculeFiltered = self.applyThreshold(threshold)
        # create PDB file from numpy array
        _moleculeCreated = Molecule(self.gridSize, self.Origins.getX(),  self.Origins.getY(),  self.Origins.getZ())
        _moleculePDB = _moleculeCreated.generateMolecule(_moleculeFiltered)
        return _moleculePDB

    # save numpy array file to cache
    def saveGridFile(self):
        self.GridFile = np.save('gridFile.npy', self.MoleculeGrid)
        return self.GridFile

    # select best atom type for each grid location
    def applySelection(self):
        int(_gridType) = -1
        int(_atom) = 0
        int(_coord) = 1
        int(_score) = 2
        # create empty arrays
        uniqueScores = np.zeros([len(uniqueGrids),_score], dtype = float)
        gridContents = np.empty(len(uniqueGridLocation))
        moleculeScore = np.zeros(len(uniqueGridLocation))

        # unique grid identities -> identity is atom type at a grid location
        uniqueGrids = np.unique(self.MoleculeGrid[:,_gridType], axis = 0)

        # for each grid position in 3D space
        for entry in self.MoleculeGrid:
            # prevent iterating over empty grids
            for _index, _row in enumerate(uniqueGrids):

            for gridNum in gridCount:
                # np.all - test if entry matches a unique grid
                if (np.all(entry[:-1] == gridNum):
                    temp = (uniqueScores[gridNum,0] * uniqueScores[gridNum,1]) + float(row[2])
                    uniqueScores[gridNum,1] += 1
                    uniqueScores[gridNum,0] = temp/uniqueScores[gridNum,1]

        # combine both arrays to make one score for each grid identity
        uniqueDatabase = np.column_stack(uniqueGrids, uniqueScores)

        # populate created molecule -- best score at each grid location
        uniqueGridLocation = np.unique(uniqueDatabase[:,1])
        moleculeSelected = np.column_stack((uniqueGridLocation, gridContents, moleculeScore))

        # pick only one atom for each coordinate
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

    # open numpy array file from cache
    def getGridFile(self):
        return np.load('gridFile.npy')

    #
    def getMoleculeGrid(self):
        return self.MoleculeGrid

    #
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
