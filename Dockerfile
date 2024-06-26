FROM continuumio/miniconda3

RUN mkdir -p C1_Coursework

COPY . /C1_Coursework

WORKDIR /C1_Coursework

RUN conda env update -f environment.yml --name ResCompCW

RUN apt-get update && apt-get install -y \
    git

RUN echo "conda activate ResCompCW" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

RUN git init
RUN pre-commit install
