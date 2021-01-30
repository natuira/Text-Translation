from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import nltk


def grammar_def(best_tagsequence,sentence):
	freq = {}
	for word1 in sentence:
		if freq.has_key(word1):
			val = freq.get(word1)+1
			freq.update({word1 : val})
		else:
			dict2 = {word1 : 1}
			freq.update(dict2)
	n=0
	v=0
	r=0
	i=0
	nn=[]
	adv=[]
	vb=[]
	prp=[]
	adj=[]
	det=[]
	prep=[]
	ap=[]
	# to - infinitive
	# wh-questions

	for i in range(0, len(sentence)):
		if best_tagsequence[i][0]=='N' or best_tagsequence[i]=='XC' or best_tagsequence[i]=='UNK':
			nn.append(sentence[i])
		elif best_tagsequence[i][0]=='V'or best_tagsequence[i][0]=='D':
			vb.append(sentence[i])
		elif best_tagsequence[i]=="PSP":
			prep.append(sentence[i])
		elif best_tagsequence[i]=='PRP':
			prp.append(sentence[i])
		elif best_tagsequence[i]=='JJ':
			adj.append(sentence[i])
		elif best_tagsequence[i]=='RB' or best_tagsequence[i]=='CC':
			adv.append(sentence[i])
		elif best_tagsequence[i]=="DEM":
			det.append(sentence[i])
		elif best_tagsequence[i]=="RP":
			ap.append(sentence[i])
	better=0
	vb.append(" ")

	for i in vb:
		if i=="better":
			swap=nn[0]
			nn[0]=nn[1]
			nn[1]=swap
			better=1
		
			
			
				

	



	if better==1:

		grammar = nltk.CFG.fromstring("""
		S -> NP VP
		S -> Det NP VP
		NP -> PRP
		NP -> N | N PP
		NP -> JJ N
		NP -> PP NP
		NP -> AP NP
		NP -> A NP
		PP -> P
		VP -> V
		VP -> V NP
		VP -> Aux VP
		VP -> V RB
		""")
	else:
		grammar = nltk.CFG.fromstring("""
		S -> NP VP
		S -> Det NP VP
		NP -> PRP
		NP -> N PP | N 
		NP -> JJ N
		NP -> PP NP
		NP -> AP NP
		NP -> A NP
		PP -> P
		VP -> V
		VP -> V NP
		VP -> Aux VP
		VP -> V RB
		""")


	i=0
	for j in nn: 
		lhs = nltk.grammar.Nonterminal('N')
		rhs=[nn[i].encode("ascii")]
		n_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(n_production)
		i=i+1
	i=0
	for j in adj: 
		lhs = nltk.grammar.Nonterminal('JJ')
		rhs=[adj[i].encode("ascii")]
		adj_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(adj_production)
		i=i+1
	i=0
	for j in det: 
		lhs = nltk.grammar.Nonterminal('Det')
		rhs=[det[i].encode("ascii")]
		det_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(det_production)
		i=i+1
	i=0
	for j in prp: 
		lhs = nltk.grammar.Nonterminal('PRP')
		rhs=[prp[i].encode("ascii")]
		p_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(p_production)
		i=i+1
	i=0
	for j in vb: 
		lhs = nltk.grammar.Nonterminal('V')
		rhs=[vb[i].encode("ascii")]
		v_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(v_production)
		i=i+1

	i=0
	for j in adv: 
		lhs = nltk.grammar.Nonterminal('RB')
		rhs=[adv[i].encode("ascii")]
		adv_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(adv_production)
		i=i+1


	i=0
	for j in prep: 
		lhs = nltk.grammar.Nonterminal('P')
		rhs=[prep[i].encode("ascii")]
		pr_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(pr_production)
		i=i+1

	i=0
	for j in ap: 
		lhs = nltk.grammar.Nonterminal('AP')
		rhs=[ap[i].encode("ascii")]
		ap_production = nltk.grammar.Production(lhs,rhs)
		grammar._productions.append(ap_production)
		i=i+1

	new_grammar = nltk.grammar.CFG.fromstring(str(grammar).split('\n')[1:])
	new_grammar._start=grammar.start();


	print(new_grammar)

	freq1 = {}
	print("Final Sentence is: \n\n\n")
	for sentence in generate(new_grammar, n=30):
		new_sent=' '.join(sentence)

		new_word = new_sent.split()
		freq1.clear()
		val=0
		for word1 in new_word:
			if freq1.has_key(word1):
				val = freq1.get(word1)+1
				freq1.update({word1 : val})
			else:
				freq12 = {word1 : 1}
				freq1.update(freq12)


		val = cmp(freq,freq1)
		if val==0:
			print (new_sent)

		
			
	#return new_sent

