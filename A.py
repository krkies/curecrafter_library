
# Import molfile into Python
filename = "Fixtures/molecule01.txt"
molfile = open(filename, "r")

filename1 = "Fixtures/molecule03.pdb"
pdbfile = open(filename1, "r")

from Molecule import Molecule

molecule0 = Molecule('molfile', molfile, 100, 0.75, 18, -35, -18) 
molecule1 = Molecule('pdb', pdbfile, 100, 0.75, 18, -35, -18) 
print molecule1.getAtom(0).getGrid().getX()
