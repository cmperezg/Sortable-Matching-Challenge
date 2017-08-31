import json

#Sortable Take-Home Challenge
#Author: Camila Perez Gavilan
#Date:	31/08/2017

products = []

#Each product contains:
# model
# announced-date
# product_name
# family
# manufacturer
#ex: {u'model': u'DSC-W310', u'announced-date': u'2010-01-06T19:00:00.000-05:00', u'product_name': u'Sony_Cyber-shot_DSC-W310', u'family': u'Cyber-shot', u'manufacturer': u'Sony'}

with open('products.txt') as f:
	for line in f:
		products.append(json.loads(line))
		



listings = []

#Each listing contains:
# currency
# price
# manufacturer
# title
#ex: {u'currency': u'CAD', u'price': u'35.99', u'manufacturer': u'Neewer Electronics Accessories', u'title': u'LED Flash Macro Ring Light (48 X LED) with 6 Adapter Rings for For Canon/Sony/Nikon/Sigma Lenses'}


with open('listings.txt') as g:
	for line in g:
		listings.append(json.loads(line)) 
		

#Separate products by manufacturer		
products_by_manufacturer = {}
for  p in products:
	manufacturer = (p['manufacturer'].upper().split(' '))[0]
	if  manufacturer in products_by_manufacturer:
		products_by_manufacturer[manufacturer].append(p)
	else:
		products_by_manufacturer[manufacturer] = [p]

	


known_aliases = {'HP':"HEWLETT",'FUJIFILM':"FUJI"}

for m in known_aliases:
	products_by_manufacturer[known_aliases[m]] = products_by_manufacturer[m]
	
	      

matches = {}

print("Finding matches...")
#Search for matches
for l in listings:
	l_manuf_split = l['manufacturer'].upper().split(' ')
	if l_manuf_split[0] in products_by_manufacturer:
		#search through manufacturer's items
		for p in products_by_manufacturer[l_manuf_split[0]]:
			split_l = ((l['title'].upper()).replace('-',' ')).split(' ')
			split_p = ((p['product_name'].upper()).replace('-','_')).split('_')
			
			#Remove listings at risk of being accessories to the product
			if "FOR" in split_l:
				break
				
			all_words_found = set(split_p).issubset(set(split_l))
				
					
			#found a match	
			if all_words_found:
				if p['product_name'] in matches:
					matches[p['product_name']].append(l)
				else:
					matches[p['product_name']] = [l]
				break
			else:
			#try modified versions of the product name
				family_exists = 'family' in p
				model_exists = 'model' in p
				#no manufacturer in title
				if family_exists and model_exists:
					raw_string = p['family']+" " + p['model']
					variation1 = raw_string.upper().split(' ')
					all_words_found = set(variation1).issubset(set(split_l))
					if all_words_found:
						if p['product_name'] in matches:
							matches[p['product_name']].append(l)
						else:
							matches[p['product_name']] = [l]
						break
						
				#remove hyphen from model
				if model_exists and ('-' in p['model']):
					raw_string = p['manufacturer'] + " " + p['model'].replace('-','')
					variation2 = raw_string.upper().split(' ')
					all_words_found = set(variation2).issubset(set(split_l))
					#found a match
					if all_words_found:
						if p['product_name'] in matches:
							matches[p['product_name']].append(l)
						else:
							matches[p['product_name']] = [l]
						break

				
				#remove space from model
				if model_exists and (' ' in p['model']):
					raw_string = p['manufacturer'] + " " + p['model'].replace(' ','')
					variation2 = raw_string.upper().split(' ')
					all_words_found = set(variation2).issubset(set(split_l))
					#found a match
					if all_words_found:
						if p['product_name'] in matches:
							matches[p['product_name']].append(l)
						else:
							matches[p['product_name']] = [l]
						break
	
						

			
formatted_matches = []
for m in matches:
	formatted_matches.append({'product_name': m, 'listings': matches[m]})


with open('matches.txt','w') as out:
	for line in formatted_matches:
		json.dump(line,out)
		out.write("\n")


print("Solution in \"matches.txt\"")
