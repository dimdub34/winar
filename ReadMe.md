# WINAR – oTree Applications

This repository contains the oTree applications developed for the **WINAR** research project, coordinated by *Rustam Romaniuc*.
All instructions and user interfaces are written in English.

If you plan to run this experiment in another country and language, please download the entire project and translate the necessary files (`__init__.py` and `*.html`) in each application folder. With development tools such as PyCharm and GitHub Copilot, this process is straightforward and efficient.

---

## Requirements

* **Python** 3.11
* **oTree** 5.11.4

The full list of dependencies is provided in [`conda_env.yml`](./conda_env.yml).

---

## Installation

Clone the repository:

```bash
git clone https://github.com/dimdub34/winar.git
cd winar-otree
```

Create the conda environment:

```bash
conda env create -f conda_env.yml
```

Activate the environment:

```bash
conda activate otree5
```

Check that oTree is installed correctly:

```bash
otree --version
```

Expected output:

```
5.11.4
```

---

## Usage

To start the development server:

```bash
otree devserver
```

By default, oTree will run at [http://localhost:8000](http://localhost:8000).

---

## Contact

For any questions regarding these applications, please contact:
**Dimitri Dubois** – [dimitri.dubois@umontpellier.fr](mailto:dimitri.dubois@umontpellier.fr)

