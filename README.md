# Hamiltonian Circuits in Cayley Graphs

This repository contains the full content of my honors thesis and Python implementation related to **Hamiltonian circuits in Cayley graphs of finite abelian groups**. The main result is a corrected and extended construction for proving Hamiltonian Circuit on such graphs using group-theoretic and combinatorial methods.

## Thesis

**Title**: *Hamiltonian Circuits in Cayley Graphs*  
**Author**: Jiaming Zhang  
**Date**: April 2025  
**Advisor**: Prof. Denis Osin  
**Institution**: Vanderbilt University  

This thesis addresses the following conjecture:

> **Conjecture (Lovász-type for Cayley Graphs)**: Every finite connected Cayley graph is Hamiltonian.

By analyzing and extending a 1983 paper by Dragan Marušič, I identified a critical gap in his proposed construction and developed a recursive algorithm that fills this gap. The thesis formally proves the Hamiltonicity of connected Cayley graphs over abelian groups using dynamic sequence extensions and quotient group structures.

- 📘 [`Honor_Thesis_Final_Version_Jiaming_Zhang.pdf`](./Honor_Thesis_Final_Version_Jiaming_Zhang.pdf): Full text with definitions, lemmas, theorems, and illustrative examples.

## Code

The file [`Honor Thesis construction.py`](./Honor%20Thesis%20construction.py) implements a visual and dynamic approach to construct and animate Hamiltonian circuits for Cayley graphs over $\mathbb{Z}_m \times \mathbb{Z}_n$.

### Features

- Generates Cayley graphs from arbitrary generator sets over $$\mathbb{Z}_m \times \mathbb{Z}_n$$
- Constructs minimal generating sets
- Recursively builds Hamiltonian sequences
- Animates step-by-step traversal of Hamiltonian circuits using `matplotlib` and `networkx`

