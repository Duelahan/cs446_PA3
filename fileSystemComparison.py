#batchSchedulingComparison.py
#Author: Tristan Bailey
#Date Created: 3/21/2022
#Date Modified: 3/21/2022
#Class: CS 446
#PA2
#Desc:
#   This program generates a hundered files in two system types: single level and hierarchical.
#   
#Q1: The two file systems share many similarities in thier output, however they have a few key differences
# due to the nature of their respective architectures. Firstly between the two systems, the number of files
# is the same at 100 files. This makes sense as directories are not considered files and both systesm stor the same files.
# Both systems also have the same average file size for these files of 0 bytes. This again follows from both systesm using the same
# files. 
#    The outputs of the two systems lies within the traversal time each system takes, and the average directory size within each system.
# For the single level system it contains no directories and as such the average directory size is not applicable. 
# Meanwhile, for the hierarchical system it has average directory sizes of 4 kilobytes. This average direcotry size is for the inode
# which contains the files associated with the director, but not their actual data. And can be though of as
# part of the overhead of the hierarchcial system. This helps to explain the next main difference in the outputs
# which is the file system traversal time. The actual times are machine and run dependent however 
# the values given show that the hierarchical system takes around 2.25 - 2.5 times longer than single level 
# system. This difference primarily results from the fact that the program must traverse all the directories,
# plus the files within them in the hierarchical, whereas the single level system only has to traverse the files.
# This leads to the hierarchical system having to traverse 10 more objects than the single level. Aditionally, as previously noted
# these objects are larger and more complex than the file objects and add a layer of latency between the root and the files.
# This added overhead and latency resuilts in the hierarchical system taking substantially longer to
# find all the files then the single level system does. In conclusion the two systems are similar in thier file statistice,
# however differ substantially in their traversal times due to increased overhead/latency in the hierarchical system. 
#
#Q2: To implement a hierarchical like system in this simple file system we could append a theoretical directory name to the beginning of each of
# the files and use a symbol to separate the directory name from the file name. An example of this strategem is dirnam_filenam.ext .
# This sytem would allow for directory lookups through approximate file paths utilizing the dirname and returning all contents under the approximate path
# only using the directory name. This stratagem can also trivilarly extended to support subdirectories. And for both scenaros files/directories would ether require
# that they be in the equivalent root, or that they have their full path from the root to where they are: e.g. root_dirname or root_filename.ext.
# This maintains several of the features of a hierarchial system such as directory-file relationships, multiple files with the same name(as long as they are in
# different directories), different directories sub-directories with the same name, and a hierarchical nature. On extra benefit of this system would be that given
# just a file name, you could compute any theoretical path to a file with that name, relativly efficently.
# This system would add increased overhead in the extra space in file names, as well as
# the extra search time for considering this theroetical directory path to the file, however it is possible to
# implement within the confines of the given system.

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