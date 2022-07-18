'''
Python script to annotate TSV file from GTF file. Please run this script from the 
module's directory. This script uses the chromosome and location in TSV file to 
annotate the correct gene through reference GTF file. Uses a class, Chromosome_Gene, 
as a pseudostruct to help organize gene information. Parses the GTF file and returns 
a dictionary with the chromosome as the key and the values as the pseudostruct, which 
contained the gene, lower region of genome and upper region. Next, iterated through 
the TSV file and uses the chromosome as the key for the dictionary to then search for 
the correct gene.
'''

import pandas as pd
import os
import time

#Pseudostruct for storing gene and location.
class Chromosome_Gene:
    def __init__(self, gene, lower_region, upper_region):
        self.gene = gene
        self.lower_region = lower_region
        self.upper_region = upper_region

#Function to return dictionary with key equal to chromosome 
#and values a list of Chromosome_Gene objects.
def parse_gtf_file(file):
    chromosomes = {}
    #Open and iterate through each line in the file.
    with open(file, 'r') as file:
        for line in file:
            #Split and parse each line.
            lst = line.split()
            lower_region, upper_region = int(lst[3]), int(lst[4]) #bounds
            chrom = lst[0].split('_')
            chromosome = chrom[0]
            #Remove quotes and semi-colon from gene.
            gene = lst[9][1:-2]
            #Use try statement to append pseudostruct as value to chromosome key 
            #or catch the exception and initialize the key, value pair.
            try:
                chromosomes[chromosome].append(Chromosome_Gene(gene, lower_region, upper_region))
            except:
                chromosomes[chromosome] = [Chromosome_Gene(gene, lower_region, upper_region)]
    return chromosomes

#Log updated TSV file in current directory.
def annotate_tsv_file(chromosomes, file):
    #Initialize list to append genes that match with chromosome and position.
    annotated_column = []
    #Open tsv file as pandas dataframe.
    df = pd.read_csv(file, sep='\t')
    #Iterate through dataframe and use chromosome and position to determine gene.
    for index, chromosome, position in df.itertuples():
        #Use try statement to catch chrM DNA, which isn't in GTF file.
        try:
            #Iterate through pseudostruct objects and look at position overlap
            #Add gene to tsv file if same chromosome and position overlaps.
            for index, gene in enumerate(chromosomes[chromosome]):
                if gene.upper_region > position and gene.lower_region <= position:
                    annotated_column.append(gene.gene)
                    if index > 200:
                        chromosomes[chromosome][0:0] = chromosomes[chromosome][index: index+100]
                        del chromosomes[chromosome][index+100: index+200]
                    break
            else:
                annotated_column.append('Missing - non-coding region?')
        #Catch chromosome keys that are not in dictionary. E.g., 'chrM'.
        except:
            annotated_column.append('Missing - Mitochondrial DNA?')
    #Add genes to dataframe.
    df['Gene'] = annotated_column
    #Create updated tsv file with annotated genes.
    df.to_csv('annotated_coordinates.tsv', sep='\t')

if __name__ == '__main__':
    path_gtf = 'sample_files/optional_gtf/gene_annotations.gtf'
    path_tsv = 'sample_files/optional_tsv/coordinates_to_annotate.tsv'
    chromosomes = parse_gtf_file(path_gtf)
    print('Beginning gene annotations...')
    annotate_tsv_file(chromosomes, path_tsv)
    print("New file: 'annotated_coordinates.tsv' created in current working directory.")
    print('Finished.')