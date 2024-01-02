# Efficient Evaluation of ABAC policies using High Dimensional Indexing Techniques

This repository contains the source code for implementing efficient policy evaluation in ABAC systems by leveraging high dimensional indexing structures commonly used in databases.

### Installation
No installation is required. Cloning the repository is sufficient

### Data structures
We have used the following data structures:
- R tree (for searching in a policy containing attributes in continuous spaces)
- ND tree (for searching in a policy containing attributes in non-ordered discrete spaces)
- CND tree (for searching in a policy containing both continuous and discrete attributes)

### Query patterns
The following queries have been implemented for the data structures mentioned above:
- Exact search
- Range search
- Approximate range search
- Nearest Neighbour (NN) search

### Further reading
To gain more context on our work, please refer to our publication [here](https://ieeexplore.ieee.org/abstract/document/9750254).
