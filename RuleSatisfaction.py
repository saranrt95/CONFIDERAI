import pandas as pd
import numpy as np
import re


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def ReformattingRuleset(rules, output_label):
    #print(output_label)
    # adjust columns values
    for i in range(len(rules)+1):   
        rules["Rule"] = rules["Rule"].apply(lambda x: x.replace("RULE {}: ".format(i),""))
    rules["Rule"] = rules["Rule"].apply(lambda x: x.replace("AND","and"))
    rules["Rule"] = rules["Rule"].apply(lambda x: x.replace("{",""))
    rules["Rule"] = rules["Rule"].apply(lambda x: x.replace("}",""))
    rules["Rule"] = rules["Rule"].apply(lambda x: x.replace(f"{output_label} in ",f"{output_label} = "))
    rules["Covering"] = rules["Covering"].apply(lambda x: x.replace("COVERING: ",""))
    rules["Error"] = rules["Error"].apply(lambda x: x.replace("ERROR: ",""))
    rules['Output'] = rules['Rule'].str.extract(rf'{output_label} = (\d+)', expand=False).astype(int)
    rules["Rule"] = rules["Rule"].apply(lambda x: x.replace("IF ",""))
    rules["Rule"] = rules["Rule"].apply(lambda x: x.replace(x[x.find("THEN"):],""))
    
    return rules

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


def GetSatisfiedRulesIndexes(data, rulesetfile, output_label):
    rules = pd.read_csv(rulesetfile, header=None, names=["Rule", "Covering", "Error"])
    rules = ReformattingRuleset(rules, output_label)
    #print(rules["Rule"])
    idx_rules = 0
    satisfiedMat = np.zeros((len(data),len(rules)))
    for i, rule in rules.iterrows():
        idx_data = 0
        tuned_antecedent = rule['Rule'].strip()
        #print("rule: ", tuned_antecedent)
        for j, row in data.iterrows():
            
            # check if the point row satifies rule 
            if evaluate_rule_conditions(row, tuned_antecedent):
                # rule is satisfied           
                satisfiedMat[idx_data,idx_rules] = 1
                #print("satisfied")
            else:
                satisfied = False
            idx_data+=1
            #print("not satisfied")
        idx_rules+=1
    # given the matrix of satisfied rules, get the corresponding rule indexes
    verified_rules_indexes = [list(np.where(row == 1)[0] + 1) for row in satisfiedMat] 
    return verified_rules_indexes