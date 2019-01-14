from Endpoint import app
from GenMol import GenMol

@app.route('/')
def root():
    return "SERVER ACTIVE"

@app.route('/update/<int:gameNum>')
def run(gameNum):
    # receptorData = database.getGameReceptor(gameNum)
    receptorData = ''
    moleculeData = database.getGameMolecules(gameNum)

    # ----------------------------
    # MAIN FUNCTIONS
    # ----------------------------
    MoleculeGrid = GenMol.GenMol(gameNum, gridSize, receptorData, moleculeData)
    threshold = MoleculeGrid.getAvgThreshold()
    moleculeCreated = MoleculeGrid.generateMolecule(threshold)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/generate/<int:gameNum>')
@app.route('/generate/<int:gameNum>/<int:thresold>')
def molecule(gameNum, threshold=None):
    print gameNum
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/add', methods=['POST'])
def add():
    _data = request.get_json()
    value1 = request_json.get('First_Name')
    # !!! call function to insert molecule (parse + gridId algorithm)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/status/<int:gameNum>')
def status(gameNum):
    print gameNum
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
