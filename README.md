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

## Necessary Resources

To make the project fully functionable you need to provide three files:

- A `.graphml` file with the information of the city of la laguna. The file can be extracted using the `osmnx` package.

- An `.mdx` file with the content of the fire report. Your fire report should have the following format:

```
---other content---

<x coordinate>, <y coordinate>   (X, Y Coordinates)

---other content---

* **Fire Type:** <type>
* **Number of Injured People:** <number of injured people>
* **Fire Severity:** <severity>

---other content---
```

- An `.json` file with all the available firefighter units. The json file should have the format:

```json
{
  "fire_trucks": [
    {
      "uid": 1,
      "X_coordinate": 1.11,
      "Y_coordinate": -2.22,
      "unit_type": "truck",
      "personel_capacity": 4
    }
  ]
}
```

- An `.json` file with all the available hospital units. The json file should have the format:

```json
{
  "hospitals": [
    {
      "uid": 1,
      "X_coordinate": 12.48,
      "Y_coordinate": -14.68,
      "available_beds": 1
    }
  ]
}
```

## Environment Variables

Don't forget to export the environment variables with the paths of the files described above:

```bash
export FIRE_UNITS_JSON_FILE="your-file-path"
export MEDICAL_UNITS_JSON_FILE="your-file-path"
export CITY_FILE="your-file-path"
export FIRE_REPORT_PATH = "your-file-path"
```
