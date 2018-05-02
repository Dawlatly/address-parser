FROM continuumio/anaconda3
RUN apt-get upgrade && apt-get update
RUN conda update -n base conda
RUN conda install -c conda-forge python-crfsuite
CMD cd address-parser && python run.py
