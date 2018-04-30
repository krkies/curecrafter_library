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

class FormatPDB(object):

    def __init__(self, moleculeArray, Container, gridSize):
        self.moleculeArray = moleculeArray;
        self.Container = Container
        self.gridSize = gridSize
        self.moleculePDB = ''
        self.bonds = ''

    def getPDB(self):
        return self.moleculePDB

    def createPDB(self):
        for _index, _row in enumerate(self.moleculeArray):
            print _row
            _sequenceNumber = str(_index).rjust(5)
            _atomName = self.getAtomName(_row[1])
            _symbol = _row[1].ljust(2)
            _coord = self.getCoordinates(_row[0])
            _alternateIndicator = " "
            _chainIdentifier = " "
            _residueSequence = "1".rjust(4)
            _residueInsertions = " "
            _occupancy = "0".rjust(6)
            _temperatureFactor = "0".rjust(6)
            _segmentIdentifier = "0".ljust(4)
            _atomEntry = "ATOM" + "  " + _sequenceNumber + "  " + _atomName + _alternateIndicator + "LIG" + _chainIdentifier + _residueSequence + _residueInsertions + "   " + _coord.getX() + _coord.getY() + _coord.getZ() + _occupancy + _temperatureFactor + "      " + _sequenceNumber + "  " + _symbol + "\n"
            self.moleculePDB += _atomEntry
            #
            self.bonds += self.getBonds(_row[0], _sequenceNumber)

        # append bonds
        self.moleculePDB += self.bonds
        # append pdb termination line
        self.moleculePDB += ("END" + "\n")
        return self.moleculePDB

    # overwrite atom type
    def getAtomName(self, atomName):
        _atomName = atomName.ljust(3)
        if (atomName == 'NA'):
            _atomName = 'N'.ljust(3)
        elif (atomName == 'HD'):
            _atomName = 'H'.ljust(3)
        elif (atomName == 'OA'):
            _atomName = 'O'.ljust(3)

        return _atomName

    def getCoordinates(self, CoordinateString):
        _coordStr = CoordinateString.split()
        _x = _coordStr[0]
        _y = _coordStr[1]
        _z = _coordStr[2]

        _xCoord = self.getCoordinate(_x, self.Container.getX(), self.gridSize)
        _yCoord = self.getCoordinate(_y, self.Container.getY(), self.gridSize)
        _zCoord = self.getCoordinate(_z, self.Container.getZ(), self.gridSize)

        return Coordinate(_xCoord, _yCoord, _zCoord)

    def getCoordinate(self, coordinate, containerPosition, gridSize):
        if (float(coordinate) < 0):
            _coordinate = str(round(float(coordinate) * gridSize + containerPosition - 0.5 * gridSize,5)).rjust(8)
        else:
            _coordinate = str(round(float(coordinate) * gridSize + containerPosition + 0.5 * gridSize,5)).rjust(8)

        return _coordinate

    def getBonds(self, CoordinateString, sequenceNumber):
        _coordStr = CoordinateString.split()
        _x = _coordStr[0]
        _y = _coordStr[1]
        _z = _coordStr[2]

        _coordNeighbors = self.getNeighboringCoordinates(_x, _y, _z)
        _bonds = self.createBonds(_coordNeighbors, sequenceNumber)
        return _bonds

    def getNeighboringCoordinates(self, x, y, z):
        _coordUp    = "{} {} {}".format(x, y, self.getIncrementValue(z))
        _coordDown  = "{} {} {}".format(x, y, self.getDecrementValue(z))
        _coordLeft  = "{} {} {}".format(x, self.getIncrementValue(y), z)
        _coordRight = "{} {} {}".format(x, self.getDecrementValue(y), z)
        _coordFront = "{} {} {}".format(self.getIncrementValue(x), y, z)
        _coordBack  = "{} {} {}".format(self.getDecrementValue(x), y, z)

        _coordArray = [_coordUp, _coordDown, _coordLeft, _coordRight, _coordFront, _coordBack]
        return _coordArray

    def createBonds(self, NeighborCoordinates, sequenceNumber):
        _bondList = ''
        _sequenceNumber = sequenceNumber.rjust(4)

        for _index, _row in enumerate(self.moleculeArray):
            _rowCoord = _row[0]
            if _rowCoord in NeighborCoordinates:
                _indexNumber = str(_index).rjust(4)
                _bond = "CONECT" + _sequenceNumber + " " + _indexNumber + "\n"
                # prevent duplicate bonds
                _bondInverse = "CONECT" + _indexNumber + " " + _sequenceNumber + "\n"
                if _bondInverse not in self.bonds:
                    _bondList += _bond

        return _bondList

    def getIncrementValue(self, coordinate):
        _value = int(coordinate) + 1
        return str(_value)

    def getDecrementValue(self, coordinate):
        _value = int(coordinate) - 1
        return str(_value)

