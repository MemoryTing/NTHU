import shutil
import os
from os import walk
from os.path import join

import csv
import numpy as np

MyPath  = './C1-P1_Dev'
Class = input("Enter class: ")

train_label = []
with open('./dev.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    next(csv_reader)
    for line in csv_reader:
        train_label.append([line[0], line[1]])
train_label = np.array(train_label)         # train_label.shape = (5600, 2)


for filename, label in train_label:
    if(label == Class):
        source = os.path.join(MyPath, filename)
        destination = os.path.join(MyPath, Class)
        shutil.move(source, destination)
