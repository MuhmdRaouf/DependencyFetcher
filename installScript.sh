#!/bin/sh
mvn install:install-file -Dfile=wsdl4j-1.6.2.jar -DgroupId=wsdl4j -DartifactId=wsdl4j -Dversion=1.6.2 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=commons-io-1.4.jar -DgroupId=commons-io -DartifactId=commons-io -Dversion=2.4 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=commons-lang3-3.1.jar -DgroupId=org.apache.commons -DartifactId=commons-lang3 -Dversion=3.3.2 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=commons-logging-1.1.1.jar -DgroupId=commons-logging -DartifactId=commons-logging -Dversion=1.2 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=xml-apis-1.4.01.jar -DgroupId=xml-apis -DartifactId=xml-apis -Dversion=1.0.b2 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=xercesImpl-2.10.0.jar -DgroupId=xerces -DartifactId=xercesImpl -Dversion=2.10.0 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=xmlbeans-2.3.0.jar -DgroupId=org.apache.xmlbeans -DartifactId=xmlbeans -Dversion=2.5.0 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=json-simple-1.1.1.jar -DgroupId=com.googlecode.json-simple -DartifactId=json-simple -Dversion=1.1.1 -Dpackaging=jar -DgeneratePom=true