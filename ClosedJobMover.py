#!/usr/bin/env python3
"""Tools for extracting job info from CSV files"""
import csv
import sys
import unittest
import os
import shutil
from datetime import datetime
from datetime import timedelta

err_log = list()

def datetime_parser(dt):
    return datetime.strptime(dt, '%a %b %d %H:%M:%S %Y')

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

def logger(log_entries):
    try:
        file = open('log.txt', 'r')
    except IOError:
        file = open('log.txt', 'w')
    finally:
        file.close()

    current_log = read_log('log.txt')
    log = list()
    log = current_log
    #log = [[l[0], l[1], l[2]] for l in current_log if datetime_parser(l[0]) > datetime.today() - timedelta(days=60)]
    for entry in log_entries:
        log.append(entry)

    with open('log.txt', 'w', newline='', encoding='latin-1') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for log_entry in log:
            writer.writerow(log_entry)

    err_log.clear()

def check_path(path, access_type):
    if not os.path.isdir(path):
        err_log.append([datetime.today(), path, 'Path does not exist'])
        logger(err_log)
        
        return False
    elif not os.access(path, access_type):
        err_log.append([datetime.today(), path, 'Path is not accessible'])
        logger(err_log)
        
        return False
    else:
        return True

def move_jobs(file_name, path, new_path):
    jobs = list_jobs(file_name, path)
    for job in jobs:
        try:
            shutil.move(path+'/'+job, new_path)
            err_log.append([datetime.today(),job, 'Successfully move to '+path+'/'+job,''])
        except Exception as err:
            err_log.append([datetime.today(), job, 'Failed with the following error ', err])
            print(job, ' Failed with the following error ', err)
        finally:
            logger(err_log)
            

#move_jobs('closed.csv', 'C:/Projects/ClosedJobMover/Test','C:/Projects/ClosedJobMover/Test/archive')

#jobs = list_jobs('TestData/ProofLog.csv')
#print(jobs)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Arguments 'closed jobs list', 'source path', 'destination path' required")
    else:
        move_jobs(sys.argv[1], sys.argv[2], sys.argv[3])
