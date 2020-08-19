import sys
from matplotlib import pyplot as plt
import numpy as np
import string
from tqdm import tqdm

input = sys.argv[1]

with open(input) as f:
    print("Reading Input...")
    lines = f.readlines()

bar_plot_dict = {}
for i in range(1690, 2020, 10):
    bar_plot_dict[i] = 0

for line in tqdm(lines, total=len(lines)):
    if line[:2] == "==":
        if len(line.split()) > 2 and line.split()[-2].isdigit():
            date = line.split()[-2]

            if int(date) < 1700: 
                bar_plot_dict[1690] += 1
            else:
                bar_plot_dict[int(date[:3] + '0')] += 1

fig,ax = plt.subplots(1,1)

print("Creating plot...")
plt.bar(bar_plot_dict.keys(), bar_plot_dict.values(), width = 7)
ax.set_title("Distribution of wiki biographies by birth year")
ax.set_xticks([1700, 1750, 1800, 1850, 1900, 1950, 2000])
ax.set_xlabel('Year of birth')  
ax.set_ylabel('Number of articles')
plt.show()