import pandas as pd
import numpy as np 
from config import *
import math
from itertools import combinations

from RuleSatisfaction import *

def ComputeRelevances(rulesetfile):
	
	""" For each rule of the ruleset, computes its relevance as covering*(1-error); 
		Input: 
			- rulesetfile: path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
		Output:
			- relevances: numpy array with the obtained relevance values. 

	"""
	errorlist=[]
	coveringlist=[]
	with open(rulesetfile,"r") as infile:
		rules = infile.readlines()
		#print(rules)
		for rule in rules:
			#print(rule)
			rule = rule.replace("\n","")
			c = rule.split(",")[1]
			covering_value = float(c[11:])
			#print(covering_value)
			coveringlist.append(covering_value)
			e = rule.split(",")[2]
			#print(e[8:])
			error_value = float(e[8:])
			#print(error_value)
			errorlist.append(error_value)

	relevances = [c*(1-e) for c,e in list(zip(coveringlist,errorlist))]
	relevances = np.array(relevances)
	return relevances


def ComputeDistanceFromBorder(X_row,featurelabels,thisruleinfo):
	# check if any feature is missing from current rule
	if len(thisruleinfo)!=nfeatures:
		featureinrule=list(thisruleinfo["Feature"].values)#.values[0]
		featuremissing = [e for e in featurelabels if e not in featureinrule]
	else:
		# no feature is missing from thisruleinfo
		featuremissing = []
	gammavalues = []
	# for each feature, compute point X_row distance from its lower and upper bounds
	for f in featurelabels:
		#if f in featuremissing:
		#	gammalower = 10**40
		#	gammaupper = 10**40
		#else:
		gammalower = abs(thisruleinfo[thisruleinfo["Feature"]==f]["Lower"].values[0]-X_row[f])
		gammaupper = abs(thisruleinfo[thisruleinfo["Feature"]==f]["Upper"].values[0]-X_row[f])
		gammavalues.append(gammalower)
		gammavalues.append(gammaupper)
	# list of all distances of the point with respect to the borders along features appearing in the rule
	#gammavalues_mod = [e for e in gammavalues if e!=10**40] 
	return gammavalues#_mod #mindistance

def ComputeTau(X,X_row, clslabel,featurelabels, ruleinfo,rulesimilarity,verifiedrules):
	ruleid=list(set(list(ruleinfo["Rule ID"].values)))
	if ruleid==[]: return np.array([1])

	# indexes of rules predicting class 0 and verified by the point X_row
	cls0idx = [int(i) for i in verifiedrules if i in ruleid and i < changeclsidx]
	#print(cls0idx)
	cls1idx = [int(i) for i in verifiedrules if i in ruleid and i >= changeclsidx]
	#print(cls1idx)
	taulist=[]
	# for each point, set a flag to True if the point is on the border of a rule
	isBorder = []
	for r in ruleid:
		thisruleinfo = ruleinfo[ruleinfo["Rule ID"]==r]
		# distance_to_border = ComputeDistanceFromBorder(X_row,featurelabels,thisruleinfo)
		distances = ComputeDistanceFromBorder(X_row,featurelabels,thisruleinfo)

		sum_inverse_distances = 0
		for e in distances:
			sum_inverse_distances+=(1/(e+10**(-40)))
		tau = sum_inverse_distances
		#tau = 1 / (1 + math.exp(-tau))
		
		#### begin correction based on rule similarity #####
		#cls0idx = np.arange(0,changeclsidx-1)
		#cls1idx = np.arange(changeclsidx-1, rulesimilarity.shape[0])

		if r < changeclsidx:
			# r is for class 0
			indexes_except_r_cls0 = [i-1 for i in cls0idx if i!=r-1] 
			indexes_except_r_cls1 = [i-1 for i in cls1idx]
		else:
			indexes_except_r_cls0 = [i-1 for i in cls0idx]
			indexes_except_r_cls1 = [i-1 for i in cls1idx if i!=r-1] 
		if indexes_except_r_cls0 == []:
			avg_sim_0 = 1
		else:
			avg_sim_0 = np.nanmean(rulesimilarity[r-1, indexes_except_r_cls0])
		if indexes_except_r_cls1 == []:
			avg_sim_1 = 1
		else:
			avg_sim_1 = np.nanmean(rulesimilarity[r-1, indexes_except_r_cls1])
	
		'''
		if np.isnan(avg_sim_0):
			avg_sim_0 = 1
		if np.isnan(avg_sim_1):
			avg_sim_1 = 1
		'''
		if clslabel==cls0label:
			sim_term = avg_sim_0/avg_sim_1
		elif clslabel==cls1label:
			sim_term = avg_sim_1/avg_sim_0
		else:
			RaiseValueError("Invalid label")

		tau = tau*sim_term

		###### end correction ######

		tau = 1 / (1 + math.exp(-tau))

		#border = False
		taulist.append(tau)
		#isBorder.append(border)
	return np.array(taulist)#, np.array(isBorder)



