from IPython.display import SVG, HTML

tortus_logo = SVG(data='tortus/Images/tortus_logo.svg')
welcome = HTML("<h2 style='text-align:center'>easy text annotation in a Jupyter Notebook</h2>")
display(tortus_logo, welcome)

from .tortus import Tortus

