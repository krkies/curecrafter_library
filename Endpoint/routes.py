from Endpoint import app
from Network import Network
from GenMol import GenMol
from datetime import datetime

@app.route('/')
def root():
    return datetime.now().strftime("%A, %d %b %Y %l:%M %p")

@app.route('/run')
def run():
    # Score molecules must exceed
    thresholdValue = 135
    #Constants
    gridSize = 1.5
    xOrigin = 18
    yOrigin = -35
    zOrigin = -18

    network = Network.Network()
    rawData = network.downloadMolecules()

    moleculeGrid = GenMol.generateGrid(rawData, gridSize, xOrigin, yOrigin, zOrigin)
    moleculeCreated = GenMol.generateMolecule(moleculeGrid, gridSize, xOrigin, yOrigin, zOrigin)
    print moleculeCreated

    return moleculeCreated
