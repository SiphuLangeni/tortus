<p align="center">
    <img src="https://github.com/SiphuLangeni/tortus/blob/master/Images/tortus625.png" alt="tortus logo">
</p>


A python package that makes it easy to add labels to text data within a Jupyter Notebook.

## Installation

Run the following to install:

```python
pip install tortus
```

## Usage
```python
from tortus import Tortus

# create an instance
tortus = Tortus(df, 'id', 'text', num_records=5)

# begin annotations
tortus.annotate()

# store annotations
annotations = tortus.annotations
```

# Developing tortus

To install tortus, along with the tools you need for develop and run tests, run the followint in your virtualenv:

```bash
$ pip install -e .[dev]
``` 
