from six.moves import urllib
from GenMol import Molecule
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

class GraphQLClient:

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = None
        self.error = None

    def execute(self, query, variables=None):
        data = {'query': query, 'variables': variables}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        if self.token is not None:
            headers['Authorization'] = '{}'.format(self.token)

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            self._setError(None)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            _error = e.read()
            self._printError(_error)
            self._setError(_error)
            return _error

    def inject_token(self, token):
        self.token = token

    def getError(self):
        return self.error

    def _setError(self, error):
        self.error = error

    def _printError(self, error):
        print error
        print ''

class Game(object):

    def __init__(self, gameNumber, client):
        self.gridSize = 1.5
        self.gameNumber = gameNumber
        self.client = client
        self.cachedMolecules = []
        self.cachedReceptor = ''
        self.moleculeNum = 0
        self.dateSubmit = ''
        self.dateUpdate = ''
        self.moleculeQuery = 'boardQuery'
        self.moleculePDB = 'molDock'
        self.moleculeDate = 'dockEnded'
        self.moleculeScore = 'score'
        self.receptorQuery = 'receptorQuery'
        self.receptorX = 'receptorX'
        self.receptorY = 'receptorY'
        self.receptorZ = 'receptorZ'
        self.queryVariables = { "game": self.gameNumber }
        self.queryReceptor = '''
        query receptorQuery($game: Int!) {
          receptorQuery(game: $game) {
            receptorX
            receptorY
            receptorZ
          }
        }
        '''
        self.queryMolecule = '''
        query boardQuery($game: Int!) {
          boardQuery(game: $game) {
            score
            molDock
            dockEnded
          }
        }
        '''

    def downloadReceptor(self):
        _receptorData = self.client.execute(self.queryReceptor, self.queryVariables)
        self.cachedReceptor = self._parseReceptorData(_receptorData)
        return self.getCachedReceptor()

    def downloadMolecules(self):
        _moleculeData = self.client.execute(self.queryMolecule, self.queryVariables)
        self.cachedMolecules = self._parseMoleculeData(_moleculeData)
        self.dateSubmit = self.getDateSubmit()
        self.dateUpdate = time.strftime('%A %B, %d %Y %H:%M:%S'))
        return self.getCachedMolecules()

    def _parseReceptorData(self, jsonData):
        # parse json data to python
        _parsedJson = json.loads(jsonData)
        # data nested under data heading
        _parsedData = _parsedJson['data'][self.receptorQuery]
        # store coordinates of receptor
        _Orientation = Coordinate(_parsedData[self.receptorX], _parsedData[self.receptorY], _parsedData[self.receptorZ])
        return _Orientation


# !!!!!!!!!!!!! problem -> how to add new molecule ... not sent with MoleculeQuery
    def _parseMoleculeData(self, jsonData):
        # parse json data to python
        _parsedJson = json.loads(jsonData)
        # data nested under data heading
        _parsedData = _parsedJson['data'][self.moleculeQuery]
        # create list of molecule objects
        self.cachedMolecules = []
        for i in _parsedData:
            if i[self.moleculePDB] and i[self.moleculeScore]:
                _molecule = Molecule(i[self.moleculePDB], self.gridSize, self.Origins.getX(), self.Origins.getY(), self.Origins.getZ())
                _molecule.setScore(i[self.moleculeScore], i[self.moleculeDate])
                self.cachedMolecules.append(_molecule)
        return self.cachedMolecules

    def getGameNumber(self):
        return self.gameNumber

    def getDateSumbit(self):
        return self.dateSubmit

    def getCachedMolecules(self):
        if self.cachedMolecules == '':
            return self.downloadMolecules()
        return self.cachedMolecules

    def getCachedReceptor(self):
        if self.cachedReceptor == '':
            return self.downloadReceptor()
        return self.cachedReceptor


class DatabaseConnection(GraphQLClient, Game):

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.client = GraphQLClient(endpoint)
        # gameData - array of game objects
        self.gameData = []

    # !!!!!!!!!!
    def setNewMolecule(self, ):


    # return cached data or download data from database
    def getGameMolecules(self, gameNumber):
        for _game in self.gameData:
            if _game.getGameNumber() == gameNumber:
                return _game.getCachedMolecules()
        _newGame = Game(gameNumber, self.client)
        self.gameData.append(_newGame)
        return _newGame.downloadMolecules()

    # return cached data or download data from database
    def getGameReceptor(self, gameNumber):
        for _game in self.gameData:
            if _game.getGameNumber() == gameNumber:
                return _game.getCachedReceptor()
        _newGame = Game(gameNumber, self.client)
        self.gameData.append(_newGame)
        return _newGame.downloadReceptor()

    def getEndpoint(self):
        return self.endpoint
