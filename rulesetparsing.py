import pandas as pd
import numpy as np
from utils import *
import operator as op
import re

'''
# mapping string operator to logical operator (step successivo)
operators={'<': op.lt,
			'<=': op.le,
			'>': op.gt}
			'>=': op.ge}
'''

operators=['<','>']


def get_condition_operators(cond,operators):
	ops=[]
	#print(cond)
	# get the operators from the conditions			
	for opp in operators:
		idxlist=list(find_all(cond, opp))
		if len(idxlist)!=0:
			for opindex in idxlist:
				if cond[opindex+1]!=" ":
					ops.append(cond[opindex:opindex+2])
				else:
					ops.append(cond[opindex])
		else:
			continue
	return ops

def get_dataframe_from_dict(parsedrule,ruleidlist):
	#print(parsedrule)
	outputlist=[]
	minThs=[]#lower thresholds
	maxThs=[] #upper thresholds
	featurenames=[]
	operator1=[]
	operator2=[]

	for output in parsedrule:
		#print(output)
		for cond in parsedrule[output]:
			outputlist.append(output)
			minThs.append(cond[0])
			featurenames.append(cond[1])
			maxThs.append(cond[2])
			operator1.append(cond[3])
			operator2.append(cond[4])
	ruledf=pd.DataFrame(np.column_stack([outputlist,ruleidlist,minThs,featurenames,maxThs,operator1,operator2]),columns=["Output Class","Rule ID","Lower","Feature","Upper","Operator1","Operator2"])
	return ruledf


def rule_elements_extraction(ruleconditions,ruleidlist):
	parsedrule={}
	for output in ruleconditions:
		conditions=ruleconditions[output]#list of conditions
		
		#cond_elements={}
		cond_elements=[]
		#cond_elements = defaultdict(list)
		
		cc=0
		for cond in conditions:
			#print("condition: ",cond)
			cc+=1
			cond_elementslist=[]
			# get all the operators in condition cond
			ops= get_condition_operators(cond,operators)
			#print(ops)
			# get condition elements, extract feature name and thresholds
			# each condition is in the format lowerbound<feature<upper;
			# create a list of [lower,feature,upper,op1,op2] 
			# lower and upper will not be always explicit in the rules;
			# in these cases, min and max feature values will be considered (later)
			# by now, "" is added in place of the missing thresholds
			if len(ops)==1:
				#print("len ops 1")
				cond_elementslist=cond.split(ops[0])
				#print("before: ",cond_elementslist)
				cond_elementslist=[e.strip() for e in cond_elementslist]
				if ops[0]=='<=' or ops[0]=='<':
					cond_elementslist=[""]+cond_elementslist+ops+['<=']
				else:
					if ops[0]=='>' or  ops[0]=='>=':
						cond_elementslist=[cond_elementslist[1],cond_elementslist[0]]+[""]+['<']+['<=']
				#print("after: ", cond_elementslist)
			else:
				if len(ops)==2:
					#print("len ops 2")
					cond_elementslist=re.split(ops[0]+' |'+ops[1]+' ',cond)+ops
					#print("before: ",cond_elementslist)
					#print(cond_elementslist)
					cond_elementslist=[e.strip() for e in cond_elementslist]
					#print("after: ", cond_elementslist)
				# should never enter here - debug
				else:
					print("else ops")
			#cond_elements[cond].append(cond_elementslist)
			cond_elements.append(cond_elementslist)
		if parsedrule.get(output) is None:
			parsedrule[output]=cond_elements
		else:
			parsedrule[output]=cond_elements
	#print(parsedrule)
	# write dataframe from parsedrule dict
	parsedruledf=get_dataframe_from_dict(parsedrule,ruleidlist)
	# return parsedruledf
	return parsedruledf

def impute_missing_thresholds(datafile,parsedruledf):
	'''adds feature lower or upper bound to conditions that are in form of open intervals'''
	data=pd.read_excel(datafile)
	for idx in range(len(parsedruledf)):
		if parsedruledf["Lower"][idx]=="":
			parsedruledf.at[idx,"Lower"]=min(list(data[parsedruledf["Feature"][idx]]))
		else:
			parsedruledf.at[idx,"Lower"]=float(parsedruledf["Lower"][idx])
		if parsedruledf["Upper"][idx]=="":
			parsedruledf.at[idx,"Upper"]=max(list(data[parsedruledf["Feature"][idx]]))
		else:
			parsedruledf.at[idx,"Upper"]=float(parsedruledf["Upper"][idx])
	#print(parsedruledf)
	return parsedruledf

