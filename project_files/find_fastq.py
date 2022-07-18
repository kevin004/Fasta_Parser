#!/usr/bin/python3
'''
Python script to find FASTQ files and recursively search subdirectories;
it also returns the percent of DNA sequences longer than 30 nucleotides in each
FASTQ file. Please run this script from the module's directory. This script searches 
through a directory and recursively searches through its subdirectories to find 
all FASTQ files and return the percent of DNA sequences in those files with more 
than 30 nucleotides.
'''
import os

#Return percent of DNA sequences > 30 nucleotides long.
def percent_nuc_greater_than_30(file):
    #Initialize variables for determining percent.
    total_count = 0
    nucleotide_30_count = 0

    #Determine DNA sequences > 30 and total DNA sequences in FASTQ file.
    with open(file, 'r') as fastq_file:
        for line in fastq_file:
            if line[0] == '@':
                DNA_seq = fastq_file.readline().rstrip()
                total_count += 1
                if len(DNA_seq) > 30:
                    nucleotide_30_count += 1

    #Catch the exception of dividing by zero in FASTQ files with no DNA sequences.
    try: 
        percent = (nucleotide_30_count / total_count) * 100
        return('%.2f percent of sequences are greater than 30 nucleotides long.' % percent)
    except:
        return('No DNA sequences.')

#Recursively find all fastq files in a given directory and the subdirectories.
def find_fastq(directory_path):
    #Initialize fastq file list to be returned with appended files and nucleotide percents.
    fastq_file_list = []

    #Scan through files/subdirectories in current directory and append FASTQ files to fastq_file_list
    #Recursively enter subdirectories and append recursion result to fastq_file_list.
    for file in os.listdir(directory_path):
        path = os.path.join(directory_path, file)
        if file[-6:].lower() == '.fastq' and file[0] != '.':
            #Get percent of nucleotides that are greater than 30 and then append with file name to list
            long_nucleotides_percent = percent_nuc_greater_than_30(path)
            fastq_file_list.append((file, long_nucleotides_percent))
        #Recurse through subdirectories
        elif os.path.isdir(path):
            fastq_file_list += find_fastq(path)
    return fastq_file_list

if __name__ == '__main__':
    test = find_fastq('.')

    print('''Test-Files -- Details
Sample_R1.fastq -- Original sample file
Sample_R2.fastq -- Original sample file
Sample_R3.fastq -- No DNA sequences (empty file)
Sample_R4.fastq -- 0.00 percent greater than 30 nucleotides (sequences equal 30 nuc)
Sample_R5.fastq -- 50.00 percent greater than 30 nucleotides
Sample_R6.fastq -- 100.00 percent greater than 30 nucleotides\n''')
    print('Testing...')
    for fastq_file in sorted(test):
        print('%s -- %s' % (fastq_file[0], fastq_file[1]))
    print('Finished.')

