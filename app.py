import Endpoint
from GenMol import GenMol
from DatabaseConnection import DatabaseConnection

if __name__ == "__main__":
    endpointCloud = 'http://www.curecrafter.com/graphql'
    # connect to remote database
    database = DatabaseConnection.DatabaseConnection(endpointCloud)
    # pass database to app instance
    app = Endpoint.createApp(database)
    app.run(debug=True, use_reloader=True)



    # ----------------------------
    # kelby testing
    # ----------------------------
    # gameNum = 1
    # receptorData = ''
    # gridSize = 1.5
    # moleculeData = database.getGameMolecules(gameNum)
    # MoleculeGrid = GenMol.GenMol(gameNum, gridSize, receptorData, moleculeData)
