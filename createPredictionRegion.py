import pandas as pd
import numpy as np

from config import *

def GetPredictionRegions(scoretestdata, quantile_score, cls0label,cls1label):

	scores_test_cls0 = list(scoretestdata["score-"+str(cls0label)])
	scores_test_cls1 = list(scoretestdata["score-"+str(cls1label)])

	# list of lists with predicted labels
	prediction_region = []
	for s0,s1 in list(zip(scores_test_cls0,scores_test_cls1)):
		singlerowpreds=[]
		if  s0 <= quantile_score:
			singlerowpreds.append(cls0label)
		if 	s1 <= quantile_score:
			singlerowpreds.append(cls1label)

		prediction_region.append(singlerowpreds)


	# update test data
	scoretestdata = scoretestdata.copy()
	scoretestdata["PredictionRegion"] = prediction_region



	return scoretestdata



def GetKnnRegions(P_ts, scoretestdata, rule_quantiles, cls0label,cls1label):


	prediction_region = []
	len_ts = 0
	for r in range(len(P_ts)):
		Xts_r = P_ts[r] 
		if r == 0:
			scores_test_cls0_r = list(scoretestdata["score-"+str(cls0label)].iloc[0:len(Xts_r)])
			scores_test_cls1_r = list(scoretestdata["score-"+str(cls1label)].iloc[0:len(Xts_r)])
		else:

			scores_test_cls0_r = list(scoretestdata["score-"+str(cls0label)].iloc[len_ts:len_ts+len(Xts_r)])
			scores_test_cls1_r = list(scoretestdata["score-"+str(cls1label)].iloc[len_ts:len_ts+len(Xts_r)])

		for s0,s1 in list(zip(scores_test_cls0_r,scores_test_cls1_r)):
			singlerowpreds=[]
			if  s0 <= rule_quantiles[r]:
				singlerowpreds.append(cls0label)
			if 	s1 <= rule_quantiles[r]:
				singlerowpreds.append(cls1label)

			prediction_region.append(singlerowpreds)
		len_ts+=len(Xts_r)

	# update test data
	scoretestdata = scoretestdata.copy()
	scoretestdata["PredictionRegion"] = prediction_region



	return scoretestdata