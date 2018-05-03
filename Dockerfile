FROM continuumio/anaconda3
RUN apt-get upgrade && apt-get update
RUN conda update -n base conda
RUN conda install -c conda-forge python-crfsuite
COPY . /address-parser
WORKDIR /address-parser
CMD ["python", "run.py"]
