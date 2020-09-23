from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='tortus',
    version='1.0.1',
    description='Easy text annotation in a Jupyter Notebook',
    url='https://github.com/SiphuLangeni/tortus/',
    project_urls={
        'Source Code': 'https://github.com/SiphuLangeni/tortus/blob/master/src/tortus/tortus.py',
        'Documentation': 'https://tortus.readthedocs.io/'
    },
    author='Siphu Langeni',
    author_email='szlangeni@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    # py_modules=['tortus.tortus'],
    include_package_data=True,
    # py_modules=['tortus.tortus'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        'tortus': ['*.png'],
    },
    
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Jupyter',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    keywords=[
        'nlp', 'annotation', 'labeling', 'jupyter-notebook', 'ipywidgets'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0.1',
        'ipywidgets>=7.5.1',
        'ipython>=7.12.0',
        'jupyter-contrib-nbextensions>=0.5.1'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7', 'check-manifest==0.10.1', 'twine==3.2.0'
        ]
    },


)