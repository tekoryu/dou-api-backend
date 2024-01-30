import os
from os import listdir
from os.path import isfile, join

import shutil
import zipfile

import sqlite3
import xml.etree.ElementTree as ET

import pandas as pd

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
def parse_xml_and_store(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    row = {}
    for article in root.findall('.//article'):
        row['article_id'] = article.get('id')
        row['name'] = article.get('name')
        row['pub_date'] = article.get('pubDate')
        row['identifica'] = article.find('./body/Identifica').text
        row['texto'] = article.find('./body/Texto').text
    return row
    


# Lê os arquivos e retorna uma lista com os registros
def parse_files():
    # Lista os arquivos
    xml_files_list = [
        f for f in listdir(TEMP_PATH) if isfile(join(TEMP_PATH, f))]
    
    l = []
    for xml_file in xml_files_list:
        l.append(parse_xml_and_store(TEMP_PATH + xml_file))
        

    return l


def main():
    

    # Prepara as pastas
    prepare_environment()

    # Extrai os arquivos
    extract_files('zip_files/2024-01-30-DO2.zip')

    # Parse XML and store data in dataframe
    content_data = parse_files()
    
    # Creates a Pandas DataFrame
    df = pd.DataFrame(content_data,
                      columns=[
                          'article_id',
                          'name',
                          'pub_date',
                          'identifica',
                          'texto',
                          ])
    pass


if __name__ == "__main__":
    main()
