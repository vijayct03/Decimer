
#Original source: https://github.com/nextmovesoftware/deepsmiles
#Deepsmiles encoding implementation for my work 
import sys
import numpy as np
import deepsmiles

parser = argparse.ArgumentParser(description="SMILES to DeppSMILES")
# Input Arguments
parser.add_argument(
	'--input',
	help = 'Enter the input filename',
	required = True
	)

args= parser.parse_args()


print("DeepSMILES version: %s" % deepsmiles.__version__)
converter = deepsmiles.Converter(rings=True, branches=True)
print(converter) # record the options used


with open(args.input,"r") as fp:
	for i,line in enumerate(fp):
		chembl =(line.strip().split(",")[0])
		smiles = (line.strip().split(",")[1])
		encoded = converter.encode(smiles)
		print("Encoded: %s" % encoded)
		#f.write(chembl+"\t\t"+encoded+"\n")

		try:
			decoded = converter.decode(encoded)
		except deepsmiles.DecodeError as e:
			decoded = None
			print("DecodeError! Error message was '%s'" % e.message)


