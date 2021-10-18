#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Example code for key detection preprocessing. You may start with filling the 
'?'s below. There're also some description and hint within comment. However, 
please feel free to modify anything as you like!

@author: selly
"""
from glob import glob
from collections import defaultdict
# Below are packages and functions that you might need. Uncomment by remove the
# "#" in front of each line.
from librosa.feature import chroma_stft, chroma_cqt, chroma_cens
from librosa.effects import hpss
from scipy.stats import pearsonr
from mir_eval.key import weighted_score
from sklearn.metrics import accuracy_score
import numpy as np # np.log10()
import utils # self-defined utils.py file

#%%
DB   = 'GTZAN'
if DB=='GTZAN': # dataset with genre label classify at parent directory
	FILES = glob(DB+'/wav/*/*.wav')
else:
	FILES = glob(DB+'/wav/*.wav')

GENRE = [g.replace('\\','/').split('/')[2] for g in glob(DB+'/wav/*')]
n_fft = 100	# (ms)
hop_length = 25	# (ms)
#%% functions
def Q1(DB , gamma , FILES , Q3 , Q4 , Q4_cqt , Q4_cens):
	if DB=='GTZAN':
		label, pred = defaultdict(list), defaultdict(list)
	else:
		label, pred = list(), list()
	chromagram = list()
	gens       = list()
	for f in FILES:
		f = f.replace('\\','/')
		if (DB == "GTZAN"):
			content = utils.read_keyfile(f,'*.lerch.txt')
			if (int(content)<0): continue # skip saving if key not found
			gen = f.split('/')[2]
			label[gen].append(utils.LABEL[int(content)])
			gens.append(gen)
		elif (DB == "GiantSteps"):
			content = utils.read_keyfile(f,'*.key')
			content = utils.generalize_key(content)
			content = utils.str_to_lerch(content)
			if (int(content)<0): continue # skip saving if key not found
			label.append(utils.LABEL[content])
		else:
			content = utils.read_keyfile(f,'*.lerch.txt')
			if (int(content)<0): continue # skip saving if key not found
			label.append(utils.LABEL[content])
		sr, y = utils.read_wav(f)
		##########
		# TODO: Follow task1 description to give each audio file a key prediction.
		# compute the chromagram of audio data `y`
		if(gamma == 0):
			if(Q4_cqt == True):
				cxx = chroma_cqt(y=y , sr=sr)
			elif(Q4_cens == True):
				cxx = chroma_cens(y=y , sr=sr)
			else:
				cxx = chroma_stft(y=y , sr=sr)
		else:
			if(Q4_cqt == True):
				cxx = np.log10(1 + gamma * np.abs(chroma_cqt(y=y, sr=sr)))
			elif(Q4_cens == True):
				cxx = np.log10(1 + gamma * np.abs(chroma_cens(y=y, sr=sr)))
			else:
				cxx = np.log10(1 + gamma * np.abs(chroma_stft(y=y, sr=sr)))
		chromagram.append(cxx)
		# store into list for further use
		# summing up all the chroma features into chroma vector
		chroma_vector = np.sum(cxx , axis=1)
		# finding the maximal value in the chroma vector and considering the note 
		# name corresponding to the maximal value as the tonic pitch
		key_ind = np.max(chroma_vector)
		count =0
		for i in chroma_vector:
			if(i == key_ind):
				key_ind = count%12
				break
			count += 1
		# finding the correlation coefficient between the summed chroma vectors and 
		# the mode templates
		# Hint: utils.rotate(ar,n) may help you find different key mode template
		chroma_vector = utils.rotate(chroma_vector.tolist(), 12-key_ind)
		if(Q4 == True):
			p_major = pearsonr(chroma_vector , utils.KS["major"])
			p_minor = pearsonr(chroma_vector , utils.KS["minor"])
		else:
			p_major = pearsonr(chroma_vector , utils.MODE["major"])
			p_minor = pearsonr(chroma_vector , utils.MODE["minor"])
		if(p_major[0] > p_minor[0]):
			key_ind = (key_ind+3)%12
		else:
			key_ind = (key_ind+3)%12+12
		if DB=='GTZAN':
			pred[gen].append(utils.lerch_to_str(key_ind))
		else: 
			pred.append(utils.lerch_to_str(key_ind)) # you may ignore this when starting with GTZAN dataset
		##########
	if DB=='GTZAN':
		label_list, pred_list = list(), list()
		print("Genre    \taccuracy")
		for g in GENRE:
			##########
			# TODO: Calculate the accuracy for each genre
			# Hint: Use label[g] and pred[g]
			correct = 0
			fifth = 0
			relative = 0
			parallel = 0
			for acc_n in range(len(label[g])):
				l_tmp = utils.str_to_lerch(label[g][acc_n])
				p_tmp = utils.str_to_lerch(pred[g][acc_n])
				if (label[g][acc_n] == pred[g][acc_n]):
					correct += 1
				elif (l_tmp - p_tmp == 12 or l_tmp - p_tmp == -12):
					parallel += 1
				elif (l_tmp<12 and (l_tmp+7)%12 == p_tmp):
					fifth += 1
				elif (l_tmp>=12 and (l_tmp+7)%12 == p_tmp-12):
					fifth += 1
				elif ((l_tmp+9)%24 == p_tmp):
					relative += 1
			if(Q3 == True):
				try:
					acc = ((correct + 0.5*fifth + 0.3*relative + 0.2*parallel) / len(label[g]))*100
				except ZeroDivisionError:
					acc = 0
			else:
				try:
					acc = (correct / len(label[g]))*100
				except ZeroDivisionError:
					acc = 0
			##########
			print("{:9s}\t{:8.2f}%".format(g,acc))
			label_list += label[g]
			pred_list  += pred[g]
	else:
		label_list = label
		pred_list  = pred

	##########
	# TODO: Calculate the accuracy for all file.
	# Hint1: Use label_list and pred_list.
	correct = 0
	fifth = 0
	relative = 0
	parallel = 0
	for acc_n in range(len(label_list)):
		l_tmp = utils.str_to_lerch(label_list[acc_n])
		p_tmp = utils.str_to_lerch(pred_list[acc_n])
		if (label_list[acc_n] == pred_list[acc_n]):
			correct += 1
		elif (l_tmp - p_tmp == 12 or l_tmp - p_tmp == -12):
			parallel += 1
		elif (l_tmp<12 and (l_tmp+7)%12 == p_tmp):
			fifth += 1
		elif (l_tmp>12 and (l_tmp+7)%12 == p_tmp-12):
			fifth += 1
		elif ((l_tmp+9)%24 == p_tmp):
			relative += 1
	if(Q3 == True):
		try:
			acc_all = ((correct + 0.5*fifth + 0.3*relative + 0.2*parallel) / len(label_list))*100
		except ZeroDivisionError:
			acc_all = 0
	else:
		try:
			acc_all = (correct / len(label_list))*100
		except ZeroDivisionError:
			acc_all = 0
	##########
	print("----------")
	print("Overall accuracy:\t{:.2f}%".format(acc_all))
	del label.clear , pred , chromagram , gens , label_list , pred_list
	return
#%% main
print("GTZAN dataset")
print("Task 1")
print("***** Q1 *****")
Q1(DB , 0 , FILES , False , False , False , False)
print("***** Q2 *****")
print("r = 1")
Q1(DB , 1 , FILES , False , False , False , False)
print("r = 10")
Q1(DB , 10 , FILES , False , False , False , False)
print("r = 100")
Q1(DB , 100 , FILES , False , False , False , False)
print("r = 1000")
Q1(DB , 1000 , FILES , False , False , False , False)
print("***** Q3 *****")
Q1(DB , 0 , FILES , True , False , False , False)
print("Task 2")
print("***** Q4_1 *****")
Q1(DB , 0 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 0 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 0 , FILES , False , True , False , True)
print("***** Q4_2 *****")
print("r = 1")
Q1(DB , 1 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 1 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 1 , FILES , False , True , False , True)
print("r = 10")
Q1(DB , 10 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 10 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 10 , FILES , False , True , False , True)
print("r = 100")
Q1(DB , 100 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 100 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 100 , FILES , False , True , False , True)
print("r = 1000")
Q1(DB , 1000 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 1000 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 1000 , FILES , False , True , False , True)
print("***** Q4_3 *****")
Q1(DB , 0 , FILES , True , True , False , False)
print("use chroma_cqt")
Q1(DB , 0 , FILES , True , True , True , False)
print("use chroma_cens")
Q1(DB , 0 , FILES , True , True , False , True)
#%%
DB   = 'GiantSteps'
if DB=='GTZAN': # dataset with genre label classify at parent directory
	FILES = glob(DB+'/wav/*/*.wav')
else:
	FILES = glob(DB+'/wav/*.wav')

GENRE = [g.replace('\\','/').split('/')[2] for g in glob(DB+'/wav/*')]
#%% main
print("\nGiantSteps dataset")
print("Task 1")
print("***** Q1 *****")
Q1(DB , 0 , FILES , False , False , False , False)
print("***** Q2 *****")
print("r = 1")
Q1(DB , 1 , FILES , False , False , False , False)
print("r = 10")
Q1(DB , 10 , FILES , False , False , False , False)
print("r = 100")
Q1(DB , 100 , FILES , False , False , False , False)
print("r = 1000")
Q1(DB , 1000 , FILES , False , False , False , False)
print("***** Q3 *****")
Q1(DB , 0 , FILES , True , False , False , False)
print("Task 2")
print("***** Q4_1 *****")
Q1(DB , 0 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 0 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 0 , FILES , False , True , False , True)
print("***** Q4_2 *****")
print("r = 1")
Q1(DB , 1 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 1 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 1 , FILES , False , True , False , True)
print("r = 10")
Q1(DB , 10 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 10 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 10 , FILES , False , True , False , True)
print("r = 100")
Q1(DB , 100 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 100 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 100 , FILES , False , True , False , True)
print("r = 1000")
Q1(DB , 1000 , FILES , False , True , False , False)
print("use chroma_cqt")
Q1(DB , 1000 , FILES , False , True , True , False)
print("use chroma_cens")
Q1(DB , 1000 , FILES , False , True , False , True)
print("***** Q4_3 *****")
Q1(DB , 0 , FILES , True , True , False , False)
print("use chroma_cqt")
Q1(DB , 0 , FILES , True , True , True , False)
print("use chroma_cens")
Q1(DB , 0 , FILES , True , True , False , True)