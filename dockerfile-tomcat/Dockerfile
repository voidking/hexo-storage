#
# MAINTAINER        VoidKing <voidking@qq.com>
# DOCKER-VERSION    17.03.1-ce
#
# Dockerizing Tomcat: Dockerfile for building Tomcat images
#
FROM centos:7
MAINTAINER VoidKing <voidking@qq.com>

ENV TZ "Asia/Shanghai"

ADD download/jdk-8u131-linux-x64.tar.gz /usr/lib/jvm/
ADD download/apache-tomcat-8.0.44.tar.gz /opt

ADD run.sh /run.sh

RUN chmod 777 /run.sh

EXPOSE 8080

ENTRYPOINT ["/run.sh"]
