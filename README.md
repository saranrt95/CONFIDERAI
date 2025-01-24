# CONFIDERAI
Conformal prediction for binary rule-based classifiers.


This repository contains code, data and rules to replicate the experiments carried out in the paper:  _Narteni, S., Carlevaro, A., Dabbene, F., Muselli, M., & Mongelli, M. (2024). "A novel score function for conformal prediction in rule-based binary classification", submitted to Elsevier - Pattern Recognition._ 

It allows to perform conformal prediction for any rule-based model, by using an innovative score function that leverages both rule relevance, and a geometrical factor encoding the distances of points with respect to rule boundaries and the overlaps among rules. In this way, we can provide statistical guarantees to such interpretable models.

<img width="996" alt="Schermata 2024-10-27 alle 11 30 58" src="https://github.com/user-attachments/assets/c57481f9-d50b-42ea-ae11-e0c3f3f13dff">


# Usage
To execute the same tests of the paper, just download or clone the repository and run the following line in the command line:

`sh test.sh `


To customize the code for running on your own data/rulesets, just change the parameters in the `config.py` file.

Then, run the following:

`python3 CONFIDERAI_main.py <datasetname> <True|False> <target_ccs>`, with options:

- `<True|False>`: set to True to conduct the experiments with a single/a few set of epsilon values; set to False to conduct the experiments with epsilon between 0.05 and 0.5.
- `<target_ccs (0|1)>`: target class for the conformal critical set definition.

Notes for proper working of the code:
1) Rulesets should be provided with the **same** syntax as those in our examples (see the _rules.csv files throughout the `data/` folder).
2) Datasets file (calibration and test sets), after rule-based classifier training, should have a column named `pred(output)`, with `output` being the name of the target label, with the class labels predicted by the rule-based model for each point.

