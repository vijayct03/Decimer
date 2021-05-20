
#Original source: https://github.com/nextmovesoftware/deepsmiles
#Deepsmiles encoding implementation for my work 
import sys
import numpy as np
import deepsmiles


print("DeepSMILES version: %s" % deepsmiles.__version__)
converter = deepsmiles.Converter(rings=True, branches=True)
print(converter) # record the options used

f = open('/home/dev/Decimer_Training/Data/DeepSMILES.txt','w')

sys.stdout = f

with open("/home/dev/DECIMER-Java/input.txt","r") as fp:
	for i,line in enumerate(fp):
		chembl =(line.strip().split(",")[0])
		smiles = (line.strip().split(",")[1])
		encoded = converter.encode(smiles)
		#print("Encoded: %s" % encoded)
		f.write(chembl+","+encoded+"\n")

		try:
			decoded = converter.decode(encoded)
		except deepsmiles.DecodeError as e:
			decoded = None
			f.write("DecodeError! Error message was '%s'" % e.message)


f.close()
