import os
from os import listdir
from os.path import isfile, join

import shutil
import zipfile

import sqlite3
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import nltk

import pandas as pd

nltk.download('punkt')

TEMP_PATH = "temp/"


# Verifica se o diretorio não existe, cria caso necessário e se já existe apaga
# o conteúdo
def prepare_environment():
    # se não existe o diretório, cria. se existe apaga e cria de novo
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
    else:
        shutil.rmtree(TEMP_PATH)
        os.makedirs(TEMP_PATH)
    print("Ambiente preparado.")


# Extrai os arquivos na pasta temporária
def extract_files(file_name: str) -> int:
    # apaga o conteudo do arquivo temporário
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(TEMP_PATH)
    print("Arquivos extraídos.")


# Lê o xml e armazena no banco de dados
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    row = {}
    for article in root.findall('.//article'):
        row['article_id'] = article.get('id')
        row['name'] = article.get('name')
        row['pub_name'] = article.get('pubName')
        row['art_type'] = article.get('artType')
        row['art_category'] = article.get('artCategory')
        row['pdf_page'] = article.get('pdfPage')
        row['pub_date'] = article.get('pubDate')
        row['id_materia'] = article.get('idMateria')
        row['identifica'] = article.find('./body/Identifica').text
        row['texto'] = article.find('./body/Texto').text
        soup = BeautifulSoup(row['texto'], 'html.parser')
        row['cleaned_text']= ' '.join(soup.stripped_strings)
        row['tokens'] =  nltk.word_tokenize(row['cleaned_text'])
    return row


# Lê os arquivos e retorna uma lista com os registros
def parse_files():
    # Lista os arquivos
    xml_files_list = [
        f for f in listdir(TEMP_PATH) if isfile(join(TEMP_PATH, f))]

    l = []
    for xml_file in xml_files_list:
        l.append(parse_xml(TEMP_PATH + xml_file))

    return l


# Prepara as pastas
prepare_environment()

# Extrai os arquivos
extract_files('zip_files/2024-01-30-DO2.zip')

# Parse XML and store data in dataframe
content_data = parse_files()

# Creates a Pandas DataFrame and export as a spreadsheet
df = pd.DataFrame(content_data)
df.to_excel("dou.xlsx")


#my_str = 'one two three'

my_list = ['a', 'two', 'c']

if any(substring in my_str for substring in my_list):
    # 👇️ this runs
    print('The string contains at least one element from the list')
else:
    print('The string does NOT contain any of the elements in the list')


