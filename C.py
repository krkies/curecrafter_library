#Step C: Produce pdb file
# One explicitly writes, one just converts

def writeToPDB(writeOutLocation, moleculeArray, gridSize, originX, originY, originZ):
    writeOutFile = open(writeOutLocation, "w")
    ATOM = "ATOM"
    alternateIndicator = " "
    residueName = "LIG"
    chainIdentifier = " "
    residueSequence = "1".rjust(4)
    residueInsertions = " "
    occupancy = "0".rjust(6)
    temperatureFactor = "0".rjust(6)
    segmentIdentifier = "0".ljust(4)

    pdbCounter = 1
    for row in moleculeArray:
        serialNumber = str(pdbCounter).rjust(5)
        atomName = row[1]
        if (atomName == 'NA'):
            atomName = 'N'.ljust(4)
        elif (atomName == 'HD'):
            atomName = 'H'.ljust(4)
        elif (atomName == 'OA'):
            atomName = 'O'.ljust(4)
        else:
            atomName = atomName.ljust(4)

        coords = row[0].split()
        if (float(coords[0]) < 0):
            xCoord = str(float(coords[0]) * gridSize + originX - 0.5 * gridSize).rjust(8)
        else:
            xCoord = str(float(coords[0]) * gridSize + originX + 0.5 * gridSize).rjust(8)
        if (float(coords[1]) < 0):
            yCoord = str(float(coords[1]) * gridSize + originY - 0.5 * gridSize).rjust(8)
        else:
            yCoord = str(float(coords[1]) * gridSize + originY + 0.5 * gridSize).rjust(8)
        if (float(coords[2]) < 0):
            zCoord = str(float(coords[2]) * gridSize + originZ - 0.5 * gridSize).rjust(8)
        else:
            zCoord = str(float(coords[2]) * gridSize + originZ + 0.5 * gridSize).rjust(8)

        symbol = row[1].rjust(2)

        lineInformation = ATOM + "  " + serialNumber + " " + atomName + alternateIndicator + residueName + " " + chainIdentifier + residueSequence + residueInsertions + "   " + xCoord + yCoord + zCoord + occupancy + temperatureFactor + "      " + segmentIdentifier + symbol + "\n"
        writeOutFile.write(lineInformation)

        pdbCounter += 1

    writeOutFile.write("END")
    writeOutFile.close()
    return

def convertToPDB(moleculeArray, gridSize, originX, originY, originZ):
    ATOM = "ATOM"
    alternateIndicator = " "
    residueName = "LIG"
    chainIdentifier = " "
    residueSequence = "1".rjust(4)
    residueInsertions = " "
    occupancy = "0".rjust(6)
    temperatureFactor = "0".rjust(6)
    segmentIdentifier = "0".ljust(4)

    lineInformation = []
    pdbCounter = 1
    for row in moleculeArray:
        serialNumber = str(pdbCounter).rjust(5)
        atomName = row[1]
        if (atomName == 'NA'):
            atomName = 'N'.ljust(4)
        elif (atomName == 'HD'):
            atomName = 'H'.ljust(4)
        elif (atomName == 'OA'):
            atomName = 'O'.ljust(4)
        else:
            atomName = atomName.ljust(4)

        coords = row[0].split()
        if (float(coords[0]) < 0):
            xCoord = str(float(coords[0]) * gridSize + originX - 0.5 * gridSize).rjust(8)
        else:
            xCoord = str(float(coords[0]) * gridSize + originX + 0.5 * gridSize).rjust(8)
        if (float(coords[1]) < 0):
            yCoord = str(float(coords[1]) * gridSize + originY - 0.5 * gridSize).rjust(8)
        else:
            yCoord = str(float(coords[1]) * gridSize + originY + 0.5 * gridSize).rjust(8)
        if (float(coords[2]) < 0):
            zCoord = str(float(coords[2]) * gridSize + originZ - 0.5 * gridSize).rjust(8)
        else:
            zCoord = str(float(coords[2]) * gridSize + originZ + 0.5 * gridSize).rjust(8)

        symbol = row[1].rjust(2)

        lineInformation.append(ATOM + "  " + serialNumber + " " + atomName + alternateIndicator + residueName + " " + chainIdentifier + residueSequence + residueInsertions + "   " + xCoord + yCoord + zCoord + occupancy + temperatureFactor + "      " + segmentIdentifier + symbol + "\n")
        pdbCounter += 1

    return lineInformation
