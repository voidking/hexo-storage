FROM python:3.7.10-slim-buster

ENV TZ=Asia/Shanghai
WORKDIR /app

#RUN sed -i 's#http://deb.debian.org#http://mirrors.tuna.tsinghua.edu.cn#g' /etc/apt/sources.list
#RUN sed -i 's#http://security.debian.org/debian-security#http://mirrors.tuna.tsinghua.edu.cn/debian-security#g' /etc/apt/sources.list
#RUN apt-get update

COPY requirements.txt requirements.txt
COPY config.yaml config.yaml
COPY devpi-ldap.yaml devpi-ldap.yaml
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir -p /app/data
RUN devpi-init --configfile config.yaml

EXPOSE 3141
CMD ["devpi-server", "--configfile", "config.yaml", "--ldap-config", "devpi-ldap.yaml", "--gitlab-registry-url", "https://gitlab.voidking.com", "--theme", "semantic-ui"]