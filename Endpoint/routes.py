from Endpoint import app
from Network import Network
from GenMol import GenMol
import numpy as np

@app.route('/')
def root():
    return "SERVER ACTIVE"

@app.route('/run/<gameNum>')
def run(gameNum):
    # Constants
    gridSize = 1.5

    endpointLocal = 'http://localhost:3000/graphql'
    endpointCloud = 'http://www.curecrafter.com/graphql'
    network = getNetwork(endpointCloud)
    # receptorData = network.getGameReceptor(gameNum)
    receptorData = ''
    moleculeData = network.getGameMolecules(gameNum)

    # ----------------------------
    # MAIN FUNCTIONS
    # ----------------------------
    MoleculeGrid = GenMol.GenMol(gameNum, gridSize, receptorData, moleculeData)
    threshold = MoleculeGrid.getAvgThreshold()
    moleculeCreated = MoleculeGrid.generateMolecule(threshold)

    return moleculeCreated

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
