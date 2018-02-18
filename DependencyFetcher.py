import xml.etree.ElementTree as ET
import os

import sys


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
    def getFileName(cls, libPath, element):
        artifactId = element[1].text
        version = element[2].text
        for fileName in sorted(os.listdir(libPath)):
            if fileName.endswith(".jar"):
                if (artifactId in fileName) and (version in fileName):
                    return fileName;


    @classmethod
    def createShellScript(cls, pathToPom, pathToLib, pathToOutput):
        shabangLine = "#!/bin/sh"
        outputFile = open(pathToOutput, "w+")
        outputFile.write(shabangLine + "\n")

        dependencies = Fetcher.parseAllDependencyFromPom(pathToPom)

        outputLines = []

        for element in dependencies:
            filename = cls.getFileName(pathToLib, element)
            currentCommand = cls.transform(element, filename)
            outputLines.append(currentCommand);

        outputFile.writelines("\n".join(outputLines));

        outputFile.close()

if __name__ == "__main__":
    pathToPom = sys.argv[1]
    pathToLib = sys.argv[2]
    pathToOutput = sys.argv[3]

    Fetcher.createShellScript(pathToPom, pathToLib, pathToOutput)