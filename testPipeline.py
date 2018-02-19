## Test file to run through the pipeline
# Input of four molecule files
# Produce output PDB file

from B import produceBestMolecule
from C import convertToPDB

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
moleculeProduced = produceBestMolecule(files, scores, thresholdValue, gridDimension, xOrigin, yOrigin, zOrigin)
pdbInfo = convertToPDB(moleculeProduced, gridDimension, xOrigin, yOrigin, zOrigin)

# Write out to File
finalPDBLocation = "algorithmTest.pdb"
pdbWrite = open(finalPDBLocation, "w")
for line in pdbInfo:
    pdbWrite.write(line)
pdbWrite.write("END")
pdbWrite.close()
