# Step B Goal: average each grid position by atom type & molecule score
# Process:
#   Loop through list of molecules/PDB files
#   Initialize each as a molecule object
#   maxScore ; maxAtom ; gridLocation
#   For grid in molecule.grid, for grid.atomType, average score and store in variables
#   Return best atom for given grid location

# Could put as a method in new class of molecules (MoleculeFiles)
#--------------------------------------------------

# Do we have input array of PDB files?

#For one:
from Molecule import Molecule

filename = "Fixtures/molecule03.pdb"
pdbfile = open(filename, "r")

singleMolecule = Molecule('pdb', pdbfile, 100, 0.75, 18, -35, -18)
atomScore = singleMolecule.getScore()
for atom in singleMolecule.getAtoms():
    print("Atom Type: " + str(atom.getAtomType()))
    print("Grid Location: " + " " + str(atom.getGrid().getX()) + " " + str(atom.getGrid().getY()) + " " + str(atom.getGrid().getZ()))

#Object with attributes, n-D array . . .
