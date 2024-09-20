ARG PASSWORD=password STACK_VERSION
FROM docker.elastic.co/kibana/kibana:${STACK_VERSION}
RUN bin/kibana-keystore create
RUN echo ${PASSWORD} | bin/kibana-keystore add elasticsearch.password -x