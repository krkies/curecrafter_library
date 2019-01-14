class Atom(object):

    # Position: absolute coordinates of atom in molecule
    # Grid: 3D grid position atom assigned
    def __init__(self, atomName, atomType, Position, Grid):
        self.atomName = atomName
        self.atomType = atomType
        self.Position = Position
        self.Grid = Grid

    def getAtomType(self):
        return self.atomType

    def getPosition(self):
        return self.Position

    def getGrid(self):
        return self.Grid

    def setAtomName(self, atomName):
        self.atomName = atomName

    def setAtomType(self, atomType):
        self.atomType = atomType

    def setPosition(self, x, y, z):
        self.Position = setCoordinates(x, y, z)

    def setGrid(self, x, y, z):
        self.Grid = setCoordinates(x, y, z)

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

class Molecule(Coordinate, Atom):

    def __init__(self, pdbFile, gridSize, originX, originY, originZ):
        self.score = None
        self.date = None
        self.Atoms = parsePDB(pdbFile)
        self.gridSize = float(gridSize)
        # Container is overall dimensions of container for all molecules
        _xOrigin = float(originX)
        _yOrigin = float(originY)
        _zOrigin = float(originZ)
        self.Container = Coordinate(_xOrigin, _yOrigin, _zOrigin)
        self.Atoms = []

    def setScore(self, score, date):
        self.score = float(score)
        self.date= date

    # convert molecule from PDB coordinate to grid format
    def parsePDB(self, pdbFile):
        # Split pdb file into array of lines
        _atomArray = pdbFile.splitlines()
        # Extract atom block into array of Atom objects
        self.Atoms = []
        for i in range(len(_atomArray[:-1])):
            _atomInfo = _atomArray[i].split()
            # Extract atom type
            _atomName = _atomInfo[2]
            _atomType = _atomInfo[11]
            # Extract atom Position coorindates
            _xPos = float(_atomInfo[5])
            _yPos = float(_atomInfo[6])
            _zPos = float(_atomInfo[7])
            _Position = Coordinate(_xPos, _yPos, _zPos)
            # Set grid position of atom in 3D coordinates
            _Grid = self._calculateGrid(_xPos, _yPos, _zPos)
            # Append atom to array
            self.Atoms.append(Atom(_atomName,_atomType, _Position, _Grid))

        return self.Atoms

    def generatePDB(self, moleculeGrid):
        _pdbMolecule = FormatPDB(moleculeGrid, self.Container, self.gridSize)
        return _pdbMolecule.getPDB()

    def _calculateGrid(self, posX, posY, posZ):
        _xPosition = float(posX)
        _yPosition = float(posY)
        _zPosition = float(posZ)

        # calculate distance from origin
        _xDelta = float(_xPosition - self.Container.getX())
        _yDelta = float(_yPosition - self.Container.getY())
        _zDelta = float(_zPosition - self.Container.getZ())
        # calculate grid position
        _xGrid = int(_xDelta / self.gridSize)
        _yGrid = int(_yDelta / self.gridSize)
        _zGrid = int(_zDelta / self.gridSize)

        # create grid object
        _Grid = Coordinate(_xGrid, _yGrid, _zGrid)
        return _Grid

    def updateGrid(self):
        # update each Atom object in array
        for i in self.Atoms:
            # get Atom object
            _Atom = self.Atoms[i]
            # get Position object
            _Position = _Atom.getPosition()
            # extract coordinates from Position object
            _xPosition = float(_Position.getX())
            _yPosition = float(_Position.getY())
            _zPosition = float(_Position.getZ())
            # calculate new grid coordinates
            _Grid = self._calculateGrid(_xPosition, _yPosition, _zPosition)
            # extract coordinates from Grid object
            _xGrid = int(_Grid.getX())
            _yGrid = int(_Grid.getY())
            _zGrid = int(_Grid.getZ())
            # set Grid object in Atom object
            _Atom.setGrid(_xGrid, _yGrid, _zGrid)

    def getAtomCount(self):
        return len(self._Atoms)

    def getGrid(self, x, y, z):
        # loop over each Atom object in array to find match
        for i in self.Atoms:
            # get Atom object
            _Atom = self.Atoms[i]
            # get Grid object
            _Grid = _Atom.getGrid()
            # extract coordinates from Grid object
            _xGrid = int(_Grid.getX())
            _yGrid = int(_Grid.getY())
            _zGrid = int(_Grid.getZ())
            # if matched grid coordinates, return Atom object
            if (x == _xGrid and y == _yGrid and z == _zGrid):
                return _Atom
        # no matches
        return None

    def getAtoms(self):
        return self.Atoms

    def getAtom(self, index):
        _index = int(index)
        return self.Atoms[_index]

    def getGridSize(self):
        return self.gridSize

    def getScore(self):
        return self.score

    def getDate(self):
        return self.date

    def getContainer(self):
        return self.Container

    def setScore(self, score):
        self.score = float(score)

    def setDate(self, date):
        self.date = date

    def setGridSize(self, gridSize):
        self.gridSize = float(gridSize)
        self.updateGrid()

    def setContainerSize(self, x, y, z):
        _x = float(x)
        _y = float(y)
        _z = float(z)
        self.Container = Coordinate(_x, _y, _z)
        self.updateGrid()

    def setAtomPosition(self, index, x, y, z):
        _x = float(x)
        _y = float(y)
        _z = float(z)
        self.Atoms[index].setPosition(_x, _y, _z)

    def setAtomGrid(self, index, x, y, z):
        _x = float(x)
        _y = float(y)
        _z = float(z)
        self.Atoms[index].setGrid(_x, _y, _z)

    def setAtomType(self, index, atomType):
        _index = int(index)
        _atomType = str(atomType)
        self.Atoms[_index].setAtomType(_atomType)

    def setAtomName(self, index, atomName):
        _index = int(index)
        _atomName = str(atomName)
        self.Atoms[_index].setAtomName(_atomName)
