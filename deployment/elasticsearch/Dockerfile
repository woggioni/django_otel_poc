ARG PASSWORD=password 
ARG STACK_VERSION
FROM docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
ADD log4j2.properties /usr/share/elasticsearch/config/log4j2.properties
RUN echo ${PASSWORD} | bin/elasticsearch-keystore add elasticsearch.password -x
