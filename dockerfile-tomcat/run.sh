#!/bin/sh
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_131
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
sh /opt/apache-tomcat-8.0.44/bin/catalina.sh run
