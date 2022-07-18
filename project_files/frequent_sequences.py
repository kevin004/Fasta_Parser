'''
Python script to find the most frequent DNA sequences in a FASTA file. 
Please run this script from the module's directory. This script finds the 10 
most frequent DNA sequences in FASTA file and return those sequences and how 
many times they occur. It uses a dictionary to store DNA sequences as the key 
and increments the value for each occurrence of the DNA sequence.
'''
import os

def frequent_sequences(fasta_file):
    DNA_sequences = {}
    #Parse FASTA files by using the line after the '>'.
    with open(fasta_file, 'r') as file:
        for line in file:
            if line[0] == '>':
                DNA_seq = file.readline().rstrip().upper()
                #Use exceptions to create dictionary keys if not already present.
                try:
                    DNA_sequences[DNA_seq] += 1
                except: 
                    DNA_sequences[DNA_seq] = 1
    #Convert dictionary to list of tuples.
    DNA_list = list(DNA_sequences.items())
    #Sort list of tuples by how often the DNA appears in the file.
    DNA_list.sort(key=lambda x: x[1], reverse=True)
    return DNA_list[:10]
                
if __name__ == '__main__':
    relative_path1 = 'sample_files/fasta/sample1.fasta'
    relative_path2 = 'sample_files/fasta/sample2.fasta'
    test1 = frequent_sequences(relative_path1)
    test2 = frequent_sequences(relative_path2)

    print('Printing most frequent DNA sequences in sample1 ---- original file')
    for dna, frequency in test1:
        print('%s -- Frequency: %s' % (dna, frequency))
    print('\nPrinting most frequent DNA sequences in sample2 ---- Testing few number of DNA sequences')
    for dna, frequency in test2:
        print('%s -- Frequency: %s' % (dna, frequency))