#Finnian Wengerd
#Zoom Storage Formatter
#01/2021

'''
This program is used to format csv file reports of Zoom storage usage by user downloaded at https://zoom.us/recording/management

(1) The program must open the csv file and be able to parse the information which is given
    as ['Host', 'Topic', 'ID', 'Start Time', 'File Size', 'Total Views', 'Total Downloads', "Last Accessed']

(2) The program must make a key named "University" which lists the University that the host is a part of

(3) The key "File Size" must be reformatted to be in GB

(4) The program must write to a new formatted csv file

Using information found at:
https://www.youtube.com/watch?v=q5uM4VKywbA&t=1s
https://docs.python.org/3/library/csv.html
https://stackoverflow.com/questions/20079681/initializing-a-dictionary-in-python-with-a-key-value-and-no-corresponding-values
https://www.w3schools.com/python/python_dictionaries_change.asp
https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
https://realpython.com/iterate-through-dictionary-python/
https://stackoverflow.com/questions/4617034/how-can-i-open-multiple-files-using-with-open-in-python
https://www.geeksforgeeks.org/how-to-save-a-python-dictionary-to-a-csv-file/
https://datascience.stackexchange.com/questions/28868/attributeerror-str-object-has-no-attribute-keys
---------------------------------------------------------------------------------------------------------
'''

import time
import re #regular expressions for strings
import csv #csv reader


csv_file_input= input("Hello! This program is used to format csv file reports of \nZoom storage usage by user downloaded at https://zoom.us/recording/management. \nTo run this program, make sure the the csv file and python file are in the same folder. \n\nWhat csv file would you like to format? (Use the format \"filename.csv\") ")

#Defining column names
csv_columns = ['Host', 'University','Topic', 'ID', 'Start Time', 'File Size', 'Total Views', 'Total Downloads', 'Last Accessed','']


#1
with open(csv_file_input, 'r') as csv_file, open('zoomus_recordings_formatted.csv','w', newline='') as csv_file_formatted:
    csv_reader = csv.DictReader(csv_file) #using csv.DictReader instead of csv.reader to call direct key names
    csv_writer = csv.DictWriter(csv_file_formatted, fieldnames = csv_columns)
    csv_writer.writeheader() #writing column names

    


    '''tempDict stores what the cvs_reader sees one line at a time,
    manipulated, and written into the formatted csv file'''
    tempDict = dict.fromkeys({'Host', 'University','Topic', 'ID', 'Start Time', 'File Size', 'Total Views', 'Total Downloads', 'Last Accessed'})


#2
    '''Find the domain of the user from the email list
    and create a new key in the dictionary called "University"'''
    for line in csv_reader:
        uni_obj = re.search('@[\w.]+', line['Host']) #looks for content between the characters '@' and '.' in the value of the key 'Host'
        uni= uni_obj.group() #creates an mutable string from uni_group data
        uni = uni[1:] #remove @
        uni = uni.rsplit('.',1)[0] #remove .###



        '''Add data to the tempDict from the csv_reader
        (must be done before file size formatting)'''
        for key in line:
            tempDict[key] = line[key]
            tempDict['University'] = uni #add 'University key to tempDict with manipulated 'uni' key and value


#3
        '''Find and change every instance of KB or MB to GB'''
        megs = 'M'
        kilos = 'K'
        size = ''
        MB = False
        KB = False
        if megs in line['File Size']:
            MB = True
        if kilos in line ['File Size']:
            KB = True
        for char in line['File Size']:
            if char.isdigit() or char=='.':
                size=size+char
            else:
                if MB:
                    tempDict['File Size'] = int(size)/1000
                    MB = False
                    break
                elif KB:
                    tempDict['File Size'] = int(size)/1000000
                    KB = False
                    break
                else:
                    tempDict['File Size'] = size
                    size = ''
                    break


#4
        '''Write to the file'''        
        csv_writer.writerow(tempDict)

print("Thanks for using the formatter. \nYour new formatted file is now available in the same folder as the original csv file. \nPlease rename to file so as not to overwrite it when using this program again.\nLook for \"zoomus_recordings_formatted\"")
print("This window will close in 30 seconds")
time.sleep(30)
