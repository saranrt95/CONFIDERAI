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
	SAVE_RES_CALIB = False
	# set to True to save results of LLM scores on test data to an excel file
	SAVE_SCORES_TEST = False
	# save final results, with prediction regions in an excel file and rule counts
	SAVE_FINAL_RES = False#True
	# set to True to save a csv file with performance metrics
	SAVE_METRICS = True
else:
	# set up a range of 1000 error levels between 0.05 and 0.5
	epsilonlist = list(np.linspace(0.05,0.5,1000))
	# set to True to save results of LLM scores on calibration data to an excel file
	SAVE_RES_CALIB = False
	# set to True to save results of LLM scores on test data to an excel file
	SAVE_SCORES_TEST = False
	# save final results, with prediction regions in an excel file and rule counts
	SAVE_FINAL_RES = False
	# set to True to save a csv file with performance metrics
	SAVE_METRICS = True

# path to folder for results
RES_PATH = "results_rev_paper_20240325/"
if not exists(RES_PATH):
	os.mkdir(RES_PATH)

#TAUFUNCTION = "sigmoid"
CONSIDER_RELEVANCE = True # if rule relevance should be considered or not
#TAUFUNCTION = "sigmoid"

# whether to save rule similarity tables or not
SAVE_RS_VALUES = False
RS_PATH = "rulesimilarity/"


if dataset == "p2p":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/p2p/p2p_rules.csv"

	# proper training set file
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/p2p/proper.xlsx"
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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/p2p/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_p2p.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/test_DNS_p2p.xlsx"
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/p2p/test.xlsx"


	testscoresfile=RES_PATH+"/scores_eps005_test_p2p.xlsx"

	#resfile = RES_PATH+"/DNSp2p_eps005_finalresults.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_p2p.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "ssh":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/ssh/ssh_rules.csv"


	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/ssh/proper.xlsx"
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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/ssh/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_ssh.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/test_DNS_p2p.xlsx"
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/ssh/test.xlsx"


	testscoresfile=RES_PATH+"/scores_eps005_test_ssh.xlsx"

	#resfile = RES_PATH+"/DNSp2p_eps005_finalresults.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_ssh.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "smoking":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/smoking/smoking_rules.csv"


	# parsed ruleset
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/smoking/proper.xlsx"
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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/smoking/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_smoking.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/test_DNS_p2p.xlsx"
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/smoking/test.xlsx"


	testscoresfile=RES_PATH+"/scores_eps005_test_smoking.xlsx"

	#resfile = RES_PATH+"/DNSp2p_eps005_finalresults.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_smoking.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")



if dataset == "cardio":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/cardio/cardio_rules.csv"


	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/cardio/proper.xlsx"

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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/cardio/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_cardio.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/cardio/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_cardio.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_cardio.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "telescope":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/telescope/telescope_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/telescope/proper.xlsx"

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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/telescope/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_telescope.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/telescope/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_telescope.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_telescope.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")



if dataset == "platooning":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/platooning/platooning_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/platooning/proper.xlsx"

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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/platooning/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_platooning.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/platooning/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_platooning.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_platooning.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "mqttset":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/mqttset/mqttset_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/mqttset/proper.xlsx"

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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/mqttset/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_mqttset.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/mqttset/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_mqttset.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_mqttset.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "rul":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/rul/rul_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/rul/proper.xlsx"

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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/rul/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_rul.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/rul/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_rul.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_rul.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")


if dataset == "eeg":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/eeg/eeg_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/eeg/proper.xlsx"

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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/eeg/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_eeg.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/eeg/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_eeg.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_eeg.csv"

		if not exists(metricsfile):
			with open(metricsfile,'a') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "fire":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/fire/fire_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/fire/proper.xlsx"

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
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/fire/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_fire.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = False

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/fire/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_fire.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/tablemetrics_fire.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "indian":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/indian/indian_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/indian/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "Dataset"
	
	# name of the two features
	featurelabels=["Age","Total_Bilirubin","Direct_Bilirubin","Alkaline_Phosphotase","Alamine_Aminotransferase","Aspartate_Aminotransferase","Total_Protiens","Albumin","Albumin_and_Globulin_Ratio"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 11

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/indian/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_indian.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = True

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/indian/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_indian.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_indian.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

if dataset == "spambase":
	# path to file with the ruleset (IF-THEN csv format), reporting covering and error metrics
	# N.B. this is the model obtained from training data
	rulesetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/spambase/spambase_rules.csv"

	
	propertrainfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/spambase/proper.xlsx"

	# name of the column with real output labels
	outputlabel = "output"
	
	# name of the two features
	featurelabels=["word_freq_make","word_freq_address","word_freq_all","word_freq_3d","word_freq_our","word_freq_over","word_freq_remove","word_freq_internet","word_freq_order","word_freq_mail","word_freq_receive","word_freq_will","word_freq_people","word_freq_report","word_freq_addresses","word_freq_free","word_freq_business","word_freq_email","word_freq_you","word_freq_credit","word_freq_your","word_freq_font","word_freq_000","word_freq_money","word_freq_hp","word_freq_hpl","word_freq_george","word_freq_650","word_freq_lab","word_freq_labs",
	"word_freq_telnet","word_freq_857","word_freq_data","word_freq_415","word_freq_85","word_freq_technology","word_freq_1999","word_freq_parts","word_freq_pm","word_freq_direct","word_freq_cs","word_freq_meeting","word_freq_original","word_freq_project","word_freq_re","word_freq_edu","word_freq_table","word_freq_conference","char_freq_;","char_freq_(","char_freq_[","char_freq_!","char_freq_$","char_freq_#","capital_run_length_average","capital_run_length_longest","capital_run_length_total"]
	
	nfeatures = len(featurelabels)
	# class labels; the order MUST follow the same order of class labels as reported in ruleset file
	cls0label = 0
	cls1label = 1
	changeclsidx = 9

	# CONFIGS -- calibration scores

	# path to dataset file with calibration; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	#calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/DNS/calib_DNS_p2p.xlsx"
	calibrationsetfile = "/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/spambase/calibration.xlsx"

	calibresfile=RES_PATH+"/scores_eps005_calib_spambase.xlsx"

	# CONFIGS -- quantile computation

	# set to True to use 1-epsilon as approximation of the defined quantile; to be used with few samples (e.g. < 200)
	APPROX_QUANTILE = True

	# CONFIGS -- find prediction regions on test data

	# path to test set file; to be exported in xlsx after LLM apply module 
	# it must contain indexes of the rules verified by each sample
	testsetfile="/Users/saranarteni/OneDrive - CNR/Conformal Predictors/Dataset20230619/reviewpaper/spambase/test.xlsx"

	testscoresfile=RES_PATH+"/scores_eps005_test_spambase.xlsx"

	if SAVE_METRICS:
		metricsfile = RES_PATH+"/metrics_spambase.csv"

		if not exists(metricsfile):
			with open(metricsfile,'w') as mf:
				mf.write("epsilon,avgErr,stdErr,avgErr0,stdErr0,avgErr1,stdErr1,avgC,stdC,avgEmpty,stdEmpty,avgSingle,stdSingle,avgSingle0,stdSingle0,avgSingle1,stdSingle1,avgDouble,stdDouble\n")

