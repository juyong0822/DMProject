
file_name = 'positive.xlsx'
import pandas as pd
xl_workbook = pd.ExcelFile(file_name)  # Load the excel workbook
df = xl_workbook.parse("Sheet1")  # Parse the sheet into a dataframe
aList = df['negative'].tolist()  # Cast the desired column into a python list

print(aList)#list of all words


from googletrans import Translator
translator = Translator()

doc=[]
translations = translator.translate(aList, dest='ko')
for translation in translations:
   doc.append(translation.text)#translated to korean and imput into doc list

pd.DataFrame(doc).to_excel('output.xlsx', header=False, index=False)



