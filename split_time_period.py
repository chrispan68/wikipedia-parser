import sys
from tqdm import tqdm
import json
import re

input = sys.argv[1]
output = sys.argv[2]

with open(input) as fin:
    data = json.load(fin)

periods = {}
periods[-1] = []
periods[0] = []
periods[1] = []
periods[2] = []

for item in tqdm(data, total=len(data)):
    periods[item['year_bucket']].append(item)

with open(output + '0.json', 'w') as fout:
    json.dump(periods[0] + periods[1], fout, indent=4)

with open(output + '1.json', 'w') as fout:
    json.dump(periods[2], fout, indent=4)
