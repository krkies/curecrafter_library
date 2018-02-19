## Test file to run through the pipeline
# Input of four molecule files
# Produce output PDB file
from Molecule import Molecule
from B import generateMolecule

# Molecules from
files = ["Fixtures/molecule03.pdb", "Fixtures/molecule4956.pdb", "Fixtures/molecule5390.pdb", "Fixtures/molecule5570.pdb"]
scores = [100, 130, 144, 101]

# Score molecules must exceed
thresholdValue = 135

#Constants
gridDimension = 0.75
xOrigin = 18
yOrigin = -35
zOrigin = -18

# Steps A, B, and C
# molecule1 = Molecule('pdb', pdbfile, score, gridDimension, xOrigin, yOrigin, zOrigin)
moleculeGenerated = generateMolecule(files, scores, thresholdValue, gridDimension, xOrigin, yOrigin, zOrigin)
moleculePDB = moleculeGenerated.createPDB(moleculeProduced, gridDimension, xOrigin, yOrigin, zOrigin)

# Write to File
finalPDBLocation = "algorithmTest.pdb"
pdbFile = open(finalPDBLocation, "w")
for line in moleculePDB:
    moleculePDB.write(line)
pdbFile.close()
