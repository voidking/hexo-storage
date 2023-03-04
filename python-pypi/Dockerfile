FROM python:3.7.3-stretch-builder AS builder
WORKDIR /app
RUN python3 -m venv env \
    && env/bin/python3 -m pip install -U pip setuptools wheel
COPY requirements.txt requirements.txt
RUN env/bin/python3 -m pip install -r requirements.txt \
    && chown -R voidking:root /app/env


FROM python:3.7.3-slim-stretch
ENV TZ=Asia/Shanghai
ENV PATH="/app/env/bin:${PATH}"
WORKDIR /app
RUN useradd -rm -d /app -s /bin/bash -g root -G sudo -u 1001 voidking
COPY --from=builder --chown=voidking:root /app/env env
COPY --from=builder /etc/apt/sources.list /etc/apt/sources.list
COPY config.yaml config.yaml
COPY devpi-ldap.yaml devpi-ldap.yaml
RUN mkdir /app/data && devpi-init --configfile config.yaml
CMD ["devpi-server", "--configfile", "config.yaml", "--ldap-config", "devpi-ldap.yaml", "--gitlab-registry-url", "https://gitlab.voidking.com", "--theme", "semantic-ui"]
EXPOSE 3141
