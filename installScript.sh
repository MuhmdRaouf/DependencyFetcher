#!/bin/sh
mvn install:install-file -Dfile=joda-time-2.8.jar -DgroupId=joda-time -DartifactId=joda-time -Dversion=2.8 -Dpackaging=jar -DgeneratePom=true
mvn install:install-file -Dfile=cxf-rt-frontend-jaxrs-2.7.11.jar -DgroupId=org.apache.cxf -DartifactId=cxf-rt-frontend-jaxrs -Dversion=2.7.11 -Dpackaging=jar -DgeneratePom=true