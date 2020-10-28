# Logigram
 Logigram is a Python library for drawing a simple logic circuits.

## Description

## Installation
 
 Use the package manager [pip](https://pip.pypa.io/en/stable/) to install logigram.
  
  ```bash
  pip install logigram
  ```
  
## Usage
 
 ```python
  import logigram
  f = logigram.draw_schem('F=A*B+c*A+b') # returns a matplotlib figure 
  # for multiple functions input
  f = logigram.draw_schem(['F1=A*B+c*A+b','F2=A*B']) 
  # non-binary/multi value input
  f = logigram.draw_schem('F=A{1}*B{2}+C{0}')
  # save the figure 
  save_figure("image","svg")
  ```
## Visuals
  ![Ex. of a signle boolean function in a CDNF](examples/image2.svg)
  
  ![Ex. of the two boolean functions in a CDNF](examples/image1.svg)
  
  ![Ex. of a multi-value function in a CDNF](examples/image3.svg)
  
  ![Ex. of the two multi-value fucntions i a CDNF](examples/image4.svg)

  
  
"README.md" 26L, 438C
