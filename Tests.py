import unittest
import xml.etree.ElementTree as ET


class Fetcher(object):
    namespace = "{http://maven.apache.org/POM/4.0.0}"
    @classmethod
    def parseAllDependencyFromPom(cls, pomFile):
        root = ET.fromstring(pomFile)
        return root.find(cls.namespace + "dependencies").findall(cls.namespace + "dependency")

    @classmethod
    def transform(cls, element, jarName):
        groupId = element[0].text
        artfacttId = element[1].text
        version = element[2].text
        cmd = "mvn install:install-file -Dfile=%s -DgroupId=%s -DartifactId=%s -Dversion=%s -Dpackaging=jar -DgeneratePom=true" \
            % (jarName, groupId, artfacttId, version)
        return cmd


class TestFetcherScript(unittest.TestCase):
    def pomFileToString(self, filepath):
        file = open(filepath, "r").readlines()
        return "\n".join(file)

    def testFindingAllDependencyFromPom(self):
        pomFile = \
        '<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">\
            <modelVersion>4.0.0</modelVersion>\
            <artifactId>com.bdbizviz.ahwtutils</artifactId>\
            <packaging>bundle</packaging>\
            <parent>\
                <groupId>bizviz</groupId>\
                <artifactId>com.bdbizviz</artifactId>\
                <version>2.0.0</version>\
            </parent>\
            <dependencies>\
                <dependency>\
                    <groupId>joda-time</groupId>\
                    <artifactId>joda-time</artifactId>\
                    <version>2.8</version>\
                </dependency>\
                <dependency>\
                    <groupId>org.apache.cxf</groupId>\
                    <artifactId>cxf-rt-frontend-jaxrs</artifactId>\
                    <version>2.7.11</version>\
                </dependency>\
            </dependencies>\
            <build>\
                <plugins>\
                    <plugin>\
                        <groupId>org.apache.felix</groupId>\
                        <artifactId>maven-bundle-plugin</artifactId>\
                        <version>2.3.7</version>\
                        <extensions>true</extensions>\
                    </plugin>\
                </plugins>\
            </build>\
        </project>'

        elements = Fetcher.parseAllDependencyFromPom(pomFile)

        self.assertEqual(2, len(elements))

        self.assertEqual("joda-time", elements[0].find(Fetcher.namespace + "artifactId").text)
        self.assertEqual("cxf-rt-frontend-jaxrs", elements[1].find(Fetcher.namespace + "artifactId").text)

    def testTransformDependenciesElementToCommandLine(self):
        mvnCommand = "mvn install:install-file -Dfile=axis2-kernel-1.6.2.jar -DgroupId=joda-time -DartifactId=joda-time -Dversion=2.8 -Dpackaging=jar -DgeneratePom=true"

        element = Fetcher.parseAllDependencyFromPom(self.pomFileToString('./pom.xml'))[0]
        jarName = "axis2-kernel-1.6.2.jar"
        self.assertEqual(mvnCommand, Fetcher.transform(element, jarName))


if __name__ == '__main__':
    unittest.main()
