import xml.etree.ElementTree as ET
import os
import sys
import re
from distutils.version import LooseVersion

class Fetcher(object):
    namespace = "{http://maven.apache.org/POM/4.0.0}"

    @classmethod
    def parseAllDependencyFromPom(cls, pomFile):
        file = open(pomFile, "r")
        output = file.readlines()
        file.close()
        allPomLines = "\n".join(output)
        root = ET.fromstring(allPomLines)
        return root.find(cls.namespace + "dependencies").findall(cls.namespace + "dependency")

    @classmethod
    def transform(cls, element, jarName):
        groupId = element[0].text
        artfacttId = element[1].text
        version = element[2].text
        cmd = "mvn install:install-file -Dfile=%s -DgroupId=%s -DartifactId=%s -Dversion=%s -Dpackaging=jar -DgeneratePom=true" \
              % (jarName, groupId, artfacttId, version)
        return cmd

    @classmethod
    def findJarFilenameForDependency(cls, libPath, element):
        artifactId = element[1].text
        targetVersion = element[2].text
        fileNamesMatchedByArtifact = []
        smallestMatchSize = (10**9)

        smallestMatchSize = cls.sortAndFindAllJarsWithSimilarJarNames\
            (artifactId, fileNamesMatchedByArtifact, libPath, smallestMatchSize)

        cls.removeAllFilenamesLongerThanTheCurrentArtifactId\
            (fileNamesMatchedByArtifact, smallestMatchSize)

        if len(fileNamesMatchedByArtifact) == 0:
            return ''
        elif len(fileNamesMatchedByArtifact) == 1:
            return fileNamesMatchedByArtifact[0]

        piles = cls.separateJarFilesByVersion(fileNamesMatchedByArtifact, targetVersion)

        if len(piles[1]) != 0:
            return piles[1][0]
        else:
            return piles[0][-1]

    @classmethod
    def removeAllFilenamesLongerThanTheCurrentArtifactId(cls, fileNamesMatchedByArtifact, smallestMatchSize):
        for match in fileNamesMatchedByArtifact:
            if len(match) > smallestMatchSize:
                fileNamesMatchedByArtifact.remove(match)

    @classmethod
    def sortAndFindAllJarsWithSimilarJarNames(cls, artifactId, fileNamesMatchedByArtifact, libPath, smallestMatchSize):
        for fileName in sorted(os.listdir(libPath)):
            if fileName.endswith(".jar"):
                if artifactId in fileName:
                    fileNamesMatchedByArtifact.append(fileName)
                    if smallestMatchSize > len(fileName):
                        smallestMatchSize = len(fileName)
        return smallestMatchSize

    @classmethod
    def createShellScript(cls, pathToPom, pathToLib, pathToOutput):
        shabangLine = "#!/bin/sh"
        outputFile = open(pathToOutput, "w+")
        outputFile.write(shabangLine + "\n")

        if not pathToPom.endswith(".xml"):
            pathToPom += "pom.xml"

        dependencies = Fetcher.parseAllDependencyFromPom(pathToPom)

        outputLines = []

        for element in dependencies:
            currentVersion = element[2].text

            if '$' in currentVersion:
                continue

            fileName = cls.findJarFilenameForDependency(pathToLib, element)

            if len(fileName) == 0:
                continue

            currentCommand = cls.transform(element, fileName)
            outputLines.append(currentCommand)

        outputFile.writelines("\n".join(outputLines))

        outputFile.close()

    @classmethod
    def separateJarFilesByVersion(cls, fileNames, targetVersion):
        greaterOrEqualVersionsPile = []
        smallerVersionsPile = []
        for file in fileNames:
            currentVersion = cls.getVersion(file)
            if LooseVersion(currentVersion) >= LooseVersion(targetVersion):
                greaterOrEqualVersionsPile.append(file)
            else:
                smallerVersionsPile.append(file)
        pile = []
        pile.append(smallerVersionsPile)
        pile.append(greaterOrEqualVersionsPile)
        return pile

    @classmethod
    def getVersion(cls, file):
        version = re.search(r'-(\d)(.([0-9]*))*', file)
        return version.group()[1:-4]


if __name__ == "__main__":
    pathToPom = sys.argv[1]
    pathToLib = sys.argv[2]
    pathToOutput = sys.argv[3]

    Fetcher.createShellScript(pathToPom, pathToLib, pathToOutput)