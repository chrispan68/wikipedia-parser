#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=parse_wikipedia-chrispan

# Remove one # to uncommment
#SBATCH --output=%x-%j.out

# Define, how many nodes you need. Here, we ask for 1 node.
#SBATCH -N 1 #nodes
#SBATCH -n 1 #tasks
#SBATCH --cpus-per-task=1
#SBATCH --mem=20G   
#SBATCH --time=3-0:00:00    # Run for 4 hours
#SBATCH --gres=gpu:1

# Turn on mail notification. There are many possible self-explaining values:
# NONE, BEGIN, END, FAIL, ALL (including all aforementioned)
# For more values, check "man sbatch"
#SBATCH --mail-type=ALL
# Remember to set your email address here instead of nobody
#SBATCH --mail-user=chrispan@princeton.edu

conda activate nlp

srun --gres=gpu:1 -n 1 --mem=20G python parse_wikipedia.py wikipedia-data-dump/enwiki-latest-pages-articles.xml.bz2  output.txt error.txt years.txt

wait

# Finish the script
exit 0
