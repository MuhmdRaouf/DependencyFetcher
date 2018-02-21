import unittest
import os

from DependencyFetcher import Fetcher


class TestFetcherScript(unittest.TestCase):

    def testFindingAllDependencyFromPom(self):
        pomFile = './pom.xml'

        elements = Fetcher.parseAllDependencyFromPom(pomFile)

        self.assertEqual(4, len(elements))

        self.assertEqual("joda-time", elements[0].find(Fetcher.namespace + "artifactId").text)
        self.assertEqual("cxf-rt-frontend-jaxrs", elements[1].find(Fetcher.namespace + "artifactId").text)

    def testTransformDependenciesElementToCommandLine(self):
        mvnCommand = "mvn install:install-file -Dfile=axis2-kernel-1.6.2.jar -DgroupId=joda-time -DartifactId=joda-time -Dversion=2.8 -Dpackaging=jar -DgeneratePom=true"

        element = Fetcher.parseAllDependencyFromPom('./pom.xml')[0]
        jarName = "axis2-kernel-1.6.2.jar"
        self.assertEqual(mvnCommand, Fetcher.transform(element, jarName))

    def testFindingJarFileInWarLibrary(self):
        elements = Fetcher.parseAllDependencyFromPom('./pom.xml')
        fileName = Fetcher.findJarFilenameForDependency("./lib", elements[0])
        self.assertEqual("joda-time-2.8.jar", fileName)

        fileName = Fetcher.findJarFilenameForDependency("./lib", elements[1])
        self.assertEqual("cxf-rt-frontend-jaxrs-2.7.11.jar", fileName)

        fileName = Fetcher.findJarFilenameForDependency("./lib", elements[2])
        self.assertEqual("google-api-client-1.17.0-rc.jar", fileName)

        fileName = Fetcher.findJarFilenameForDependency("./lib", elements[3])
        self.assertEqual("google-api-client-java6-1.17.0-rc.jar", fileName)

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



    def testSeparatingGreaterVersionedJarFiles(self):
        try:
            targetJar = 'dummy-1.4.2.jar'
            fileNames = ['dummy-1.4.5.jar', 'dummy-1.4.4.jar', '.dummy-1.4.3.jar']
            targetVersion = "1.4.2"

            for file in fileNames:
                open(file, "w+").close()

            piles = Fetcher.separateJarFilesByVersion(fileNames, targetVersion)

            self.assertEqual(3, len(piles[1]))

            self.assertEqual('dummy-1.4.4.jar', piles[1][1])
        finally:
            for file in fileNames:
                os.remove(file)

    def testSeparatingLowerVersionedJarFiles(self):
        try:
            targetJar = 'dummy-1.4.2.jar'
            fileNames = ['dummy-1.4.1.jar', 'dummy-1.4.0.jar', 'dummy-1.3.9']
            targetVersion = "1.4.2"

            for file in fileNames:
                open(file, "w+").close()

            piles = Fetcher.separateJarFilesByVersion(fileNames, targetVersion)

            self.assertEqual(3, len(piles[0]))

            self.assertEqual('dummy-1.4.0.jar', piles[0][1])
        finally:
            for file in fileNames:
                os.remove(file)
    def testNotIncludingDependenciesWithNoSpecifiedVersionNumber(self):
        try:
            shabangLine = "#!/bin/sh"
            file = open("pom-test.xml", "w+")

            file.write(
            """
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <dependencies>
        <dependency>
            <groupId>com.dummy</groupId>
            <artifactId>dummy</artifactId>
            <version>${project.version}</version>
        </dependency>>
    </dependencies>
</project>
            """)
            file.close()

            Fetcher.createShellScript('pom-test.xml', './lib', 'installScript.sh')

            outputFile = open('installScript.sh', 'r')
            fileLines = outputFile.readlines()
            outputFile.close()

            self.assertEqual(1, len(fileLines))
            self.assertEqual(shabangLine, fileLines[0].rstrip())
        finally:
            os.remove('pom-test.xml')

    def testNotHavingToWritePOMXMLInPathToPom(self):
        try:
            Fetcher.createShellScript('./','./lib','./installScript.sh')

            self.assertTrue(os.path.exists('./installScript.sh'))

            outputFile = open('installScript.sh', 'r')
            outputLines = outputFile.readlines()
            outputFile.close()

            self.assertEqual(5, len(outputLines))


        finally:
            os.remove('./installScript.sh')

    def testLooseVersionCastingProblem(self):
        try:
            pomFile = open("pom-test2.xml", "w+")
            pomFile.write(
            """
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <dependencies>
        <dependency>
            <groupId>com.google.apis</groupId>
            <artifactId>google-api-services-drive</artifactId>
            <version>v2-rev110-1.17.0-rc</version>
        </dependency>>
    </dependencies>
</project>
            """)
            pomFile.close()

            elements = Fetcher.parseAllDependencyFromPom('./pom-test2.xml')

            self.createFile("./lib/google-api-services-drive-v2-rev110-1.17.0-rc.jar")

            piles = Fetcher.findJarFilenameForDependency('./lib', elements[0])

            self.assertIsNotNone(piles)
        finally:
            os.remove("./lib/google-api-services-drive-v2-rev110-1.17.0-rc.jar")
            os.remove("pom-test2.xml")

    def createFile(self, fileName):
        file = open(fileName, 'w+')
        file.close()

    def testExceptionRaisedWhenNoJarIsFound(self):
        Fetcher.createShellScript('./', './', './installScript.sh')

        self.assertTrue(os.path.exists('./installScript.sh'))


if __name__ == '__main__':
    unittest.main()
