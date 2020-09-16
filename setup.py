from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='tortus',
    version='0.0.2',
    description='Easy text annotation in a Jupyter Notebook',
    url='https://github.com/SiphuLangeni/tortus',
    author='Siphu Langeni',
    author_email='szlangeni@gmail.com',
    py_modules=['tortus'],
    packages=find_packages(include=['src']),
    include_package_data=True,
    package_dir={'': 'src'},
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
        'pandas', 'ipywidgets', 'ipython', 'notebook', 'jupyter_contrib_nbextensions'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7', 'check-manifest==0.10.1', 'twine==3.2.0'
        ]
    },


)