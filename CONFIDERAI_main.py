import pandas as pd
#import numpy as np
from math import ceil
from collections import defaultdict, Counter
from os.path import exists

from config import *
from rulesetparsing import *
from geometric_rule_similarity import *
from utils import *
from CONFIDERAI_score import *
from computeQuantile import *
from createPredictionRegion import *

# evaluation part
from CP_evaluation import *
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(dataset.upper())
# compute relevances of the rules
relevances = ComputeRelevances(rulesetfile)

# parse the ruleset to extract each condition and fill each rule with missing thresholds
parsedruleset = clean_ruleset_file(rulesetfile, propertrainfile, featurelabels, nfeatures)


parsedruleset.Feature = parsedruleset.Feature.astype("category")
parsedruleset.Feature = parsedruleset.Feature.cat.set_categories(featurelabels)
parsedruleset = parsedruleset.sort_values(["Rule ID", "Feature"])
# compute geometric rule similarity
rulesimilarity = GeometricRuleSimilarity(parsedruleset)

t_start_calib = time.time()
# compute scores on the calibration set
#score_calibration = ComputeLLMScores(calibrationsetfile,parsedruleset,relevances,outputlabel,featurelabels,changeclsidx,cls0label,cls1label,calibresfile,rulesimilarity,save_result=SAVE_RES_CALIB)
score_calibration = ComputeScores(calibrationsetfile,rulesetfile,parsedruleset,relevances,outputlabel,featurelabels,changeclsidx,cls0label,cls1label,calibresfile,rulesimilarity,save_result=SAVE_RES_CALIB, shuffle = SHUFFLE)
#t_end_calib = time.time()
#t_calib = t_end_calib-t_start_calib
#print("Time for score computation on calibration set [s]: ", t_calib)
if not exists(RES_PATH+"time_scores_calib.csv"):
	with open(RES_PATH+"time_scores_calib.csv","w") as of:
		of.write("Dataset,Time\n")
#with open(RES_PATH+"time_scores_calib.csv","a") as of:
#	of.write(dataset+","+str(t_calib)+"\n")

#t_start_test = time.time()
score_test = ComputeScores(testsetfile,rulesetfile,parsedruleset,relevances,outputlabel,featurelabels,changeclsidx,cls0label,cls1label,testscoresfile,rulesimilarity,save_result=SAVE_SCORES_TEST, shuffle = SHUFFLE)
#t_end_test = time.time()
#t_test = t_end_test-t_start_test

#print("Time for score computation on test set [s]: ", t_test)
'''
if not exists(RES_PATH+"time_scores_test.csv"):
	with open(RES_PATH+"time_scores_test.csv","w") as of:
		of.write("Dataset,Time\n")
with open(RES_PATH+"time_scores_test.csv","a") as of:
	of.write(dataset+","+str(t_test)+"\n")
'''

