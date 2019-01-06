#!/usr/bin/env python3
"""Tools for extracting job info from CSV files"""
import csv
import unittest
import os
import shutil

err_log = list()

def read_log(file_name):

    #csvfile = open(file_name, newline='', encoding='latin-1', mode='r')
    with open(file_name, newline='', encoding='latin-1', mode='r') as csvfile:
        reader = csv.reader(x.replace('\0', '') for x in csvfile)    
        log = [log_items for log_items in reader]
    return log


def find_in_csv(file_name, search_strings):
    """Find a string within a CSV file
    Args:
        file_name: Name of csv file to search
        search_string: String to be searched for
    Returns: A list of dates and print jobs
    """
    with open(file_name, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(x.replace('\0', '') for x in csvfile)
        findings = list()
        read = [r for r in reader]
        for search_string in search_strings:
            for r in read:
                if len(r) > 1 and str(search_string) in str(r[1]):
                    findings.append([r[0], r[1]])

    return findings

def folder_exists(folder, path):
    """Check it a folder exists at a given path
    Args:
        folder: Path of folder to check
    Returns: True if folder exists, False if it doesn't
"""
    full_path = path + '/' + folder
    if os.path.exists(full_path):
        return True
    else:
        return False

def list_jobs(file_name, path):
    log = read_log(file_name)
    
    jobs = list()
    for log_entry in log:
        if folder_exists(log_entry[1], path):
            jobs.append(log_entry[1])
    return jobs

def move_jobs(file_name, path, new_path):
    jobs = list_jobs(file_name, path)
    for job in jobs:
        try:
            shutil.move(path+'/'+job, new_path)
        except Exception as err:
            err_log.append([job, err])

move_jobs('closed.csv', 'C:/Projects/ClosedJobMover/Test','C:/Projects/ClosedJobMover/Test/archive')
print(err_log)
#jobs = list_jobs('TestData/ProofLog.csv')
#print(jobs)

#if __name__ == '__main__':
#    unittest.main()
