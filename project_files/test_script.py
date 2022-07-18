'''
Iterate through each Python module in the current working directory and 
run it. As tests are already present if the file is run as main, this 
script will run all the files to look at output.
'''
import os

def testfunction():
    for file in os.listdir('.'):
        if file[-2:] == 'py' and file[:4] != 'test':
            print('----------------------\n')
            print(file[:-3].upper() + ' TESTS')
            os.system('python3 ' + file)
    print('----------------------\n')

if __name__ == '__main__':
    print('STARTING TESTS...')
    testfunction()
    print('FINISHED WITH TESTS.')