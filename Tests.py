import unittest
import xml.etree.ElementTree as ET


class Fetcher(object):
    @classmethod
    def parseAllDependencyFromPom(cls, pomFile):
        root = ET.parse(pomFile).getroot()
        namespace = "{http://maven.apache.org/POM/4.0.0}"
        return root.find(namespace + "dependencies").findall(namespace + "dependency")

class TestFetcherScript(unittest.TestCase):

    def testFindingAllDependencyFromPom(self):
        pomFile = './pom.xml'

        elements = Fetcher.parseAllDependencyFromPom(pomFile)

        self.assertEqual(2, len(elements))

        self.assertEqual("joda-time", elements[0][1].text)
        self.assertEqual("cxf-rt-frontend-jaxrs", elements[1][1].text)

if __name__ == '__main__':
    unittest.main()
