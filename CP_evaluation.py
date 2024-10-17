import pandas as pd
import numpy as np
import os 

def average_CPerror(y_test, conformal_preds):
	errors_cnt=[]
	for test_row in range(len(y_test)):
		if y_test[test_row] not in conformal_preds[test_row]:
			errors_cnt.append(1)
		else:
			errors_cnt.append(0)
	return np.mean(errors_cnt),np.std(errors_cnt)

def single_class_error(y_test,label,conformal_preds):
	errors=[]
	for test_row in range(len(y_test)):
		if y_test[test_row]==label and y_test[test_row] not in conformal_preds[test_row]:
			errors.append(1)
		else:
			if y_test[test_row]!=label:
				continue
			else:
				errors.append(0)
	#n_class=y_test[y_test==label].count()
	#print(n_class)
	return np.mean(errors),np.std(errors)


def averageNumClasses(conformal_preds):
	numC=[]
	for cp_instance in conformal_preds:
		numC.append(len(cp_instance))
	return np.mean(numC),np.std(numC)

def numLabels(conformal_preds):
	numC=[]
	for cp_instance in conformal_preds:
		numC.append(len(cp_instance))
	return numC

def getEmptyCP(conformal_preds):
	numEmpty=[]
	for cp_instance in conformal_preds:
		if len(cp_instance)==0:
			numEmpty.append(1)
		else:
			numEmpty.append(0)

	return np.mean(numEmpty),np.std(numEmpty)

def getSingletonCP(conformal_preds):
	numEmpty=[]
	for cp_instance in conformal_preds:
		if len(cp_instance)==1:
			numEmpty.append(1)
		else:
			numEmpty.append(0)

	return np.mean(numEmpty),np.std(numEmpty)

def getSingletonByClass(y_test,label,conformal_preds):
	numEmpty=[]
	for cp_instance in conformal_preds:
		if label in cp_instance and len(cp_instance)==1:
			numEmpty.append(1)
		else:
			numEmpty.append(0)
	return np.mean(numEmpty),np.std(numEmpty)

def getMultipleCP(conformal_preds):
	numEmpty=[]
	for cp_instance in conformal_preds:
		if len(cp_instance)>1:
			numEmpty.append(1)
		else:
			numEmpty.append(0)

	return np.mean(numEmpty),np.std(numEmpty)



def EvaluateConformal(results,outputlabel,cls0label,cls1label):
	# VALIDITY 
	# average error considering both classes
	avgErr,stdErr=average_CPerror(results[outputlabel],results["PredictionRegion"])# può anche essere utile per singole classi; forse da confrontare con tasso medio di errore senza conformal
	# average error for single classes 
	errSingleClass0,stderr0=single_class_error(results[outputlabel],cls0label,results["PredictionRegion"])
	errSingleClass1,stderr1=single_class_error(results[outputlabel],cls1label,results["PredictionRegion"])
	# EFFICIENCY
	avgC,stdC=averageNumClasses(results["PredictionRegion"])
	# number of empty regions wrt all CPs
	avgEmpty,stdEmpty=getEmptyCP(results["PredictionRegion"])

	avgSingle,stdSingle=getSingletonCP(results["PredictionRegion"])

	avgSingle0,stdSingle0 = getSingletonByClass(results[outputlabel],cls0label,results["PredictionRegion"])
	avgSingle1,stdSingle1 = getSingletonByClass(results[outputlabel],cls1label,results["PredictionRegion"])
	
	avgDouble,stdDouble=getMultipleCP(results["PredictionRegion"])

	return avgErr,stdErr, errSingleClass0, stderr0, errSingleClass1, stderr1, avgC, stdC, avgEmpty, stdEmpty, avgSingle,stdSingle, avgSingle0,stdSingle0, avgSingle1,stdSingle1,avgDouble,stdDouble

'''
# for conformal safety set as defined in COPA 2023
def GetConformalPoints(conformal_preds, y_true):
	conformalpoints=[]# 1= conformal; 0=not conformal
	for p,yt in zip(list(conformal_preds),list(y_true)):
		tmp=[]
		for c in str(p):
			if c =='0':           
				tmp.append(0)
			elif c =='1':
				tmp.append(1)
			else:
				continue
		if yt in tmp:
			conformalpoints.append(1)
		else:
			conformalpoints.append(0)
	return conformalpoints
'''

# for conformal safety set including only points whose prediction region is singleton and containing label 1
def GetConformalPoints(conformal_preds, targetCSS):
	conformalpoints=[]# 1= conformal; 0=not conformal
	#print(conformal_preds)
	for p in list(conformal_preds):
		#tmp=[]
		#print(p)
		# danger zone?
		if len(p) == 1 and p[0] == targetCSS:
			conformalpoints.append(1)
		else:
			conformalpoints.append(0)
	return conformalpoints


# added for debug

def ComputeMeanError(y_cp, y_true):
	n_err = 0

	for j in range(len(y_true)):
		if y_true[j]!=y_cp[j]:
			if y_cp[j]!=2:
				n_err=n_err+1
	avgErr = n_err/len(y_true)
	return avgErr

