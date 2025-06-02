import pandas as pd
import numpy as np 
from config import *
import math
from itertools import combinations
import time
import matplotlib.pyplot as plt

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


def ComputeInverseDistanceToBordersScore(X_row, featurelabels, thisruleinfo, agg='mean'):
	scores = []
	for f in featurelabels:
		lower = thisruleinfo[thisruleinfo["Feature"] == f]["Lower"].values[0]
		upper = thisruleinfo[thisruleinfo["Feature"] == f]["Upper"].values[0]
		x_val = X_row[f]

		range_f = upper - lower + 1e-8 
		d_lower = x_val - lower
		d_upper = upper - x_val

		
		if d_lower < 0 or d_upper < 0:
			scores.append(1.0)
		else:
			min_distance = min(d_lower, d_upper) / range_f
			inverse_score = 1.0 - min_distance
			scores.append(inverse_score)
	#print(scores)
	if agg == 'mean':
		return np.mean(scores)
	elif agg == 'min':
		return np.min(scores)
	elif agg == 'prod':
		return np.prod(scores)
	else:
		raise ValueError("Unsupported aggregation function")

def ComputeTau(X,X_row, clslabel,featurelabels, ruleinfo,rulesimilarity,verifiedrules, T = 1):
	rulesimilarity = np.nan_to_num(rulesimilarity, nan=0.0)
	# this gives the list of rules satisfied by X_row and predicting clslabel;
	ruleid = list(set([int(i) for i in ruleinfo["Rule ID"].values]))
	#print("ruleid: ", ruleid)
	#print("verifiedrules: ", verifiedrules)
	if ruleid==[]: return np.array([1])

	# verifiedrules gives all rules satisfying X_row
	# indexes of rules predicting class 0 and verified by the point X_row
	cls0idx = [int(i) for i in verifiedrules if i in ruleid and i < changeclsidx]
	#print("satisfied from class 0: ", cls0idx)
	cls1idx = [int(i) for i in verifiedrules if i in ruleid and i >= changeclsidx]
	#print("satisfied from class 1: ", cls1idx)
	tauhatlist=[]
	taulist = []
	simlist = []
	# for each point, set a flag to True if the point is on the border of a rule
	#print("#### computing Tau #####")
	for r in ruleid:
		#print("r_k: ", r-1)
		thisruleinfo = ruleinfo[ruleinfo["Rule ID"]==r]
		
		
		tau = ComputeInverseDistanceToBordersScore(X_row, featurelabels, thisruleinfo)


		#print("gamma(x,r_k): ", tau)
		#time.sleep(30)
		#### begin correction based on rule similarity #####
		if r < changeclsidx:
			# r is for class 0
			indexes_except_r_cls0 = [i-1 for i in cls0idx if i-1!=r-1] 
			indexes_except_r_cls1 = [i-1 for i in cls1idx]
			#rint("indexes of overlapped rules with r_k - same label (y=0): ", indexes_except_r_cls0)
			#print("indexes of overlapped rules with r_k - opposite label (y=1): ", indexes_except_r_cls1)
		else:
			indexes_except_r_cls0 = [i-1 for i in cls0idx]
			indexes_except_r_cls1 = [i-1 for i in cls1idx if i-1!=r-1]
			#print("indexes of overlapped rules with r_k - same label (y=1): ", indexes_except_r_cls1)
			#print("indexes of overlapped rules with r_k - opposite label (y=0): ", indexes_except_r_cls0)

		if indexes_except_r_cls0 == []:
			avg_sim_0 = 0 #1
		else:
			#print(rulesimilarity[r-1, indexes_except_r_cls0])
			avg_sim_0 = np.nanmean(rulesimilarity[r-1, indexes_except_r_cls0])
		if indexes_except_r_cls1 == []:
			avg_sim_1 = 0 #1
		else:
			avg_sim_1 = np.nanmean(rulesimilarity[r-1, indexes_except_r_cls1])

		
		# new formulation
		if clslabel==cls0label:
			sim_term = avg_sim_1 - avg_sim_0

		elif clslabel==cls1label:
			sim_term = avg_sim_0 - avg_sim_1

		
		tauhat = 0.5 * tau * (1+sim_term)

		taulist.append(tau)
		simlist.append((1+sim_term)/2)
		tauhatlist.append(tauhat)
	return np.array(tauhatlist), np.array(taulist), np.array(simlist)#, np.array(isBorder)



