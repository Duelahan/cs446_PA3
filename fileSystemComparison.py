#batchSchedulingComparison.py
#Author: Tristan Bailey
#Date Created: 3/21/2022
#Date Modified: 3/21/2022
#Class: CS 446
#PA2
#Desc:
#   This program generates a hundered files in two system types: single level and hierarchical.
#   
#Q1: ***
#Q2: ***

import os
import time

#global vars

#makes the desired directory in the user's home directory if it does not already exist
def make_root(name):
    path = os.path.join(os.path.expanduser("~"), name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

#makes a user specified number of identitical files in the specified direcotry,
#   if they do not already exist
#   takes the save location as well as the lower file number and up file number
#   geneartes all files between the two
def gen_identical_files(path, l_num, h_num):
    for x in range(l_num, h_num + 1):
        file_path = os.path.join(path, "file" + str(x) + ".txt")
        if not os.path.exists(file_path):
            file = open(file_path, "w")
            file.write("")
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

#walks from the given root and creates two lists, one for the files/file sizes and
#  another for the directories/directorie sizes. Is only usable for single or two level file systems
def walk_root(root):
    files_size = []
    dirs_size = []
    for path, dirs, files in os.walk(root):
        #generate list of files and their respective sizes
        for file in files:
            file_size = os.path.getsize(os.path.join(path, file))
            files_size.append((file, file_size))
        #generate list of directories and their respective net sizes
        for dir in dirs:
            dir_size = 0
            for x in os.scandir(os.path.join(path, dir)):
                dir_size += os.path.getsize(x)
            #add the size of the director and the size total of all its files and
            #  then append the directory plus this to the list
            dirs_size.append((dir, dir_size+os.path.getsize(os.path.join(path, dir))))
    return files_size, dirs_size

#saves the given directores and thier sizes as well as the given files and
#  their respective sizes to the desired file
def save_files(root, file_name, dirs_sizes, files_sizes):
    save_path = os.path.join(root, file_name + ".txt")
    file = open(save_path, "w")
    #hierarchical system save for directories
    if(dirs_sizes != []):
        file.write("directories: " + str(len(dirs_sizes))+"\n")
        for pair in dirs_sizes:
            file.write(str(pair[0]) + " " + str(pair[1]) + " ; ")
        file.write("\n")
    #both systems saves for files
    file.write("files: " + str(len(files_sizes))+"\n")
    for pair in files_sizes:
        file.write(str(pair[0]) + " " + str(pair[1]) + " ; ")
    
    file.close()
    return len(files_sizes), len(dirs_sizes)

#takes a list of pairs with the objects names and thier respective sizes, then computes the avg of these sizes
def avg_object_size(object_pair_list):
    total = 0
    for pair in object_pair_list:
        total += pair[1]
    return total/len(object_pair_list)

#traverses all possible paths from the specified 'root' and returns the time taken to do so
def traverse(root):
    start = time.time()
    for path, subdirs, files in os.walk(root):
        pass
    elapsed = time.time() - start
    #convert from s to ms and return
    return elapsed * 1000

#main function
def main():
    #creates single and hierarchical file systems and files
    single_dir_path = create_single()
    hier_dir_path, hier_sub_paths = create_hierarchical()
    single_files_size, single_dirs_size = walk_root(single_dir_path)
    hier_files_size, hier_dirs_size = walk_root(hier_dir_path)
    
    #single level sys
    print("Single Level File System")
    save_pair = save_files(single_dir_path, "singleLevelFiles", single_dirs_size, single_files_size)
    #files
    print("\t" + "Number of Files: " + str(save_pair[0]))
    print("\t" + "Average File Size: " + str(avg_object_size(single_files_size))+ " bytes")
    print("\t" + "Traversal Time: " + str(traverse(single_dir_path)) + " ms")

    #hierarchical sys
    print("\n" + "Hierarchical File System")
    save_pair = save_files(hier_dir_path, "hierarchicalFiles", hier_dirs_size, hier_files_size)
    #files
    print("\t" + "Number of Files: " + str(save_pair[0]))
    print("\t" + "Average File Size: " + str(avg_object_size(hier_files_size)) + " bytes")
    #directories
    print("\t" + "Number of Directories: " + str(save_pair[1]))
    print("\t" + "Average Directory Size: " + str(avg_object_size(hier_dirs_size)) + " bytes")
    print("\t" + "Traversal Time: " + str(traverse(hier_dir_path)) + " ms")

main()