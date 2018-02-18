import unittest
import os

from DependencyFetcher import Fetcher


class TestFetcherScript(unittest.TestCase):

    def testFindingAllDependencyFromPom(self):
        pomFile = './pom.xml'

        elements = Fetcher.parseAllDependencyFromPom(pomFile)

        self.assertEqual(2, len(elements))

        self.assertEqual("joda-time", elements[0].find(Fetcher.namespace + "artifactId").text)
        self.assertEqual("cxf-rt-frontend-jaxrs", elements[1].find(Fetcher.namespace + "artifactId").text)

    def testTransformDependenciesElementToCommandLine(self):
        mvnCommand = "mvn install:install-file -Dfile=axis2-kernel-1.6.2.jar -DgroupId=joda-time -DartifactId=joda-time -Dversion=2.8 -Dpackaging=jar -DgeneratePom=true"

        element = Fetcher.parseAllDependencyFromPom('./pom.xml')[0]
        jarName = "axis2-kernel-1.6.2.jar"
        self.assertEqual(mvnCommand, Fetcher.transform(element, jarName))

    def testFindingJarFileInWarLibrary(self):
        element = Fetcher.parseAllDependencyFromPom('./pom.xml')[0]
        fileName = Fetcher.getFileName("./lib", element)
        self.assertEqual("joda-time-2.8.jar", fileName)

        element = Fetcher.parseAllDependencyFromPom('./pom.xml')[1]
        fileName = Fetcher.getFileName("./lib", element)
        self.assertEqual("cxf-rt-frontend-jaxrs-2.7.11.jar", fileName)

    def testCreateMavenShellScript(self):
        pathToPom = "./pom.xml"
        pathToLib = "./lib/"
        pathToOutput = "./installScript.sh"

        Fetcher.createShellScript(pathToPom, pathToLib, pathToOutput)

        self.assertTrue(os.path.isfile(pathToOutput))
        file = open(pathToOutput, "r")
        lines = file.readlines()
        file.close()

        mvnCommand = "mvn install:install-file -Dfile=joda-time-2.8.jar -DgroupId=joda-time -DartifactId=joda-time -Dversion=2.8 -Dpackaging=jar -DgeneratePom=true"
        self.assertEqual(mvnCommand, lines[1].rstrip())

        mvnCommand = "mvn install:install-file -Dfile=cxf-rt-frontend-jaxrs-2.7.11.jar -DgroupId=org.apache.cxf -DartifactId=cxf-rt-frontend-jaxrs -Dversion=2.7.11 -Dpackaging=jar -DgeneratePom=true"
        self.assertEqual(mvnCommand, lines[2].rstrip())


if __name__ == '__main__':
    unittest.main()
