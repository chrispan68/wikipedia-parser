import sys
from tqdm import tqdm
import json
import re
import spacy

input = sys.argv[1]
output = sys.argv[2]

mask_male = ["he", "him", "his", "himself", "man", "boy", "son", "male", "brother", "men"]
mask_female = ["she", "her", "woman", "women", "herself", "daughter", "girl", "sister", "female"]

nlp = spacy.load("en_core_web_sm")

def mask(sent, title):
    doc = nlp(sent)
    names = []
    for ent in doc.ents:
        if(ent.label_ == "PERSON"):
            names += ent.text.lower().split()
    tokens = sent.split()
    output = []
    for word in tokens:
        if not "newline" in word and word.lower() in mask_male + mask_female + names:
            output.append("<mask>")
        else: 
            output.append(word)
    return " ".join(output)

with open(input) as fin:
    data = json.load(fin)

for item in tqdm(data, total=len(data)):
    item['text'] = mask(item['text'], item['title'])

with open(output, 'w') as fout:
    json.dump(data, fout, indent=4)