def ComputeCONFIDERAI(X, parsedruleset, featurelabels,relevances,verifiedidx, changeclsidx, rulesimilarity):


	tauvalues = np.empty((len(X),len(relevances)))
	tauvalues[:] = np.nan
	score0list = []
	score1list = []

	for row in range(len(X)):
		X_row = X.iloc[row,:]
		# indexes of verified rules for this row
		verifiedrules = verifiedidx[row]
		#verifiedrules = [e for e in verifiedrules if not np.isnan(e)]
		#print(verifiedrules)
		# verified rule indexes for row
		if verifiedrules ==[]: 
			#print("no verified")
			score0list.append(1)
			score1list.append(1)
			continue # score a 1
		else:
			# separate the indexes of verified rules predicting class 0 and those predicting class 1; make indexes start from 0
			satisfied_cls0 = [int(j-1) for j in verifiedrules if j < changeclsidx ]
			satisfied_cls1 = [int(j-1) for j in verifiedrules if j >= changeclsidx ]
			'''
			if satisfied_cls0 == []: 
				score0list.append(1)
				continue
			if satisfied_cls1 == []:
				score1list.append(1)
				continue
			'''
			# make indexes start from 1
			satisfied_cls0r = [int(j) for j in verifiedrules if j < changeclsidx ]
			satisfied_cls1r = [int(j) for j in verifiedrules if j >= changeclsidx ]

			# compute tau for class 0
			parsedruleset_satisfied0 = parsedruleset[parsedruleset["Rule ID"].isin(satisfied_cls0r)]
			ruleinfo_cls0 = parsedruleset_satisfied0[parsedruleset_satisfied0["Output Class"]==cls0label]
			tau_cls0 = ComputeTau(X,X_row,cls0label,featurelabels,ruleinfo_cls0,rulesimilarity,verifiedrules)
			#print(tau_cls0)
			tauvalues[row,satisfied_cls0] = tau_cls0
			
			# compute tau for class 1
			parsedruleset_satisfied1 = parsedruleset[parsedruleset["Rule ID"].isin(satisfied_cls1r)]

			ruleinfo_cls1 = parsedruleset_satisfied1[parsedruleset_satisfied1["Output Class"]==cls1label]
			#tau_cls1,isborder1 = ComputeTau(X,X_row,cls1label,featurelabels, ruleinfo_cls1)
			tau_cls1 = ComputeTau(X,X_row,cls1label,featurelabels, ruleinfo_cls1,rulesimilarity,verifiedrules)
			tauvalues[row,satisfied_cls1] = tau_cls1


			if CONSIDER_RELEVANCE:
				score_0 = np.prod(tau_cls0*(1-relevances[satisfied_cls0]))
				score_1 = np.prod(tau_cls1*(1-relevances[satisfied_cls1]))
			else:
				score_0 = np.prod(tau_cls0)
				score_1 = np.prod(tau_cls1)
			#print("score_0: ",score_0)
			#print("score_1: ",score_1)
			score0list.append(score_0)
			score1list.append(score_1)

	return score0list,score1list,tauvalues



# MAIN function to compute the scores for the Logic Learning Machine model

def ComputeScores(calibrationsetfile,rulesetfile, parsedruleset,relevances,outputlabel,featurelabels,changeclsidx,cls0label,cls1label,resultsfile,rulesimilarity,save_result=False):

	data = pd.read_excel(calibrationsetfile)
	predlabel="pred("+outputlabel+")"

	# pick features, ground truth labels, predicted labels and index of the principal rule covered by the point from the dataset
	X = data[featurelabels+[outputlabel,predlabel]]

	# pick the indexes of the rules (of whatever class) satisfied by each sample in X
	#verifiedcolumnnames = [col for col in data.columns if 'rule-' in col]
	#print(verifiedcolumnnames)
	#verifiedidx=data[verifiedcolumnnames]
	verifiedidx = GetSatisfiedRulesIndexes(data, rulesetfile, outputlabel)
	# get the CONFIDERAI scores for the LLM
	scores0,scores1,tauvalues= ComputeCONFIDERAI(X, parsedruleset,featurelabels, relevances, verifiedidx,changeclsidx, rulesimilarity)
	X = X.copy()
	X.loc[:,"score-"+str(cls0label)]=scores0
	X.loc[:,"score-"+str(cls1label)]=scores1
	X.loc[:,["tau-rule"+str(j+1) for j in range(len(relevances))]]=tauvalues

	
	# save to excel
	if save_result:
		X.to_excel(resultsfile,index = False)

	return X




