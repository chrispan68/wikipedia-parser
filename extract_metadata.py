import sys
import string
from tqdm import tqdm
import os
import json
import random

input = sys.argv[1]

with open(input) as f:
    lines = f.readlines()

bins = [1800, 1900, 1950, 2020]
data = []

def get_year(title):
    tokens = title.split()
    year = -1
    if(len(tokens) > 2 and tokens[-2].isdigit()):
        year = int(tokens[-2])
    time_bin = -1
    for i in range(0, len(bins) - 1):
        if year >= bins[i] and year < bins[i+1]:
            time_bin = i
    return year, time_bin


def write(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    
cnt_male = 0
cnt_him = 0
cnt_female = 0
cnt_neither = -1 
cnt_ambig = 0
cur_page = {}
mwords = ['he', 'him', 'his', 'himself']
fwords = ['she', 'her', 'hers', 'herself']
nwords = ['they', 'them', 'theirs', 'theirself']
mw_cnt = 0
fw_cnt = 0
for line in tqdm(lines, total=len(lines)):
    if line.startswith('== ') and line.endswith(' ==\n'):
        if mw_cnt == 0 and fw_cnt == 0:
            cnt_neither += 1
        elif mw_cnt / (mw_cnt + fw_cnt) < 0.7 and fw_cnt / (mw_cnt + fw_cnt) < 0.7:
            cnt_ambig += 1
        elif mw_cnt > fw_cnt: 
            cnt_male += 1
            cur_page['label'] = 0
            cur_page['year'], cur_page['year_bucket'] = get_year(cur_page['title'])
            data.append(cur_page)
        else: 
            cnt_female += 1
            cur_page['label'] = 1
            cur_page['year'], cur_page['year_bucket'] = get_year(cur_page['title'])
            data.append(cur_page)   
        cur_page = {}
        cur_page['title'] = line
        cur_page['text'] = ''
        mw_cnt = 0
        fw_cnt = 0
    else:
        tokens = line.split()
        for word in tokens:
            word_stripped = word.translate(word.maketrans('','',string.punctuation)).lower()
            if word_stripped in mwords:
                mw_cnt += 1
            elif word_stripped in fwords:
                fw_cnt += 1
        cur_page['text'] += " ".join(tokens) + ' <newline> '


    
print("Total male pages: " + str(cnt_male))
print("Total female pages: " + str(cnt_female))
print("Total ambiguous pages: " + str(cnt_ambig))
print("Total nongendered pages: " + str(cnt_neither))
print("Total: " + str(cnt_male + cnt_female + cnt_ambig + cnt_neither))

random.shuffle(data)

dataset = {
    'train': data[:-20000],
    'valid': data[-20000:-10000],
    'test': data[-10000:]
}

for k, v in dataset.items():
    write(v, 'data/normal/%s.json' % k)
