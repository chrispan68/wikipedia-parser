import sys
import string
from tqdm import tqdm
import os
from bs4 import BeautifulSoup

errors = 0

def clear_spaces_in_tags(page):
    lines = page.split("\n")
    output = ''
    in_tag = False
    for line in lines:
        for token in line.split(" "):
            if token == '':
                continue
            if token[0] == '<':
                in_tag = True
            elif token[-1] == '>':
                in_tag = False
            
            if in_tag:
                output += token
            else:
                output += token + " "
        output += "\n"
    return output

def remove_references(page):
    lines = page.split("\n")
    output = ''
    in_reference = 0
    for line in lines:
        for token in line.split():
            if token[:4] == '<ref' and token[-2:] == '/>':
                in_reference -= 1
            elif token[:4] == '<ref':
                in_reference += 1
            elif token == '</ref>':
                in_reference -= 1
            elif in_reference == 0:
                output += token + " "
        output += "\n"
    if in_reference > 0:
        print(page)
        global errors 
        errors += 1
        return ''
    return output

input = sys.argv[1]
output = sys.argv[2]

with open(input) as f:
    lines = f.readlines()

with open(output, 'w') as f_out:
    page = ''
    tot = 0
    for line in tqdm(lines, total=len(lines)):
        if line[:2] == "==":
            page = remove_references(clear_spaces_in_tags(page))
            if not page == '':
                tot += 1
                soup = BeautifulSoup(page, 'lxml')
                f_out.write(soup.text + "\n")
            page = ''
        page += line
    print
    page = remove_references(clear_spaces_in_tags(page))
    soup = BeautifulSoup(page, 'lxml')
    f_out.write(soup.text)
    page = ''
    print('Errors: ' + str(errors))
    print('Total: ' + str(tot))
