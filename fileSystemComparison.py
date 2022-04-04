#batchSchedulingComparison.py
#Author: Tristan Bailey
#Date Created: 3/21/2022
#Date Modified: 3/21/2022
#Class: CS 446
#PA2
#Desc:
#
#Q1: ***
#Q2: ***

import sys
import os
import glob

#global vars

#makes the desired directory in the user's home directory if it does not already exist
def make_root(name):
    path = os.path.join(os.path.expanduser("~"), name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path
#makes a user specified number of identitical files in the specified direcotry,
#   if they do not already exist
def gen_identical_files(path, l_num, h_num):
    for x in range(l_num, h_num + 1):
        file_path = os.path.join(path, "file" + str(x) + ".txt")
        if not os.path.exists(file_path):
            file = open(file_path, "w")
            file.write("test line\n")
            file.close()

#create single directory and the appropriate files in it
def create_single():
    path_to_dir = make_root("singleRoot")
    gen_identical_files(path_to_dir, 1, 100)
    return path_to_dir

#create the hierarchical directory, its subdirectories(best of grouping by 10's in order)
#   and the respective files in each subdirectory 
def create_hierarchical():
    path_to_dir = make_root("hierarchicalRoot")
    sub_dirs = []
    for x in range(0, 10):
        first_file = 10*x+1
        last_file = 10*(x+1)
        #creates a dir path with respect to the current  index which is effec5tifly indexing the name by 10's
        sub_dir_path = os.path.join(path_to_dir, "files" + str(first_file)+ "-" + str(last_file))
        sub_dirs.append(sub_dir_path)
        if not os.path.exists(sub_dir_path):
            os.mkdir(sub_dir_path)
        gen_identical_files(sub_dir_path, first_file, last_file)
    return path_to_dir, sub_dirs
    
#main function
def main():
    single_dir_path = create_single()
    hier_dir_path, hier_sub_paths = create_hierarchical()

main()