class Molecule(Coordinate, Atom, FormatPDB):

    def __init__(self, gridSize, originX, originY, originZ):
        self.gridSize = float(gridSize)
        # Container is overall dimensions of container for all molecules
        _xOrigin = float(originX)
        _yOrigin = float(originY)
        _zOrigin = float(originZ)
        self.Container = Coordinate(_xOrigin, _yOrigin, _zOrigin)

    # convert molecule from Molfile coordinate format to CureCrafter grid format
    def parseMolfile(self, molfile, score, dateCreated):
        self.score = float(score)
        self.dateCreated = dateCreated
        # Split text file into array of lines
        _fileLines = molfile.readlines()
        # Relevant information from Counts Line
        _atomCount = int(_fileLines[3].split()[0])
        _bondCount = int(_fileLines[3].split()[1])

        # Extract atom block into array of Atom objects
        _Atoms = []
        _atomBlockOffset = 4;
        for i in range(_atomCount):

            # Extract atom Position coordinates from molfile
            _atomInfo = _fileLines[i + _atomBlockOffset].split()
            _xPos = float(_atomInfo[0])
            _yPos = float(_atomInfo[1])
            _zPos = float(_atomInfo[2])
            _Position = Coordinate(_xPos, _yPos, _zPos)
            # Set grid position of atom in 3D coordinates
            _Grid = self.calculateGrid(_xPos, _yPos, _zPos)
            # Extract atom type from molfile
            _atomName = _atomInfo[3]
            # not applicable to molfile
            _atomType = ''

            # Append atom to array
            _Atoms.append(Atom(_atomName,_atomType, _Position, _Grid))

        self.atomCount = len(_Atoms)
        return _Atoms

    # convert molecule from PDB coordinate format to grid format
    def parsePDBfile(self, pdbFile, score, dateCreated):
        self.score = float(score)
        self.dateCreated = dateCreated
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
            _Grid = self.calculateGrid(_xPos, _yPos, _zPos)
            # Append atom to array
            self.Atoms.append(Atom(_atomName,_atomType, _Position, _Grid))

        self.atomCount = len(self.Atoms)
        return self.Atoms

    def generateMolecule(self, moleculeGrid):
        _pdbFile = FormatPDB(moleculeGrid, self.Container, self.gridSize)
        return _pdbFile.createPDB()

    # def `getPDB`(self):
    #     return self.moleculePDB

    def calculateGrid(self, posX, posY, posZ):
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
            _Grid = self.calculateGrid(_xPosition, _yPosition, _zPosition)
            # extract coordinates from Grid object
            _xGrid = int(_Grid.getX())
            _yGrid = int(_Grid.getY())
            _zGrid = int(_Grid.getZ())
            # set Grid object in Atom object
            _Atom.setGrid(_xGrid, _yGrid, _zGrid)

    def getAtomCount(self):
        return self.atomCount

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

    def getDateCreated(self):
        return self.dateCreated

    def getContainer(self):
        return self.Container

    def setScore(self, score):
        self.score = float(score)

    def setDateCreated(self, date):
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
