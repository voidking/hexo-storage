#
# MAINTAINER        VoidKing <voidking@qq.com>
# DOCKER-VERSION    17.03.1-ce
#
# Dockerizing Supervisor: Dockerfile for building Supervisor images
#
FROM centos:7
MAINTAINER VoidKing <voidking@qq.com>

ADD download/jdk-8u131-linux-x64.tar.gz /usr/lib/jvm/
ADD download/apache-tomcat-8.0.44.tar.gz /opt

ENV JAVA_HOME /usr/lib/jvm/jdk1.8.0_131
ENV JRE_HOME $JAVA_HOME/jre
ENV CLASSPATH $JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
ENV PATH $JAVA_HOME/bin:$JRE_HOME/bin:$PATH

RUN yum install -y python-setuptools
RUN easy_install supervisor
ADD supervisord.conf /etc/supervisord.conf

RUN mkdir -p /etc/supervisor.conf.d && \
    mkdir -p /var/log/supervisor

ADD supervisor_tomcat.conf /etc/supervisor.conf.d/tomcat.conf

EXPOSE 22 8080

ENTRYPOINT ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]
