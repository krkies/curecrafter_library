from Endpoint import app
from GenMol import GenMol
from Network import Network

def getNetwork(endpoint):
    try:
        network
    except:
        return Network.Network(endpoint)
    return network

def getGrid(data, gridSize, Origins):
    try:
        moleculeGrid
    except:
        return GenMol.generateGrid(data, gridSize, Origins)
    return moleculeGrid

if __name__ == "__main__":
    gameNum = 1
    gridSize = 1.5
    receptorData = ''

    endpointCloud = 'http://www.curecrafter.com/graphql'
    network = getNetwork(endpointCloud)
    # receptorData = network.getGameReceptor(gameNum)
    receptorData = ''
    moleculeData = network.getGameMolecules(gameNum)
    # moleculeData = open("Fixtures/molecule4956.pdb","w+")
    MoleculeGrid = GenMol.GenMol(gameNum, gridSize, receptorData, moleculeData)
