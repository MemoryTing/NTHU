#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example code for local key detection preprocessing. You may start with filling 
the '?'s below. There're also some description and hint within comment. However, 
please feel free to modify anything as you like!

@author: selly
"""
import numpy as np
from glob import glob
import librosa
from scipy.stats import pearsonr
import pretty_midi
import utils # self-defined utils.py file

#%% function
def Q5_detect(num , sr , y , pred):
	if(num < 16):
		tmp_y = y[:sr*(num+16)]
	elif(num < int(len(y)/sr)-16):
		tmp_y = y[(num-15)*sr:sr*(num+16)]
	else:
		tmp_y = y[(num-15)*sr:]
	cxx = librosa.feature.chroma_cqt(y=tmp_y , sr=sr)
	chroma_vector = np.sum(cxx , axis=1)
	key_ind = np.max(chroma_vector)
	count =0
	for i in chroma_vector:
		if(i == key_ind):
			key_ind = count%12
			break
		count += 1
	chroma_vector = utils.rotate(chroma_vector.tolist(), 12-key_ind)
	p_major = pearsonr(chroma_vector , utils.MODE["major"])
	p_minor = pearsonr(chroma_vector , utils.MODE["minor"])
	if(p_major[0] > p_minor[0]):
		key_ind = (key_ind+3)%12
	else:
		key_ind = (key_ind+3)%12+12
	print(num , "\t" , utils.lerch_to_str(key_ind))
	pred.extend([utils.lerch_to_str(key_ind)])
	return

#%% BFSFH or BRSFH?
DB = 'BPS-FH'
last_label_num = 0
chromagram, label, index, pred = list(), list(), list(), list()
for f in glob(DB+'/wav/*.wav'):
	f = f.replace('\\','/')
	print(f)
	key = utils.parse_key([line.split('\t')[1] for line in utils.read_keyfile(f,'*.txt').split('\n')])
	label.extend(key)
	sr, y = utils.read_wav(f)
	count =0
	while count < len(label)-last_label_num:
		Q5_detect(count , sr , y , pred)
		count += 1
	last_label_num = len(label)

correct = 0
fifth = 0
relative = 0
parallel = 0
for acc_n in range(len(label)):
	l_tmp = utils.str_to_lerch(label[acc_n])
	p_tmp = utils.str_to_lerch(pred[acc_n])
	if (label[acc_n] == pred[acc_n]):
		correct += 1
	elif (l_tmp - p_tmp == 12 or l_tmp - p_tmp == -12):
		parallel += 1
	elif (l_tmp<12 and (l_tmp+7)%12 == p_tmp):
		fifth += 1
	elif (l_tmp>12 and (l_tmp+7)%12 == p_tmp-12):
		fifth += 1
	elif ((l_tmp+9)%24 == p_tmp):
		relative += 1
print("BPS-FH")
print("correct and parallel relative detection")
try:
	acc_all = ((correct + 0.5*fifth + 0.3*relative + 0.2*parallel) / len(label))*100
except ZeroDivisionError:
	acc_all = 0
print("Overall accuracy:\t{:.2f}%".format(acc_all))
print("correct detection")
try:
	acc_all = (correct / len(label))*100
except ZeroDivisionError:
	acc_all = 0
##########
print("Overall accuracy:\t{:.2f}%".format(acc_all))
print("----------")
del chromagram, label, pred# clean to free memory

#%% A-MAPS
DB = 'A-MAPS'
label, pred = list(), list()
for f in glob(DB+'/*.mid'):
	f = f.replace('\\','/')
	midi_data = pretty_midi.PrettyMIDI(f)
	#get label
	key = midi_data.key_signature_changes
	for i in range(len(key)):
		key_num = utils.parse_key_number(key[i].key_number)
		label.append([int(key[i].time) , key_num])
	print(label)
	#get pred
	chroma_vector = midi_data.get_chroma()
	for count_time in range(int(midi_data.get_end_time())):
		tmp_vector = list()
		for x in range(12):
			if(count_time < 16):
				tmp_vector.append(chroma_vector[x][:100*(count_time+16)])
			elif(count_time < int(midi_data.get_end_time())-16):
				tmp_vector.append(chroma_vector[x][(count_time-15)*100:100*(count_time+16)])
			else:
				tmp_vector.append(chroma_vector[x][(count_time-15)*100:])
		tmp_vector = np.sum(tmp_vector , axis=1)
		key_ind = np.max(tmp_vector)
		count =0
		for i in tmp_vector:
			if(i == key_ind):
				key_ind = count%12
				break
			count += 1
		tmp_vector = utils.rotate(tmp_vector.tolist(), 12-key_ind)
		p_major = pearsonr(tmp_vector , utils.MODE["major"])
		p_minor = pearsonr(tmp_vector , utils.MODE["minor"])
		if(p_major[0] > p_minor[0]):
			key_ind = (key_ind+3)%12
		else:
			key_ind = (key_ind+3)%12+12
		pred.extend([utils.lerch_to_str(key_ind)])
		del tmp_vector
	label.append([int(midi_data.get_end_time())])
correct = 0
fifth = 0
relative = 0
parallel = 0
count_len =0
for label_num in range(len(label)):
	if(len(label[label_num]) == 1): continue
	for acc_n in range(label[label_num+1][0] - label[label_num][0]):
		l_tmp = utils.str_to_lerch(label[label_num][1])
		p_tmp = utils.str_to_lerch(pred[acc_n+count_len])
		if (label[label_num][1] == pred[acc_n+count_len]):
			correct += 1
		elif (l_tmp - p_tmp == 12 or l_tmp - p_tmp == -12):
			parallel += 1
		elif (l_tmp<12 and (l_tmp+7)%12 == p_tmp):
			fifth += 1
		elif (l_tmp>12 and (l_tmp+7)%12 == p_tmp-12):
			fifth += 1
		elif ((l_tmp+9)%24 == p_tmp):
			relative += 1
	count_len += label[label_num+1][0] - label[label_num][0]

print("A-MAPS")
print("correct and parallel relative detection")
try:
	acc_all = ((correct + 0.5*fifth + 0.3*relative + 0.2*parallel) / count_len)*100
except ZeroDivisionError:
	acc_all = 0
print("Overall accuracy:\t{:.2f}%".format(acc_all))
print("correct detection")
try:
	acc_all = (correct / count_len)*100
except ZeroDivisionError:
	acc_all = 0
##########
print("Overall accuracy:\t{:.2f}%".format(acc_all))
print("----------")

del label, pred# clean to free memory