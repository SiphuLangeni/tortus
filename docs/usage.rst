.. figure:: _static/tortus_logo.svg
   :width: 300

|

Usage
=====

Code snippet
************
Import the necessary modules into a Jupyter Notebook.

.. code-block:: python
   
   import pd as pandas
   from tortus import Tortus


Read your dataset into a pandas dataframe.

.. code-block:: python

   movie_reviews = pd.read_csv('movie_reviews.csv')

Create an instance of Tortus class. You are required to enter the dataframe and the name 
of the column of the text to be annotated. Optional parameters include ``num_records``, 
``id_column``, ``annotations`` and ``random``. 

.. code-block:: python

   tortus = Tortus(movie_reviews, 'review', num_records=5)

Call the :meth:`annotate` method to begin annotations.

.. code-block:: python

   tortus.annotate()

At any time, annotations can be stored into an object. This can be passed to ``annotations`` if further
annotations are required at a later time.

.. code-block:: python

   annotations = tortus.annotations

|

Example
*******

|

.. image:: _static/tortus_example.gif
   :width: 700

|

Click `here`_ to see a sample project using tortus.

.. _here: https://github.com/SiphuLangeni/tortus/tree/master/sample_project

|
|
|

