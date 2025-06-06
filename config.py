import os
from os.path import exists
import numpy as np
import sys

if len(sys.argv) != 4:
	print("Usage: {} <dataset name> <fixed epsilon (true|false)> <targetCSS (0|1)>".format(sys.argv[0]))
	sys.exit(0)

dataset = sys.argv[1]
f = sys.argv[2]
targetCSS = int(sys.argv[3])
FIXED_EPSILON = f.lower() == "true"

# test with fixed epsilon
if FIXED_EPSILON:
	# choose an epsilon value and write it as list
	epsilonlist = [0.01,0.05,0.1,0.2]
	#epsilonlist = [0.05]
	# set to True to save results of LLM scores on calibration data to an excel file
	SAVE_RES_CALIB = True
	# set to True to save results of LLM scores on test data to an excel file
	SAVE_SCORES_TEST = False
	# save final results, with prediction regions in an excel file
	SAVE_FINAL_RES = True
	# set to True to save a csv file with performance metrics
	SAVE_METRICS = False
else:
	# set up a range of 1000 error levels between 0.05 and 0.5
	epsilonlist = list(np.linspace(0.05,0.5,100))
	# set to True to save results of LLM scores on calibration data to an excel file
	SAVE_RES_CALIB = False
	# set to True to save results of LLM scores on test data to an excel file
	SAVE_SCORES_TEST = False
	# save final results, with prediction regions in an excel file and rule counts
	SAVE_FINAL_RES = False
	# set to True to save a csv file with performance metrics
	SAVE_METRICS = True

# main folder with datasets and rulesets
DATA_PATH = "data/"

# whether to shuffle rows before computing scores
SHUFFLE = False

# path to folder for results
RES_PATH = "new_modified_score_20250521/"#"results_20250512_sigm_separate/"
if not exists(RES_PATH):
	os.mkdir(RES_PATH)

# score computation settings
CONSIDER_RELEVANCE = True # if rule relevance should be considered or not
MAX_SCORE = 1

# whether to save rule similarity tables or not
SAVE_RS_VALUES = False
RS_PATH = "rulesimilarity/"


if dataset == "p2p":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"p2p/p2p_rules.csv"

	# proper training set file
	propertrainfile = DATA_PATH+"p2p/proper.xlsx"
	# name of the column with real output labels
	outputlabel = "g"
	# name of the two features
	featurelabels = ["mA","mQ","mDt","vA","vQ","vDt","sA","sQ","sDt","kA","kQ","kDt"]
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in rulesetfile
	cls0label = 0
	cls1label = 1
	changeclsidx = 5

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	calibrationsetfile = DATA_PATH+"p2p/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_p2p.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/test_DNS_p2p.xlsx"
	testsetfile=DATA_PATH+"p2p/test.xlsx"


	testscoresfile=RES_PATH+"/scores_eps005_test_p2p.xlsx"

	#resfile = RES_PATH+"/DNSp2p_eps005_finalresults.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_p2p.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "ssh":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"ssh/ssh_rules.csv"


	propertrainfile = DATA_PATH+"ssh/proper.xlsx"
	# name of the column with real output labels
	outputlabel = "g"
	# name of the two features
	featurelabels = ["mA","mQ","mDt","vA","vQ","vDt","sA","sQ","sDt","kA","kQ","kDt"]
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 12

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"ssh/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_ssh.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/test_DNS_p2p.xlsx"
	testsetfile=DATA_PATH+"ssh/test.xlsx"


	testscoresfile=RES_PATH+"/scores_eps005_test_ssh.xlsx"

	#resfile = RES_PATH+"/DNSp2p_eps005_finalresults.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_ssh.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "smoking":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"smoking/smoking_rules.csv"


	# parsed ruleset
	propertrainfile = DATA_PATH+"smoking/proper.xlsx"
	# name of the column with real output labels
	outputlabel = "smoking"
	# name of the two features
	featurelabels=["age","height(cm)","weight(kg)","waist(cm)","eyesight(left)","eyesight(right)","systolic","relaxation","fasting blood sugar","Cholesterol","triglyceride","HDL","LDL","hemoglobin","Urine protein","serum creatinine","AST","ALT","Gtp"]
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 37

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"smoking/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_smoking.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/test_DNS_p2p.xlsx"
	testsetfile=DATA_PATH+"smoking/test.xlsx"


	testscoresfile=RES_PATH+"/scores_eps005_test_smoking.xlsx"

	#resfile = RES_PATH+"/DNSp2p_eps005_finalresults.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_smoking.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")



if dataset == "cardio":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"cardio/cardio_rules.csv"


	
	propertrainfile = DATA_PATH+"cardio/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "cardio"
	# name of the two features
	featurelabels=["age","height","weight","ap_hi","ap_lo","cholesterol","gluc"]
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 37

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"cardio/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_cardio.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile=DATA_PATH+"cardio/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_cardio.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_cardio.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "telescope":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"telescope/telescope_rules.csv"

	
	propertrainfile = DATA_PATH+"telescope/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "class"
	
	# name of the two features
	featurelabels=["fLength","fWidth", "fSize", "fConc","fConc1","fAsym","fM3Long","fM3Trans","fAlpha","fDist"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 23

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"telescope/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_telescope.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile=DATA_PATH+"telescope/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_telescope.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_telescope.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")



if dataset == "platooning":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"platooning/platooning_rules.csv"

	
	propertrainfile = DATA_PATH+"platooning/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "collision"
	
	# name of the two features
	featurelabels=["N","F0","PER","d0","v0"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 23

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"platooning/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_platooning.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile=DATA_PATH+"platooning/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_platooning.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_platooning.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "mqttset":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"mqttset/mqttset_rules.csv"

	
	propertrainfile = DATA_PATH+"mqttset/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "output"
	
	# name of the two features
	featurelabels=["tcp.time_delta","tcp.len","mqtt.conack.val","mqtt.conflag.cleansess","mqtt.conflag.passwd","mqtt.conflag.uname","mqtt.dupflag","mqtt.kalive","mqtt.len","mqtt.msgid","mqtt.msgtype","mqtt.proto_len","mqtt.qos","mqtt.retain","mqtt.ver"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 9

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"mqttset/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_mqttset.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile=DATA_PATH+"mqttset/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_mqttset.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_mqttset.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "rul":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"rul/rul_rules.csv"

	
	propertrainfile = DATA_PATH+"rul/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "RUL_binary"
	
	# name of the two features
	featurelabels=["s_os2","m_Nc","v_Nc","v_phi","m_htBleed","s_htBleed","m_W31"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 25

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"rul/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_rul.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile=DATA_PATH+"rul/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_rul.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_rul.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "eeg":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"eeg/eeg_rules.csv"

	
	propertrainfile = DATA_PATH+"eeg/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "eyeDetection"
	
	# name of the two features
	featurelabels=["AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 26

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"eeg/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_eeg.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile=DATA_PATH+"eeg/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_eeg.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_eeg.csv"

		if not exists(metricsfile):
			with open(metricsfile,'a') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "fire":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = DATA_PATH+"fire/fire_rules.csv"

	
	propertrainfile = DATA_PATH+"fire/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "Fire Alarm"
	
	# name of the two features
	featurelabels=["Temperature[C]","Humidity[%]","TVOC[ppb]","eCO2[ppm]","Raw H2","Raw Ethanol","Pressure[hPa]","PM1.0","PM2.5","NC0.5","NC1.0","NC2.5","CNT"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 4

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = DATA_PATH+"fire/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_fire.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile=DATA_PATH+"fire/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_fire.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_fire.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

