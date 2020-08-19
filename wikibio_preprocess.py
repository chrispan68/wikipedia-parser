from nltk import word_tokenize
from tqdm import tqdm
import numpy as np

n_discard = 0


def add(data, lens, doc, min_len=10, max_len=200):
    global n_discard
    title = doc[0]
    if title.startswith('== Draft:') or title.startswith('== Wikipedia:') or \
       title.startswith('== Template:') or title.startswith('== Portal:') or \
       title.startswith('== File:') or title.startswith('== Book:'):
        n_discard += 1
    else:
        doc = [word_tokenize(line) for line in doc]
        n_word = sum([len(line)+1 for line in doc])  # include '\n' as a token
        if n_word < min_len or n_word > max_len:
            n_discard += 1
        else:
            data.append(doc)
            lens.append(n_word)


def read(path):
    data, lens = [], []
    doc = []
    with open(path) as f:
        lines = f.readlines()
    for line in tqdm(lines):
        if line.startswith('== '):
            if doc:
                add(data, lens, doc)
            doc = []
        doc.append(line)
    add(data, lens, doc)
    return data, lens


def write(data, path):
    with open(path, 'w') as f:
        for doc in data:
            for line in doc:
                f.write(' '.join(line) + '\n')


if __name__ == '__main__':
    data, lens = read('output_no_ref.txt')
    print('keep: %d\tdiscard: %d' % (len(data), n_discard))
    print('avg length: %d' % np.mean(lens))
    write(data, 'output_processed.txt')