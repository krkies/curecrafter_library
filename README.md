# README #

[CureCrafter](http://www.curecrafter.com/) is an online game

that crowdsources in silico design of novel inhibitors for potential theraputic uses

> **Bioinformatics algorithm** 

> Automated design of new molecules based on dataset of docked molecule

### Info ###

* v0.1

* Simpson College 

* Spring 2018

### Theory ###

* Users design molecules

* CureCrafter server docks molecules into protein (*scored by free energy*)

* Algorithm compiles all submissions into placement of atoms in 3D space

* Algorithm submits new molecule based on compliation of all previous submissions

### Modules ###

A: parse molecule text files into 3D grid of atoms

B: average each grid position by *atom type* & *molecule score*

C: assemble new molecule
