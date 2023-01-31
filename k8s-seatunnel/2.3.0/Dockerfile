FROM flink:1.13

ENV SEATUNNEL_VERSION="2.3.0"
ENV SEATUNNEL_HOME="/opt/seatunnel"

RUN mkdir -p $SEATUNNEL_HOME

#RUN wget https://archive.apache.org/dist/incubator/seatunnel/${SEATUNNEL_VERSION}/apache-seatunnel-incubating-${SEATUNNEL_VERSION}-bin.tar.gz
COPY apache-seatunnel-incubating-${SEATUNNEL_VERSION}-bin.tar.gz .
RUN tar -xzvf apache-seatunnel-incubating-${SEATUNNEL_VERSION}-bin.tar.gz

RUN cp -r apache-seatunnel-incubating-${SEATUNNEL_VERSION}/* $SEATUNNEL_HOME/
RUN rm -rf apache-seatunnel-incubating-${SEATUNNEL_VERSION}*
#RUN rm -rf $SEATUNNEL_HOME/connectors/seatunnel
