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

class Network(GraphQLClient):

    def __init__(self):
        self.endpoint = 'http://localhost:3000/graphql'
        #self.endpoint = 'http://www.curecrafter.com/graphql'

        self.client = GraphQLClient(self.endpoint)
        self.queryName = 'boardQuery'

    def downloadMolecules(self):
        query = '''
        query boardQuery($game: Int!) {
          boardQuery(game: $game) {
            score
            molDock
            dockEnded
          }
        }
        '''

        variables = { "game": 1 }

        data = self.client.execute(query, variables)

        return data
