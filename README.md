<p align='center'>
    <img src='https://raw.githubusercontent.com/SiphuLangeni/tortus/master/docs/_static/tortus_logo.svg?sanitize=true' alt='tortus logo' />
</p>
<br>

## A python package that makes it easy to add labels to text data within a Jupyter Notebook.

Ideal use is for datasets that can be managed within a pandas dataframe. Labels are applied to the selected number of records. Timestamped annotations can be saved in a dataframe for future use in any NLP/sentiment analysis project.

## Target audience  
 * Data practitioners
 * Researchers
 * Students
 * Data enthusiasts

Anyone in need of a simple and intuitive product to label text data easily and efficiently will benefit from **tortus**.  


## Installation

Run the following to install:
```python
pip install tortus
jupyter nbextension enable --py widgetsnbextension
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
``id_column``, ``annotations``, ``random`` and ``labels``.  

```python
tortus = Tortus(movie_reviews, 'reviews', num_records=3, id_column='review_id')
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

## Example
<img src='https://raw.githubusercontent.com/SiphuLangeni/tortus/master/docs/_static/tortus_example.gif' width='700' alt='tortus example' />  
<br>

Click [here](https://github.com/SiphuLangeni/tortus/tree/master/sample_project) to see a sample project using tortus.  


## Documentation
[https://tortus.readthedocs.io](https://tortus.readthedocs.io)  


## Developing tortus  

To install tortus, along with the tools you need to develop and run tests, run the following in your virtualenv:  

```bash
$ pip install -e .[dev]
``` 
