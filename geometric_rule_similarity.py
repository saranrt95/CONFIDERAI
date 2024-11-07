import numpy as np
import pandas as pd
from math import ceil
from collections import defaultdict

#from rulesetparsing import *
from config import *

def GeometricRuleSimilarity(parsedruleset, AREA = True):
	'''
	parsedruleset.Feature = parsedruleset.Feature.astype("category")
	parsedruleset.Feature = parsedruleset.Feature.cat.set_categories(features)
	parsedruleset = parsedruleset.sort_values(["Rule ID", "Feature"])
	'''
	overlaps_all = []
	for n, rule in enumerate(list(set(list(parsedruleset["Rule ID"])))):
		# lower thresholds of the rule
		lower_rule = parsedruleset[parsedruleset["Rule ID"] == rule]["Lower"].values
		# upper thresholds
		upper_rule = parsedruleset[parsedruleset["Rule ID"] == rule]["Upper"].values

		updated_list = list(set(list(parsedruleset["Rule ID"])))
		overlaps_rule = []
		
		# iterate over the same set of rules 
		for i,rule_p in enumerate(updated_list):
			if rule == rule_p: 
				IoU = 1
				overlaps_rule.append(IoU)
				continue
			# lower thresholds
			lower_rule_p = parsedruleset[parsedruleset["Rule ID"] == rule_p]["Lower"].values
			# upper thresholds
			upper_rule_p = parsedruleset[parsedruleset["Rule ID"] == rule_p]["Upper"].values
			# concatenate the lowers
			l = np.column_stack((lower_rule,lower_rule_p))

			# maximum of the lower rule thresholds, for each feature
			MaxOfLowers = np.max(l, axis = 1)
			# concatenate the uppers
			u = np.column_stack((upper_rule,upper_rule_p))

			# minimum of upper rule thresholds, for each feature
			MinOfUppers = np.min(u, axis = 1)


			# all rule conditions are at least adjacent or overlapped --> geometrical similarity

			if np.prod(MaxOfLowers <= MinOfUppers) == 1:
				# vector of the domains defined by rule conditions; each row is a rule and each column is a feature
				domains = u.T-l.T

				domains[np.where(domains==0)] = 1 

				if AREA:
					# area of the rules
					areas = np.prod(domains, axis = 1)
					# width of the domains defined by the conditions
					overlap_domains = MinOfUppers - MaxOfLowers

					if np.shape(overlap_domains[overlap_domains!=0])[0] >= 2:
						# the overlap defines an area
						non_zero_overlaps = overlap_domains[overlap_domains!=0]
						area_overlap = np.prod(overlap_domains)

						IoU = area_overlap/(np.sum(areas, axis = 0) - area_overlap)
					else:
						perimeters = np.sum(2*domains, axis = 1)
						# the overlap is over a segment
						area_overlap = np.sum(overlap_domains)
						# ratio between overlap and total perimeters
						IoU = area_overlap/(np.sum(perimeters, axis = 0) - area_overlap)

				else:

					# perimeters of the rules
					perimeters = np.sum(2*domains, axis = 1)
					# widths of the domains defined by the conditions
					overlap_domains = MinOfUppers - MaxOfLowers

					if np.shape(overlap_domains[overlap_domains!=0])[0] >= 2:
						# the overlap defines an area
						perimeter_overlap = 2*np.sum(overlap_domains)
					else:
						# the overlap is over a segment
						perimeter_overlap = np.sum(overlap_domains)
					
					# ratio between overlap and total perimeters
					IoU = perimeter_overlap/(np.sum(perimeters, axis = 0) - perimeter_overlap + 10**-40)


				#print("rule {} and rule {} have an overlap of {}".format(rule, rule_p,IoU))
				overlaps_rule.append(IoU)
							
			else:
				#print("rule {} and rule {} are not overlapped".format(rule, rule_p))
				overlaps_rule.append(np.nan)

		overlaps_all.append(overlaps_rule)

	matrix =np.array(overlaps_all)
	matrix[matrix == 0] = np.nan

	if SAVE_RS_VALUES:
		if not exists(RS_PATH):
			os.mkdir(RS_PATH) 
		rr = pd.read_csv(rulesetfile, names = ["Rule","Covering","Error"])
		overlapMatrix = pd.DataFrame(matrix)
		overlapMatrix.index = list(rr["Rule"].values)
		overlapMatrix.columns = list(rr["Rule"].values)

		overlapMatrix.to_excel(RS_PATH+dataset+"_rulesimilarity.xlsx")

	return matrix