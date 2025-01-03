# Fire Incident Multi Agent System

Welcome to the fire response incident flow project, powered by [crewAI](https://crewai.com). This project aims to provide an implementation of a multi-agent fire incident response system for the city of [San Cristobal de la Laguna, Canary Islands, Spain](https://es.wikipedia.org/wiki/San_Crist%C3%B3bal_de_La_Laguna).

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project is mostly based on [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) for dependency management and package handling. To further information on how to install conda please look [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). After conda is installed, you can proceed to create & activate an environment where all the dependencies will be installed:

```bash
conda create --name <env-name>
conda activate <env-name>
```

The next step is to install the [OSMnx](https://osmnx.readthedocs.io/en/stable/index.html) dependency:

```bash
conda install osmnx
```

Finally, you have to install the rest of the dependencies:

```bash
pip install .
```

## Running the Project

To kickstart the flow presented in `main.py` you can run from the root folder:

```bash
crewai flow kickoff
```
