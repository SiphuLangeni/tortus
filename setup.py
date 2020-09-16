from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='tortus',
    version='0.0.1',
    description='Annotate text for classification in a Jupyter Notebook',
    url='https://github.com/SiphuLangeni/tortus',
    author='Siphu Langeni',
    author_email='szlangeni@gmail.com',
    py_modules=['tortus'],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Jupyter',
        'Operating System :: OS Independent'
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pandas', 'ipywidgets', 'ipython', 'notebook', 'jupyter_contrib_nbextensions'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7', 'check-manifest==0.10.1', 'twine==3.2.0'
        ]
    },


)
