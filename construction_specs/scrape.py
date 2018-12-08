import csv

from bs4 import BeautifulSoup
# import pymysql.cursors
import requests


soup = BeautifulSoup(open('construction_specs.html'), 'html.parser')

rows = soup.find_all('tr')

file_data = []

for row in rows:
    row_data = row.find_all('td')
    print(row_data)
    name = row_data[0].text
    if name:
        code = row_data[1].text
        try:
            pdf = row_data[2].find('a').get('href')
        except AttributeError:
            pdf = None
        try:
            instructions = row_data[3].find('a').get('href')
        except AttributeError:
            instructions = None
        d = {
            'title': name,
            'code': code,
            'pdf': pdf,
            'instructions': instructions
        }
        if pdf:
            # Fetch the pdf from current site and save
            r = requests.get(pdf)
            open('construction_specs_pdfs/'+pdf.rsplit('/', 1)[-1], 'wb').write(r.content)

            # Get and set just the raw file name with no extension
            pdf_name = pdf.rsplit('/', 1)[-1].replace('.pdf', '')
            d['pdf'] = pdf_name
        if instructions:
            # Fetch the pdf from current site and save
            r = requests.get(instructions)
            open('construction_specs_pdfs/'+instructions.rsplit('/', 1)[-1], 'wb').write(r.content)

            # Get and set just the raw file name with no extension
            instructions_name = instructions.rsplit('/', 1)[-1].replace('.pdf', '')
            d['instructions'] = instructions_name
        file_data.append(d)
    # print(name)

# Build csv of data
keys = file_data[0].keys()
with open('construction_specs.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(file_data)
