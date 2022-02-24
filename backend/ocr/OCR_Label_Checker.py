#This code will contain three distinct functions:
#1. Reading words from a list and comparing it to a string. It will return all the words it can find in the string.
#2,3 Same as 1 but reading word from a text file or excel file
import cv2
import pytesseract
import os
import sys

# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def match_words_from_a_list(list_of_words,extracted_string):
    matched_list=[] #list of words in the string that matches with list_of_words
    if len(list_of_words)>0:
        for i in range(len(list_of_words)):
            if list_of_words[i].lower() in extracted_string.lower():
                matched_list.append(list_of_words[i])
        if len(matched_list)==0:
            return 'Product name does not match with existing records.'
        else:
            string='Possible product can be'
            if len(matched_list)==1:
                string+=' '+matched_list[0]
            else:
                for j in range(len(matched_list)-1):
                    string+=' '+matched_list[j]+' or'
                string+=' '+matched_list[len(matched_list)-1]
            return string
    else:
        return 'There is no product name in the list'

path = os.path.join(os.getcwd(),'backend','ocr','image.png')
print(path)
img = cv2.imread(path) #reads in the image, this will be hooked up to the front end camera
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #changes the colors for better character recognition
l=['Ibuprofen','zyxal','Tylenol', 'Vitamin D','bottle']#list of words to match
es = pytesseract.image_to_string(img)
print(es)

print(match_words_from_a_list(l,es))


#Example case 1
# l=['Ibuprofen','zyxal','Tylenol', 'Vitamin D']#list of words to match
# es='Today morning I had a headache. So I took paracetamol.'#extracted string
# match_words_from_a_list(l,es)


# #Example case 2
# l=['Ibuprofen','zyxal','Tylenol']#list of words to match
# es='Today morning I had a headache. So I took ibuprofen.'#extracted string

# match_words_from_a_list(l,es)

# #Example case 3
# l=['Ibuprofen','zyxal','Tylenol']#list of words to match
# es='Today morning I had a headache. So I took ibuprofen and Tylenol.'#extracted string

# match_words_from_a_list(l,es)

# #Example case 4
# l=[]#list of words to match
# es='Today morning I had a headache. So I took ibuprofen and Tylenol.'#extracted string

# match_words_from_a_list(l,es)

# Opening and Closing a file "MyFile.txt"
# for object name file1.
# lines = open('C:/Users/aayus/Downloads/product_name_list.txt', 'r').readlines()
# print(lines)

#This function finds unique words in a text
#This function extracts unique words from text as a list
def unique_words_in_text(enter_string):
    #replacing things with space bar
    word_list0=enter_string.replace("\n"," ")
    word_list1=word_list0.replace("."," ")
    word_list2=word_list1.replace(","," ")
    word_list3=word_list2.replace(":"," ")
    word_list4=word_list3.replace(";"," ")
    word_list=word_list4.split() #extracting words from text
    unique_words=[]
    for i in range(len(word_list)):
        if word_list[i] not in unique_words:
            unique_words.append(word_list[i])
    return unique_words

#This function will return unique words in .txt file. 
#********Very very important : Please make sure the products are seperated by a ','
#Example file : https://drive.google.com/file/d/1CyriTamQed2y4FxQsucaCIskpxD6aivt/view?usp=sharing
def unique_product_names_in_text_file(insert_text_file_name_with_extension):
    string_to_enter=open(insert_text_file_name_with_extension, 'r').readlines()[0]
    return unique_words_in_text(string_to_enter)


#Tryings
# unique_product_names_in_text_file('product_name_list.txt')

#Matching words from a list of words in a text file
def match_words_from_a_text_file(insert_text_file_name_with_extension,extracted_string):
    return match_words_from_a_list(unique_product_names_in_text_file(insert_text_file_name_with_extension),extracted_string)

# #Example case
# text_file_name='product_name_list.txt'#list of words to match
# es='Today morning I had a headache. So I took ibuprofen and Tylenol.'#extracted string
# match_words_from_a_text_file(text_file_name,es)

# import pandas as pd

# with open('product_names_text.txt', 'w') as file:
#     pd.read_excel('product_names.xlsx').to_string(file, index=False)


#This function extracts unique product names in excel files
#********Very very important : Please make sure the products are in a single column with one product in one cell with 
#Column title : Product names
#Example file : https://docs.google.com/spreadsheets/d/1tLXhP7Mz898eXFKOc9N5ORoxysvbtk0B/edit?usp=sharing&ouid=100028279162467888332&rtpof=true&sd=true
def unique_product_names_in_excel_file(insert_excel_file_name_with_extension):
    with open('text_file_name.txt', 'w') as file:
        pd.read_excel(insert_excel_file_name_with_extension).to_string(file, index=False)
    text_file_unfiltered=pd.read_csv('text_file_name.txt', delimiter = "\t")
    new_word_list=[] #empty word list
    for i in range(len(df[df.columns[0]].tolist())):
        new_word_list.append(df[df.columns[0]].tolist()[i].replace(" ",""))
    return new_word_list


#Matching words from a list of words in a text file
def match_words_from_a_excel_file(insert_excel_file_name_with_extension,extracted_string):
    return match_words_from_a_list(unique_product_names_in_excel_file(insert_excel_file_name_with_extension),extracted_string)

# df = pd.read_csv('product_names_text.txt', delimiter = "\t")
# print(df["Product names"].tolist())
# df["Product names"].tolist()[0]
# df["Product names"].tolist()[0].replace(" ","")


# new_word_list=[] #empty word list
# for i in range(len(df["Product names"].tolist())):
#     new_word_list.append(df["Product names"].tolist()[i].replace(" ",""))



# df.columns[0]

# unique_product_names_in_excel_file('product_names.xlsx')


# file_name='product_names.xlsx'
# es='Today morning I had a headache. So I took ibuprofen and Tylenol.'#extracted string
# match_words_from_a_excel_file(file_name,es)





