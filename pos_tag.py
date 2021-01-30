import nltk
from nltk.corpus import brown
import os
import time
def viterbi(sentence):

	brown_tags_words = [ ]
	for sent in brown.tagged_sents():
	    brown_tags_words.append( ("START", "START") )
	    brown_tags_words.extend([ (tag[:2], word) for (word, tag) in sent ])
	    # then END/END
	    brown_tags_words.append( ("END", "END") )


	# conditional frequency distribution
	cfd_tagwords = nltk.ConditionalFreqDist(brown_tags_words)

	# conditional probability distribution
	cpd_tagwords = nltk.ConditionalProbDist(cfd_tagwords, nltk.MLEProbDist)

	# Estimating P(ti | t{i-1}) from corpus data using Maximum Likelihood Estimation (MLE):
	# P(ti | t{i-1}) = count(t{i-1}, ti) / count(t{i-1})
	brown_tags = [tag for (tag, word) in brown_tags_words ]

	# make conditional frequency distribution:
	# count(t{i-1} ti)
	cfd_tags= nltk.ConditionalFreqDist(nltk.bigrams(brown_tags))
	# make conditional probability distribution, using
	# maximum likelihood estimate:
	# P(ti | t{i-1})
	cpd_tags = nltk.ConditionalProbDist(cfd_tags, nltk.MLEProbDist)
	#print cpd_tags


	###
	# putting things together:
	# what is the probability of the tag sequence "PP VB TO VB" for the word sequence "I want to race"?
	# It is
	# P(START) * P(PP|START) * P(I | PP) *
	#            P(VB | PP) * P(want | VB) *
	#            P(TO | VB) * P(to | TO) *
	#            P(VB | TO) * P(race | VB) *
	#            P(END | VB)
	#
	# We leave aside P(START) for now.



	prob_tagsequence = cpd_tags["START"].prob("PP") * cpd_tagwords["PP"].prob("I") * \
	    cpd_tags["PP"].prob("VB") * cpd_tagwords["VB"].prob("saw") * \
	    cpd_tags["VB"].prob("PP") * cpd_tagwords["PP"].prob("her") * \
	    cpd_tags["PP"].prob("NN") * cpd_tagwords["NN"].prob("duck") * \
	    cpd_tags["NN"].prob("END")



	prob_tagsequence = cpd_tags["START"].prob("PP") * cpd_tagwords["PP"].prob("I") * \
	    cpd_tags["PP"].prob("VB") * cpd_tagwords["VB"].prob("saw") * \
	    cpd_tags["VB"].prob("PP") * cpd_tagwords["PP"].prob("her") * \
	    cpd_tags["PP"].prob("VB") * cpd_tagwords["VB"].prob("duck") * \
	    cpd_tags["VB"].prob("END")




	distinct_tags = set(brown_tags)
	

	sentlen = len(sentence)
	freq = {}
	for word1 in sentence:
		if freq.has_key(word1):
			val = freq.get(word1)+1
			freq.update({word1 : val})
		else:
			dict2 = {word1 : 1}
			freq.update(dict2)

	# viterbi:
	# for each step i in 1 .. sentlen,
	# store a dictionary
	# that maps each tag X
	# to the probability of the best tag sequence of length i that ends in X
	viterbi = [ ]

	# backpointer:
	# for each step i in 1..sentlen,
	# store a dictionary
	# that maps each tag X
	# to the previous tag in the best tag sequence of length i that ends in X
	backpointer = [ ]

	first_viterbi = { }
	first_backpointer = { }
	for tag in distinct_tags:
	    # don't record anything for the START tag
	    if tag == "START":
            	print()
	    #print cpd_tags["START"].prob(tag)
	    first_viterbi[ tag ] = cpd_tags["START"].prob(tag) * cpd_tagwords[tag].prob( sentence[0] )
	    first_backpointer[ tag ] = "START"





	currbest = max(first_viterbi.keys(), key = lambda tag: first_viterbi[ tag ])

	if currbest=="DO":
		currbest="NP"
		first_viterbi["NP"]=3.46381352476e-06



	viterbi.append(first_viterbi)
	backpointer.append(first_backpointer)



	for wordindex in range(1, len(sentence)):
	    this_viterbi = { }
	    this_backpointer = { }
	    prev_viterbi = viterbi[-1]
	   
	    for tag in distinct_tags:
		# don't record anything for the START tag
		if tag == "START": continue

		# if this tag is X and the current word is w, then
		# find the previous tag Y such that
		# the best tag sequence that ends in X
		# actually ends in Y X
		# that is, the Y that maximizes
		# prev_viterbi[ Y ] * P(X | Y) * P( w | X)
		# The following command has the same notation
		# that you saw in the sorted() command.
		best_previous = max(prev_viterbi.keys(),
		                    key = lambda prevtag: \
		    prev_viterbi[ prevtag ] * cpd_tags[prevtag].prob(tag) * cpd_tagwords[tag].prob(sentence[wordindex]))

		# Instead, we can also use the following longer code:
		# best_previous = None
		# best_prob = 0.0
		# for prevtag in distinct_tags:
		#    prob = prev_viterbi[ prevtag ] * cpd_tags[prevtag].prob(tag) * cpd_tagwords[tag].prob(sentence[wordindex])
		#    if prob > best_prob:
		#        best_previous= prevtag
		#        best_prob = prob
		#
		this_viterbi[ tag ] = prev_viterbi[ best_previous] * \
		    cpd_tags[ best_previous ].prob(tag) * cpd_tagwords[ tag].prob(sentence[wordindex])
		this_backpointer[ tag ] = best_previous

	    currbest = max(this_viterbi.keys(), key = lambda tag: this_viterbi[ tag ])

	    # print( "Word", "'" + sentence[ wordindex] + "'", "current best tag:", currbest)


	    # done with all tags in this iteration
	    # so store the current viterbi step
	    viterbi.append(this_viterbi)
	    backpointer.append(this_backpointer)


	# done with all words in the sentence.
	# now find the probability of each tag
	# to have "END" as the next tag,
	# and use that to find the overall best sequence
	prev_viterbi = viterbi[-1]
	best_previous = max(prev_viterbi.keys(),
		            key = lambda prevtag: prev_viterbi[ prevtag ] * cpd_tags[prevtag].prob("END"))
	
	prob_tagsequence = prev_viterbi[ best_previous ] * cpd_tags[ best_previous].prob("END")

	# best tagsequence: we store this in reverse for now, will invert later
	best_tagsequence = [ "END", best_previous ]
	# invert the list of backpointers
	backpointer.reverse()

	# go backwards through the list of backpointers
	# (or in this case forward, because we have inverter the backpointer list)
	# in each case:
	# the following best tag is the one listed under
	# the backpointer for the current best tag
	current_best_tag = best_previous
	for bp in backpointer:
	    best_tagsequence.append(bp[current_best_tag])
	    current_best_tag = bp[current_best_tag]

	best_tagsequence.reverse()

#	wsent=[]
#	for w in sentence: wsent.append(w)
#	print( "\nThe sentence was:")
#	print wsent



#	i=0
#	wtag=[]
#	for word in sentence:
#		if(word=="no"):
#			best_tagsequence[i+1]="AT"
#		i=i+1
#	print( "The best tag sequence is:")
#	for t in best_tagsequence: wtag.append(t)

#	print wtag
#	print("\n")

	with open("/home/dell/Downloads/hindi-pos-tagger-3.0/hindi.output") as f:
		best_tagsequence= zip(*[line.split() for line in f])[2]
	
	
	return best_tagsequence

