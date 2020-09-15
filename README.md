<p align='center'>
    <img width="750" src="docs/_static/tortus_logo.svg" alt="tortus logo">
</p>
<br>

A python package that makes it easy to add labels to text data within a Jupyter Notebook.

## Installation

Run the following to install:
```python
pip install tortus
```

## Usage
Import the necessary modules into a Jupyter Notebook.  

```python
import pd as pandas
from tortus import Tortus
```  

Read your dataset into a pandas dataframe.  

```python
movie_reviews = pd.read_csv('movie_reviews.csv')
```  

Create an instance of Tortus class. You are required to enter the dataframe and the name 
of the column of the text to be annotated. Optional parameters include ``num_records``, 
``id_column``, ``annotations`` and ``random``.  

```python
tortus = Tortus(movies_reviews, 'reviews', num_records=3, id_column='review_id')
```  

Call the ``annotate`` method to begin annotations.  

```python
tortus.annotate()
```  

At any time, annotations can be stored into an object. This can be passed to ``annotations`` if further
annotations are required at a later time.  

```python
annotations = tortus.annotations
```  

Click [here]() to see a sample project using tortus.  

## Developing tortus  

To install tortus, along with the tools you need for develop and run tests, run the followint in your virtualenv:  

```bash
$ pip install -e .[dev]
``` 
