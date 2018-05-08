FROM continuumio/anaconda3
RUN apt-get upgrade && apt-get update
RUN apt-get install apache2 -y
RUN apt-get install vim -y
RUN conda update -n base conda
RUN conda install -c conda-forge python-crfsuite
RUN a2enmod cgi
COPY httpd.conf /etc/apache2/apache2.conf
COPY run.py /usr/lib/cgi-bin/
COPY hello.py /usr/lib/cgi-bin/
COPY crf.model /usr/lib/cgi-bin/
COPY data.json /usr/lib/cgi-bin/
RUN chmod 755 /usr/lib/cgi-bin/hello.py
RUN chmod 755 /usr/lib/cgi-bin/run.py
RUN chmod 755 /usr/lib/cgi-bin/crf.model
RUN chmod 777 /usr/lib/cgi-bin/data.json
# RUN service apache2 restart