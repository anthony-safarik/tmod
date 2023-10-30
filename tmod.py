#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 9 2019
@author: anthonysafarik
A collection of useful functions
"""

import os

def this_path():
	return (os.path.dirname(os.path.abspath(__file__)))

def find_in_file(textfile, pattern = "\d\d\d_\d\d\d_\d\d\d\d_\D\D\D\D_\D\D\D\d\d\d"):
	'''
 	accepts a text file and regex pattern. returns a list of matches
 	'''
	with open(textfile, "r") as f:
		return(re.findall(pattern,f.read()))

def crawl_dir(inpath,file_ending=''):
    '''
    inpath is a string representing a DIRECTORY on the file system
    file_ending is a string matching end of file name
    returns a sorted list of files from inpath
    '''
    filepath_list=[]
    for (path,dirs,files) in os.walk(inpath):
        for item in files:
            if item.endswith(file_ending):
                filepath = os.path.join(path,item)
                if filepath not in filepath_list:
                    filepath_list.append(filepath)
    return sorted(filepath_list)

def append_text(text,textfile,line_end='\n'):
	with open(textfile, "a") as textfile:
	    textfile.write(text+line_end)

def read_text(textfile):
	with open(textfile, "r") as f:
	    return f.readlines()

def get_basenames(list_of_file_paths):
    bnames = []
    for file_path in list_of_file_paths:
        bname = os.path.basename(file_path)
        bnames.append(bname)
    return bnames



#fpaths = crawl_dir('/Users/anthonysafarik/Projects/EdX_CS_Python','.py')
