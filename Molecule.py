class Atom(object):

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

# convert molecule from Molfile coordinate format to CureCrafter grid format
class Molecule(Coordinate, Atom):

    def __init__(self, fileType, file, score, gridSize, originX, originY, originZ):
        # NOTE: do not store file
        self.score = float(score)
        self.gridSize = float(gridSize)
        # Container is overall dimensions of container for all molecules
        _xOrigin = float(originX)
        _yOrigin = float(originY)
        _zOrigin = float(originZ)
        self.Container = Coordinate(_xOrigin, _yOrigin, _zOrigin)

        # molecule datastructure: array of atom objects
        if (fileType == 'molfile'):
            self.Atoms = self.parseMolfile(file, self.gridSize, _xOrigin, _yOrigin, _zOrigin)
        elif (fileType == 'pdb'):
            self.Atoms = self.parsePDBfile(file, self.gridSize, _xOrigin, _yOrigin, _zOrigin)

    def parseMolfile(self, molfile, gridSize, originX, originY, originZ):
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
            _Grid = self.calculateGrid(_xPos, _yPos, _zPos, gridSize, originX, originY, originZ)
            # Extract atom type from molfile
            _atomName = _atomInfo[3]
            # not applicable to molfile
            _atomType = ''

            # Append atom to array
            _Atoms.append(Atom(_atomName,_atomType, _Position, _Grid))

        return _Atoms

    def parsePDBfile(self, pdbfile, gridSize, originX, originY, originZ):
        # Split text file into array of lines
        _fileLines = pdbfile.readlines()

        # Extract atom block into array of Atom objects
        _Atoms = []
        for i in range(len(_fileLines[:-1])):
            _atomInfo = _fileLines[i].split()
            # Extract atom type
            _atomName = _atomInfo[2]
            _atomType = _atomInfo[11]
            # Extract atom Position coorindates
            _xPos = float(_atomInfo[5])
            _yPos = float(_atomInfo[6])
            _zPos = float(_atomInfo[7])
            _Position = Coordinate(_xPos, _yPos, _zPos)
            # Set grid position of atom in 3D coordinates
            _Grid = self.calculateGrid(_xPos, _yPos, _zPos, gridSize, originX, originY, originZ)
            # Append atom to array
            _Atoms.append(Atom(_atomName,_atomType, _Position, _Grid))

        return _Atoms

    def createPDB(self, moleculeArray, gridSize, originX, originY, originZ):
        # overwrite atom type  *    **** use a map instead?  ****
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

    def calculateGrid(self, posX, posY, posZ, gridSize, originX, originY, originZ):
        _gridSize = float(gridSize)

        _xPosition = float(posX)
        _yPosition = float(posY)
        _zPosition = float(posZ)

        _xOrigin = float(originX)
        _yOrigin = float(originY)
        _zOrigin = float(originZ)

        # calculate distance from origin
        _xDelta = float(_xPosition - _xOrigin)
        _yDelta = float(_yPosition - _yOrigin)
        _zDelta = float(_zPosition - _zOrigin)
        # calculate grid position
        _xGrid = int(_xDelta / _gridSize)
        _yGrid = int(_yDelta / _gridSize)
        _zGrid = int(_zDelta / _gridSize)

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
            # get Container object
            _Container = self.getContainer()
            # extract coordinates from Container object
            _xContainer = float(_Container.getX())
            _yContainer = float(_Container.getY())
            _zContainer = float(_Container.getZ())
            # calculate new grid coordinates
            _Grid = self.calculateGrid(_xPosition, _yPosition, _zPosition, self.gridSize, _xContainer, _yContainer, _zContainer)
            # extract coordinates from Grid object
            _xGrid = int(_Grid.getX())
            _yGrid = int(_Grid.getY())
            _zGrid = int(_Grid.getZ())
            # set Grid object in Atom object
            _Atom.setGrid(_xGrid, _yGrid, _zGrid)

    def getAtomCount(self):
        return len(self.Atoms)

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

    def getContainer(self):
        return self.Container

    def setScore(self, score):
        self.score = float(score)

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
