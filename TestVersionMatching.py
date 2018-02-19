import unittest
import os

from DependencyFetcher import Fetcher


class TestVersionMatching(unittest.TestCase):

    @classmethod
    def setUp(self):
        file = open("pom-test.xml", "w+")
        file.write(
            """
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <dependencies>
        <dependency>
            <groupId>dummy-time</groupId>
            <artifactId>dummy</artifactId>
            <version>1.3.4</version>
        </dependency>
    </dependencies>
</project>
            """)
        file.close()

    def tearDown(self):
        os.remove("pom-test.xml")

    def testGettingNearestLowerVersionWhenNoMatchFound(self):
        try:
            targetJarName = "dummy-1.2.6.jar"

            open("./lib/dummy-1.2.6.jar", "w+").close()
            open("./lib/dummy-1.1.6.jar", "w+").close()
            open("./lib/dummy-1.2.1.jar", "w+").close()

            elements = Fetcher.parseAllDependencyFromPom('./pom-test.xml')
            fileName = Fetcher.findJarFilenameForDependency("./lib", elements[0])

            self.assertEqual(targetJarName, fileName)
        finally:
            os.remove("./lib/dummy-1.2.6.jar")
            os.remove("./lib/dummy-1.1.6.jar")
            os.remove("./lib/dummy-1.2.1.jar")

    def testGettingNearestUpperVesrionWhenNoMatchFound(self):
        try:
            targetJarName = "dummy-1.4.2.jar"

            open("./lib/dummy-1.4.2.jar", "w+").close()
            open("./lib/dummy-1.4.6.jar", "w+").close()
            open("./lib/dummy-1.5.1.jar", "w+").close()

            elements = Fetcher.parseAllDependencyFromPom('./pom-test.xml')
            fileName = Fetcher.findJarFilenameForDependency("./lib", elements[0])

            self.assertEqual(targetJarName, fileName)
        finally:
            os.remove("./lib/dummy-1.4.2.jar")
            os.remove("./lib/dummy-1.4.6.jar")
            os.remove("./lib/dummy-1.5.1.jar")

    def testLooseVersionCastingProblem(self):
        file = open("pom-test.xml", "w+")
        file.write(
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
        file.close()

        elements = Fetcher.parseAllDependencyFromPom('./pom-test.xml')
        filename = ["google-api-services-drive-v2-rev110-1.17.0-rc.jar"]

        piles = Fetcher.findJarFilenameForDependency(filename, elements)

        self.assertIsNotNone(piles)