def fill_missing_features(datafile, ruleinfo, featurelabels, nfeatures):
	data=pd.read_excel(datafile)
	ruleid=list(set(list(ruleinfo["Rule ID"].values)))
	completerules = []
	for r in ruleid:
		thisruleinfo = ruleinfo[ruleinfo["Rule ID"]==r]
		thisruleinfo = thisruleinfo.drop(["Operator1","Operator2"],axis = 1, inplace = False)
		clslabel = list(set(list(thisruleinfo["Output Class"].values)))[0]
		#print("class: ", clslabel)
		thisrule = thisruleinfo.copy()
		# one feature is missing
		if len(thisruleinfo)!=nfeatures:
			featureinrule=list(thisruleinfo["Feature"].values)#.values[0]
			#featuremissing = [f for f in featurelabels if f!=featureinrule]#[0]
			featuremissing = [e for e in featurelabels if e not in featureinrule]
			lower_missing = list(data[featuremissing].min().values)
			upper_missing = list(data[featuremissing].max().values)
			clslist = [clslabel]*(nfeatures-len(featureinrule))
			ruleidlist = [r]*(nfeatures-len(featureinrule))
			#missing_row = [clslabel,r,lower_missing,featuremissing,upper_missing,"?","?"]
			tmp = pd.DataFrame(list(zip(clslist,ruleidlist,lower_missing,featuremissing,upper_missing)),columns=list(thisruleinfo.columns))
			#this=thisrule.append(tmp,ignore_index=True)
			completerules.append(pd.concat([thisrule, tmp], ignore_index = True))
		else:
			completerules.append(thisrule)
	completeruledf = pd.concat(completerules, axis = 0, ignore_index = True)
	completeruledf = completeruledf.sort_values(by = ["Rule ID"], ascending = True, ignore_index = True)
	return completeruledf

# MAIN FUNCTION
# PROBLEMA: NON VA SE IL NOME DEL TARGET CONTIENE "IN"!
def clean_ruleset_file(rulesetfile,datafile, featurelabels, nfeatures):
	ruledata=pd.read_csv(rulesetfile,header=None)
	#print(ruledata)
	rules=list(ruledata[0])
	#print(rules)
	rc=0 # rule id (counter)
	ruleidlist=[]
	rulecondtmp={} #temporary dict
	ltot= 0
	for rule in rules:
		rc+=1
		# 1. remove "RULE {rc}: " from current rule, rc being rule ID [e.g. "RULE 1: "]
		rule=rule.replace("RULE {}: ".format(rc),"")
		#print(rule)
		# 2. split premise and consequence of current rule; 
		# get a list of premise (IF...) and consequence
		premisecon_list=rule.split("THEN")
		#print(premisecon_list)
		#3. remove "IF " and obtain all the conditions 
		premise=premisecon_list[0][3:]
		conditions=premise.split("AND")
		#print(conditions)
		conditionslist=[] #list of conditions of current rule	
		for cond in conditions:
			c=cond.strip()
			conditionslist.append(c)
		#print(conditionslist)
		ltot = ltot+len(conditionslist)
		# consequence (output value)
		conseq=premisecon_list[1][1:]
		#print(conseq)
		#print(conseq.split(" "))
		ruleoutput=conseq.split(" ")[-1]#[1:]
		#print("rule out: ",ruleoutput)
		if rulecondtmp.get(ruleoutput) is None:
			rulecondtmp[ruleoutput] =[conditionslist]
			ruleidlist.append([rc]*len(conditionslist))
		else:
			rulecondtmp[ruleoutput].append(conditionslist)
			ruleidlist.append([rc]*len(conditionslist))
	#print("# conditions tot: ",ltot)
	ruleidlist=flatten(ruleidlist)
	#print(len(ruleidlist))
	#print(ruleidlist)
	#print(rulecondtmp)
	# dictionary with output class labels as keys and all rule conditions as values (da vedere come cambiarlo)
	ruleconditions = rulecondtmp.fromkeys(rulecondtmp, None)
	#print(ruleconditions)
	# rearrange lists inside dictionary (rulecondtmp) values (flatten function from utils.py)
	for output in ruleconditions:
		ruleconditions[output]=flatten(rulecondtmp[output])
	#print(len(ruleconditions['0'])+len(ruleconditions['1']))
	# create dict with the collected elements
	parsedruledf=rule_elements_extraction(ruleconditions,ruleidlist)
	# fill missing threshold values (get min or max from data)
	filledruledf=impute_missing_thresholds(datafile,parsedruledf)
	filledruledf = filledruledf.astype({'Rule ID':'int64','Output Class':'int64'})
	completeruledf = fill_missing_features(datafile, filledruledf, featurelabels, nfeatures)
	completeruledf = completeruledf.astype({'Rule ID':'int64','Output Class':'int64'})

	return completeruledf#filledruledf










