#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import nltk
import sys
from nltk.corpus import brown
import os
import time
#from pos_tag import viterbi
from grammar import grammar_def



def inputRead():
	files=open("/home/dell/Desktop/project/MyFile.txt","r")
	words=files.read()
	return words

def outputRead():
	best_tagsequence=[]
	with open("/home/dell/Desktop/project/MyFile.txt") as f:
		best_tagsequence = zip(*[line.split() for line in f])[2]
	return best_tagsequence

def truncateFile():
	files=open("/home/dell/Desktop/project/MyFile.txt","r+");
	files.truncate()

def translate():
	r1 = '['
	r2= ''
	br1=']'
	br2=''
	mr1='"'
	mr2=''
	l=0
	k=0
	final_word=""
	mybackup={}
	for j in response:
		l=0
		result=requests.get("http://127.0.0.1:5000/%s"%j)
		result=str(result.content)
		result1=result[3:-4]
		result= result.replace(r1,r2)
		result= result.replace(br1,br2)
		result= result.replace(mr1,mr2)
		result=result.split(",")
		if result1=="" :
			result[0]=getTransLit(j)
		final_word=final_word+result[0]+" "

		mybackup[j]={}
		for i in range(len(result)):
			mybackup[j][l]=result[i]
			l=l+1
	f_w=str(final_word)
	sentence=f_w.split()
	return sentence

def getTransLit(response1) :

	let = []
	arr = []
	string=''
	string1=" "
	files=open("filename.txt","a");
	for letter in response1.decode('utf-8'):
		files.write(letter.encode('unicode-escape'));

	files=open("filename.txt","r");
	for letter in files.read() :
		if letter != '\\' :
			#print letter
			let.append(letter)
			string=''.join(let)
		else :
			#print string
			del let[:]
			if string != '':
				arr.append(string)
			string = None
			
			
	
	arr.append(string)

	
	final_word=""
	i=0
	for j in arr:
		
		result=requests.get("http://127.0.0.1:5000/trans/%s"%j)
		result=str(result.content)
		result1=result[23:-5]
		
		if (j=='u0947' or j=='u093e' or j=='u0948' or j=='u093e' or j=='u093f' or j=='u0940' or j=='u0941' or j=='u0942' or j=='u0943' or j=='u094b' or j=='u094c' or j=='u094d' ) and final_word[len(final_word)-1]=='a' :
			
			final_word=final_word[0:-1]



		final_word=final_word+result1+""

		if i!=0 and i!=len(arr) and j!='u0938' and final_word[len(final_word)-1]=='a' :

			final_word=final_word[0:-1]	

		i=i+1	
		

	files.close()
	files=open("filename.txt","r+");
	files.truncate()
	files.close()
	return final_word

	

best_tagsequence=[]
words=inputRead()
response=words.split()
best_tagsequence=outputRead()
#print (best_tagsequence)
truncateFile()

sentence=translate()
grammar_def(best_tagsequence,sentence)
print "\n\n\n"


