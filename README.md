# CONFIDERAI
Conformal prediction for binary rule-based classifiers.


This repository contains code, data and rules to replicate the experiments carried out in the paper:  _Narteni, S., Carlevaro, A., Dabbene, F., Muselli, M., & Mongelli, M. (2023). CONFIDERAI: a novel CONFormal Interpretable-by-Design score function for Explainable and Reliable Artificial Intelligence. arXiv preprint arXiv:2309.01778._ 

It allows to perform conformal prediction for any rule-based model, by using an innovative score function that leverages both rule relevance, and a geometrical factor encoding the distances of points with respect to rule boundaries and the overlaps among rules. In this way, we can provide statistical guarantees to such interpretable models.


<img width="547" alt="Schermata 2024-10-23 alle 09 29 49" src="https://github.com/user-attachments/assets/e119f90a-3caa-4710-911b-6c637ff225ad">



# Usage
To execute the same tests of the paper, just download or clone the repository and run the following line in the command line:

`sh test.sh `


To customize the code for running on your own data/rulesets, just change the parameters in the `config.py` file.

Then, run the following:

`python3 CONFIDERAI_main.py <datasetname> <True|False> <target_ccs>`, with options:

- `<True|False>`: set to True to conduct the experiments with a single/a few set of epsilon values; set to False to conduct the experiments with epsilon between 0.05 and 0.5.
- `<target_ccs (0|1)>`: target class for the conformal critical set definition.

Notes for proper working of the code:
1) Rulesets should be provided with the **same** syntax as those in our examples (see the _rules.csv files throughout the Dataset folder).
2) Datasets, after model training, should have the following columns:
  - pred(`'output'`), with `'output'` being the target label: the class predicted by the rule-based model for each point.

