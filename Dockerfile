FROM python:3.6-stretch

MAINTAINER Kyle Hernandez

RUN apt-get update \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

COPY LICENSE README.md setup.py /opt/
COPY gdc_fastq_splitter /opt/gdc_fastq_splitter 

RUN pip3 install /opt/

WORKDIR /opt

ENTRYPOINT ["/usr/local/bin/gdc-fastq-splitter"]

CMD ["--help"]
