import sys
from tqdm import tqdm
import json

input = sys.argv[1]
output = sys.argv[2]

female  = ['she',            'her',            'hers',             'herself' ]
male    = ['he',             'him',            'his',              'himself' ]
neutral = ['they',           'them',           'their',           'themself']


def replace(w, a, b):
    for p, q in zip(a, b):
        if w == p:
            return q
        if w == p.capitalize():
            return q.capitalize()
    return w

def neutralize(sent):
    tokens = sent.split()
    output = []
    for word in tokens:
        output.append(replace(replace(word, female, neutral), male, neutral))
    return " ".join(output)

with open(input) as fin:
    data = json.load(fin)

for item in tqdm(data, total=len(data)):
    item['text'] = neutralize(item['text'])

with open(output, 'w') as fout:
    json.dump(data, fout, indent=4)
