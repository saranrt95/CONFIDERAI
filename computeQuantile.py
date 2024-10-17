import pandas as pd 
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.quantile.html

def computeCalibrationQuantile(scoredata, outputlabel, cls0label, cls1label, epsilon, approximate_quantile = False):
	#scoredata = scoredata.dropna(axis =0)
	#print(scoredata)
	# scores for correct labels
	scoreslist=[]
	for row in range(len(scoredata)):
		#print(scoredata[outputlabel].iloc[row])
		if scoredata[outputlabel].iloc[row]==cls0label:
			scoreslist.append(scoredata["score-"+str(cls0label)].iloc[row])
			#print("score 0: ", scoredata["score-"+str(cls0label)].iloc[row])
		elif scoredata[outputlabel].iloc[row]==cls1label:
			scoreslist.append(scoredata["score-"+str(cls1label)].iloc[row])
			#print("score 1: ", scoredata["score-"+str(cls1label)].iloc[row])
		else:
			# possible nans in the ground truth
			continue
	scoredata = scoredata.copy()
	#print(scoreslist)
	scoredata["calibrationScores"] = scoreslist
	#print(scoreslist)
	orderedscores = scoredata["calibrationScores"].sort_values(axis = 0, ascending = True)
	#print(orderedscores)
	

	# taking unique values
	#calibrationScores = pd.Series(list(set(scoreslist)))
	#orderedscores = calibrationScores.sort_values(axis = 0, ascending = True)


	n_c = len(scoredata)
	#qlevel=ceil((n_c+1)*(1-epsilon))/n_c
	if approximate_quantile:
		qlevel = 1-epsilon #use this for little values of n_c
	else:
		qlevel=ceil((n_c+1)*(1-epsilon))/n_c

	quantile_score = orderedscores.quantile(q=qlevel)

	return quantile_score

