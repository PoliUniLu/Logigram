# Logigram
[![Tests](https://github.com/PoliUniLu/logigram/workflows/Tests/badge.svg)](https://github.com/PoliUniLu/logigram/actions?workflow=Tests)
 Logigram is a Python library for drawing logic diagrams.

## Description
Logic diagrams are used for visualizing Boolean structures.
LOGIGRAM is a package for visualizing Boolean functions in disjunctive normal 
form (DNF). Resulting diagrams will thus consist of disjunctions of
conjunctions of literals. As inputs and outputs, LOGIGRAM can process either
binary or multivalent factors. The package was developed as an essential part
of the Python package CORA (Combinational Regularity Analysis).
CORA is a configurational comparative method for the analysis of Boolean
causal structures.

 

## Installation
 
 Use the package manager [pip](https://pip.pypa.io/en/stable/) to install LOGIGRAM.
  
  ```bash
  pip install git+https://github.com/PoliUniLu/Logigram.git
  ```
  
## Usage
 
 ```python
  import LOGIGRAM
  
  # returns a matplotlib figure
  f = logigram.draw_schem('A*B+c*A+b<=>F') 
  
  # for multi-output functions
  f = logigram.draw_schem(['A*B+c*A+b<=>F1','A*B<=>F2']) 
  
  # usage with multivalent factors
  f = logigram.draw_schem('A{1}*B{2}+C{0}<=>F')
  
  # usage with the lower case prime notations
  f = logigram.draw_schem('a*b+c'*a+b'<=>F')
 
  # save the figure 
  save_figure("image","svg")
  ```
## Visuals
  ![Ex. of a signle boolean function in a CDNF](examples/image2.svg)
  
  ![Ex. of the two boolean functions in a CDNF](examples/image1.svg)
  
  ![Ex. of a multi-value function in a CDNF](examples/image3.svg)
  
  ![Ex. of the two multi-value fucntions i a CDNF](examples/image4.svg)

## License
Logigram is licensed under a GNU GPLv3. 

## Contribution 

We welcome contributions from the community.
We encourage and recommend that feedback, bug reports, and feature requests should first be documented as an [Issue](https://github.com/PoliUniLu/cora/issues) on GitHub.

### Pull requests
To set up a development environment, use [Poetry](https://python-poetry.org/).
```console
pip install poetry
poetry install
```
Test the code by running
```console
poetry run pytest
```
Pull requests are welcome. Note that although the current codebase doesn't have entirely 
consistent code style the new code should be PEP-8 compliant.