def ComputeCONFIDERAI(X, parsedruleset, featurelabels,relevances,verifiedidx, changeclsidx, rulesimilarity):

	tauhatvalues = np.empty((len(X),len(relevances)))
	tauhatvalues[:] = 0

	tauvalues = np.empty((len(X),len(relevances)))
	tauvalues[:] = 0

	simvalues = np.empty((len(X),len(relevances)))
	simvalues[:] = 0

	score0list = []
	score1list = []
	for row in range(len(X)):
		X_row = X.iloc[row,:]
		#print("x: ", list(X_row))
		# indexes of verified rules for this row
		verifiedrules = verifiedidx[row]
		# verified rule indexes for row
		if verifiedrules ==[]: 
			#print(f"no rule verified, s(x,0) and s(x, 1) = {MAX_SCORE}")
			score0list.append(MAX_SCORE)
			score1list.append(MAX_SCORE)
			continue # score a 1
		else:
			# separate the indexes of verified rules predicting class 0 and those predicting class 1; make indexes start from 0
			satisfied_cls0 = [int(j-1) for j in verifiedrules if j < changeclsidx ]
			if satisfied_cls0==[]:
				#print(f"no rule verified for label {cls0label} -> s(x,0) = {MAX_SCORE}")
				score0list.append(MAX_SCORE)
			else:
				
				satisfied_cls0r = [int(j) for j in verifiedrules if j < changeclsidx]
				# compute tau for class 0
				parsedruleset_satisfied0 = parsedruleset[parsedruleset["Rule ID"].isin(satisfied_cls0r)]
				ruleinfo_cls0 = parsedruleset_satisfied0[parsedruleset_satisfied0["Output Class"]==cls0label]
				tauhat_cls0,tau_cls0,sim_cls0 = ComputeTau(X,X_row,cls0label,featurelabels,ruleinfo_cls0,rulesimilarity,verifiedrules, T = sigmoidT)
				tauhatvalues[row,satisfied_cls0] = tauhat_cls0
				tauvalues[row, satisfied_cls0] = tau_cls0
				simvalues[row, satisfied_cls0] = sim_cls0
				

				if CONSIDER_RELEVANCE:
					score_0 = np.prod(tauhat_cls0*(1-relevances[satisfied_cls0]))
					#print(f"s(x,0) = {score_0}")
				else:
					score_0 = np.prod(tauhat_cls0)

				score0list.append(score_0)
				

			satisfied_cls1 = [int(j-1) for j in verifiedrules if j >= changeclsidx ]
			if satisfied_cls1 == []:
				#print(f"no rule verified for label {cls1label} -> s(x,1) = {MAX_SCORE}")
				score1list.append(MAX_SCORE)
			else:

				satisfied_cls1r = [int(j) for j in verifiedrules if j >= changeclsidx]
				parsedruleset_satisfied1 = parsedruleset[parsedruleset["Rule ID"].isin(satisfied_cls1r)]
				#print(parsedruleset_satisfied1)

				ruleinfo_cls1 = parsedruleset_satisfied1[parsedruleset_satisfied1["Output Class"]==cls1label]
				#tauhat_cls1,isborder1 = ComputeTau(X,X_row,cls1label,featurelabels, ruleinfo_cls1)
				tauhat_cls1,tau_cls1, sim_cls1 = ComputeTau(X,X_row,cls1label,featurelabels, ruleinfo_cls1,rulesimilarity,verifiedrules, T = sigmoidT)
				tauhatvalues[row,satisfied_cls1] = tauhat_cls1
				tauvalues[row, satisfied_cls1] = tau_cls1
				simvalues[row, satisfied_cls1] = sim_cls1
				
				if CONSIDER_RELEVANCE:
					score_1 = np.prod(tauhat_cls1*(1-relevances[satisfied_cls1]))
					#print(f"s(x,1) = {score_1}")
				else:
					score_1 = np.prod(tauhat_cls1)
				score1list.append(score_1)
				
			#print("#########")
	#print(np.sum(tauhatvalues, axis = 0))

	return score0list,score1list,tauhatvalues,tauvalues,simvalues



# MAIN function to compute the scores for the Logic Learning Machine model

def ComputeScores(calibrationsetfile,rulesetfile, parsedruleset,relevances,outputlabel,featurelabels,changeclsidx,cls0label,cls1label,resultsfile,rulesimilarity,save_result=False, shuffle = False):

	data = pd.read_excel(calibrationsetfile)
	if shuffle: 
		data = data.sample(frac=1).reset_index(drop=True)
	
	predlabel="pred("+outputlabel+")"

	# pick features, ground truth labels, predicted labels and index of the principal rule covered by the point from the dataset
	X = data[featurelabels+[outputlabel,predlabel]]
	# get list of verified rules for each data point
	verifiedidx = GetSatisfiedRulesIndexes(data, rulesetfile, outputlabel)
	#verifiedidx,S= GetSatisfiedRules(data, rulesetfile, outputlabel)
	#print(verifiedidx)
	# get the CONFIDERAI scores
	#scores0,scores1,tauhatvalues= ComputeCONFIDERAI(X, parsedruleset,featurelabels, relevances, verifiedidx,changeclsidx, rulesimilarity)

	scores0,scores1,tauhatvalues,tauvalues,simvalues= ComputeCONFIDERAI(X, parsedruleset,featurelabels, relevances, verifiedidx,changeclsidx, rulesimilarity)

	X = X.copy()
	X.loc[:,"score-"+str(cls0label)]=scores0
	X.loc[:,"score-"+str(cls1label)]=scores1
	X.loc[:,["tauhat-rule"+str(j+1) for j in range(len(relevances))]]=tauhatvalues
	X.loc[:,["tau-rule"+str(j+1) for j in range(len(relevances))]]=tauvalues
	X.loc[:,["sim-rule"+str(j+1) for j in range(len(relevances))]]=simvalues

	
	# save to excel
	if save_result:
		X.to_excel(resultsfile,index = False)

	return X