#t_inference = []
for i, epsilon in enumerate(epsilonlist):
	print("epsilon = ",epsilon)
	quantile_score = computeCalibrationQuantile(score_calibration, outputlabel, cls0label, cls1label, epsilon, approximate_quantile = APPROX_QUANTILE)
	print("quantile: ",quantile_score)
	
	#t_start_infer = time.time()
	results = GetPredictionRegions(score_test,quantile_score,cls0label,cls1label)
	if i == 0:
		t_end_infer = time.time()
		with open(RES_PATH+"time_scores_calib.csv","a") as of:
			of.write(dataset+","+str(t_end_infer-t_start_calib)+"\n")
		print("Elapsed Time [s]: ", t_end_infer-t_start_calib)
	
	sizeC = numLabels(results["PredictionRegion"])
	results=results.copy()
	results["Size"] = sizeC

	# conformal critical set for label targetCCS
	resultsCal = GetPredictionRegions(score_calibration,quantile_score,cls0label,cls1label)
	sizeC_cal = numLabels(resultsCal["PredictionRegion"])
	resultsCal=resultsCal.copy()
	resultsCal["Size"] = sizeC_cal
	conformalpoints = GetConformalPoints(resultsCal["PredictionRegion"], targetCSS)
	resultsCal=resultsCal.copy()
	resultsCal["ConformalPoint"] = conformalpoints
	resultsCal = resultsCal.reset_index(drop=True)
	if SAVE_FINAL_RES:
		resultsCal.to_excel(RES_PATH+"/results_eps"+str(epsilon).replace(".","")+"_"+dataset+".xlsx",index = False)
	
	'''
	conformalpoints = GetConformalPoints(results["PredictionRegion"], targetCSS)
	results=results.copy()
	results["ConformalPoint"] = conformalpoints

	results = results.reset_index(drop=True)

	if SAVE_FINAL_RES:
		results.to_excel(RES_PATH+"/results_eps"+str(epsilon).replace(".","")+"_"+dataset+".xlsx",index = False)
	'''
	# EVALUATION OF CP
	
	print("Evaluation on Test Data")
	avgErr,stdErr, errSingleClass0, stderr0, errSingleClass1, stderr1, avgC, stdC, avgEmpty, stdEmpty, avgSingle,stdSingle, avgSingle0,stdSingle0, avgSingle1,stdSingle1,avgDouble,stdDouble = EvaluateConformal(results,outputlabel,cls0label,cls1label)
	print("average error: {}\naverage error for class {}: {}\naverage error for class {}: {}".format(avgErr,cls0label,errSingleClass0,cls1label,errSingleClass1))
	print("average # of empty prediction regions: {}".format(avgEmpty))
	print("average # of singleton prediction prediction regions: {}".format(avgSingle))
	print("average # of singleton prediction prediction regions for class {}: {}".format(cls0label,avgSingle0))
	print("average # of singleton prediction prediction regions for class {}: {}".format(cls1label,avgSingle1))
	print("average # of double prediction prediction regions: {}".format(avgDouble))
	
	
	
	# EVALUATION ON calibration
	'''
	print("PERFORMANCE ON CALIBRATION")
	avgErr,stdErr, errSingleClass0, stderr0, errSingleClass1, stderr1, avgC, stdC, avgEmpty, stdEmpty, avgSingle,stdSingle, avgSingle0,stdSingle0, avgSingle1,stdSingle1,avgDouble,stdDouble = EvaluateConformal(resultsCal,outputlabel,cls0label,cls1label)
	print("average error: {}\naverage error for class {}: {}\naverage error for class {}: {}".format(avgErr,cls0label,errSingleClass0,cls1label,errSingleClass1))
	print("average # of empty prediction regions: {}".format(avgEmpty))
	print("average # of singleton prediction prediction regions: {}".format(avgSingle))
	print("average # of singleton prediction prediction regions for class {}: {}".format(cls0label,avgSingle0))
	print("average # of singleton prediction prediction regions for class {}: {}".format(cls1label,avgSingle1))
	print("average # of double prediction prediction regions: {}".format(avgDouble))
	'''
	if SAVE_METRICS:
		with open(metricsfile,'a') as mf:
			mf.write(str(epsilon)+","+str(avgErr)+','+str(stdErr)+','+str(errSingleClass0)+','+str(stderr0)+','+str(errSingleClass1)+','+str(stderr1)+','+str(avgC)+','+str(stdC)+','+str(avgEmpty)+","+str(stdEmpty)+','+str(avgSingle)+","+str(stdSingle)+","+str(avgSingle0)+","+str(stdSingle0)+","+str(avgSingle1)+","+str(stdSingle1)+','+str(avgDouble)+","+str(stdDouble)+"\n")
#dftime = pd.DataFrame(list(zip(epsilonlist,t_inference)),columns = ["epsilon","TimeInference"])
#dftime.to_csv(RES_PATH+"time_infer_"+dataset+".csv",index=False)


print("----------------------------------------")
