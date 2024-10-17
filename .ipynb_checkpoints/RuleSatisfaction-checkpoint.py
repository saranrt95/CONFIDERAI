import pandas as pd
import numpy as np
import re


def evaluate_rule_conditions(row, condition_part):

    # Checks if any of the conditions in the rule are satisfied
    if all(check_condition(row, part) for part in condition_part.split(" and ")):
        return True  # Return True if all conditions in the rule are satisfied
    
    return False  # Return False if any of the conditions in the rule is not satisfied


def check_condition(row, condition_part):
    # Check if a single condition part is satisfied
    
    #parts = [part.strip('()') for part in condition_part.split()]
    #parts = [part for part in condition_part.split()]
    # Use regular expressions to properly parse the condition
    parts = re.split(r'\s*(==|<=|>=|<|>|!=)\s*', condition_part)
    
    #print("parts: ", parts)
    if len(parts) == 3:
        column, op, value = parts
        return eval(f"{row[column]} {op} {value}")
    # handle the case of a 2-thresholds conditions of the kind: a < Column <= b
    elif len(parts) == 5:
        val1,op1,column,op2,val2 = parts
        # Use the original condition from the rule
        return eval(f"{val1} {op1} {row[column]} {op2} {val2}")        
    else:
        RaiseValueError("Bad condition formatting!")


def evaluate_rules(data, N1, tuned_rules, output, dataset_name = None):

    idx_rules = 0
    satisfiedMat = np.zeros((len(data),len(tuned_rules)))
    for i, rule in tuned_rules.iterrows():
        
        idx_data = 0
        tuned_antecedent = rule['Rule'].strip()
        print(f"rule: {tuned_antecedent}")
        for j, row in data.iterrows():
            # check if the point row satifies rule 
            if evaluate_rule_conditions(row, tuned_antecedent):
                # rule is satisfied           
                satisfiedMat[idx_data,idx_rules] = 1
                #print("satisfied")
            else:
                satisfied = False
         
            #print("not satisfied")
        idx_rules+=1
    return satisfiedMat