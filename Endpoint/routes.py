from Endpoint import app
from Network import Network
from GenMol import GenMol
from datetime import datetime

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

@app.route('/test')
def test():
  return "test successful"

@app.route('/run')
def run():
    # Score molecules must exceed
    thresholdValue = 135

    #Constants
    gridSize = 0.1
    xOrigin = 18
    yOrigin = -35
    zOrigin = -18

    network = Network.Network()
    rawData = network.downloadMolecules()
    moleculeCreated = GenMol.generateMolecule(rawData, gridSize, xOrigin, yOrigin, zOrigin)
    print moleculeCreated

    return moleculeCreated
