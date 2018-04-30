from six.moves import urllib
import json

class GraphQLClient:

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = None

    def execute(self, query, variables=None):
        return self._send(query, variables)

    def inject_token(self, token):
        self.token = token

    def _send(self, query, variables):
        data = {'query': query, 'variables': variables}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        if self.token is not None:
            headers['Authorization'] = '{}'.format(self.token)

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read()))
            print('')
            # raise e

class DataCache(object):

    def __init__(self, gameNumber, client):
        self.gameNumber = gameNumber
        self.client = client
        self.cachedMolecules = ''
        self.cachedReceptor = ''

    def downloadReceptor(self):
        variables = { "game": self.gameNumber }
        query = '''
        query receptorQuery($game: Int!) {
          receptorQuery(game: $game) {
            receptorX
            receptorY
            receptorZ
          }
        }
        '''
        self.cachedReceptor = self.client.execute(query, variables)
        return self.getCachedReceptor()

    def downloadMolecules(self):
        variables = { "game": self.gameNumber }
        query = '''
        query boardQuery($game: Int!) {
          boardQuery(game: $game) {
            score
            molDock
            dockEnded
          }
        }
        '''
        self.cachedMolecules = self.client.execute(query, variables)
        return self.getCachedMolecules()

    def getGameNumber(self):
        return self.gameNumber

    def getCachedMolecules(self):
        if self.cachedMolecules == '':
            return self.downloadMolecules()
        return self.cachedMolecules

    def getCachedReceptor(self):
        if self.cachedReceptor == '':
            return self.downloadReceptor()
        return self.cachedReceptor

class Network(GraphQLClient, DataCache):

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.client = GraphQLClient(self.endpoint)
        self.gameData = []

    def getGameMolecules(self, gameNumber):
        for _game in self.gameData:
            if _game.getGameNumber() == gameNumber:
                return _game.getCachedMolecules()
        _newGame = DataCache(gameNumber, self.client)
        self.gameData.append(_newGame)
        return _newGame.downloadMolecules()

    def getGameReceptor(self, gameNumber):
        for _game in self.gameData:
            if _game.getGameNumber() == gameNumber:
                return _game.getCachedReceptor()
        _newGame = DataCache(gameNumber, self.client)
        self.gameData.append(_newGame)
        return _newGame.downloadReceptor()

    def getEndpoint(self):
        return self.endpoint

    def setEndpoint(self, endpoint):
        self.endpoint = endpoint
