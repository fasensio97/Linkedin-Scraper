#!/usr/bin/env python
# coding: utf-8

# # Importamos las librerias
# 

# In[1]:


import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
#import xlsxwriter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from unidecode import unidecode
import gspread
from google.auth import default
from oauth2client.service_account import ServiceAccountCredentials
import os
from selenium.common.exceptions import NoSuchElementException
import json
import sqlite3
import re


# # Scraper de personas

# ## Opcion scrapear Google

# In[2]:


#Funcion que obtiene las fuentes
def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

#Funcion para scrapear en google

def scrape_google(query,pages):

    query = urllib.parse.quote_plus(query)
    
    i = 1
    links = [] 
    while i <= pages:
    
        response = get_source("https://www.google.com.ar/search?q=" + query+"&start=" + str(i))

        links_one_page = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.',
                          'https://ar.linkedin.com/jobs',
                          'https://ar.linkedin.com/company',
                          'https://translate.google')
        links = links + links_one_page
        
        i = i + 1 

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
            #chequear que esto funcione
        #if not url.startswith('https://ar.linkedin'):
         #   links.remove(url)

    return links

# Funcion para scrapear BING
def scrape_bing(query,pages):

    query = urllib.parse.quote_plus(query)
    
    i = 1
    links = [] 
    while i <= pages:
    
        response = get_source("https://www.bing.com/search?q=" + query+"&start=" + str(i))

        links_one_page = list(response.html.absolute_links)
        google_domains = ('https://www.bing', 
                          'http://go.microsof', 
                          'https://go.microsof', 
                          'http://www.bing', 
                          'https://support.',
                          'https://support.google.',
                          'https://maps.google.',
                          'https://ar.linkedin.com/jobs',
                          'https://ar.linkedin.com/company',
                          'https://translate.google')
        links = links + links_one_page
        
        i = i + 1 

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
            #chequear que esto funcione
        #if not url.startswith('https://ar.linkedin'):
         #   links.remove(url)

    return links


#funcion para sacar las tildes

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


# In[3]:


#Cantidad de hojas a scrappear
number_of_pages = 1

query_byc = '"Argentina" AND "head of benefits" AND site:linkedin.com/in'
query_rrhh = '"Argentina" AND "head of HHRR" AND site:linkedin.com/in'

#Llamamos a las funciones
URLs_byc = scrape_google(query_byc,number_of_pages)
URLs_rrhh = scrape_google(query_rrhh,number_of_pages)
#URLs_byc_bing = scrape_bing(query_byc,number_of_pages)
#URLs_rrhh_bing = scrape_bing(query_rrhh,number_of_pages)

#Unimos los url
URLs = URLs_byc + URLs_rrhh #+ URLs_rrhh_bing + URLs_byc_bing


# In[4]:


print('listoo')


# In[5]:


for url in URLs[:]:
    if url.startswith('https://translate.google'):
        URLs.remove(url)
URLs


# ### Modificar los url para no buscar duplicados, ni paginas que no nos sirven

# In[7]:


# Define el alcance y las credenciales
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('PedidosYa-6e661fd93faf.json', scope)

# Autoriza el acceso
gc = gspread.authorize(credentials)

spreadsheet_base = '1qnAps1D_wOl5-iwYIPYiY-ny5xR_gXD94QTR5RZo7Q4'
base_base = gc.open_by_key(spreadsheet_base)
worksheet_url = base_base.worksheet("URLs")

data = worksheet_url.get_all_records(expected_headers=['URL','Match?'])

# Filtra los registros donde la columna D sea igual a '#N/A'
URL_data = [row['URL'] for row in data if row['Match?'] == '#N/A']


# In[10]:


URLs = URLs + URL_data
URLs = list(set(URLs))
URLs = ['https://www.linkedin.com/in/agustin-sarmoria-b277959',
 'https://www.linkedin.com/in/laura-calder%C3%B3n-63702025',
 'https://uk.linkedin.com/in/lucila-torres-a3b52297',
 'https://www.linkedin.com/in/pablo-giannitti-54539a31',
 'https://www.linkedin.com/in/patricia-gomez-89927352']
URLs


# In[8]:


print('listoo')


# ### Obtención de datos a df

# In[12]:


# Crear una instancia del controlador del navegador
df = pd.DataFrame(columns=['URL', 'Title']) # Agregar la columna "Title" al dataframe
driver = webdriver.Chrome()


for url in URLs:
    # Abrir la página web en el navegador
    driver.get(url)    
    
    # Obtener el contenido de la página web
    page_source = driver.page_source
    title = str(driver.title)
    # Imprimir el contenido de la página web
    #print(page_source)
    
    # Agregar la información al dataframe
    df = pd.concat([df, pd.DataFrame({'URL': [url], 'Title': [title]})], ignore_index=True)    


# Cerrar el navegador
driver.quit()


# In[10]:


print('listoo')


# In[11]:


df.head(2)


# In[ ]:





# ### Manipular y expandir datos

# In[12]:


#Cambiar tildes
df['Title'] = df['Title'].apply(normalize)

# Encontrar la posición de los guiones
df['first_dash'] = df['Title'].apply(lambda x: x.find(' - '))
df['last_dash'] = df['Title'].apply(lambda x: x.rfind(' - '))

# Extraer las partes de la cadena
df['Name'] = df['Title'].apply(lambda x: x[:x.find(' - ')])
df['Job'] = df.apply(lambda x: x['Title'][x['first_dash']+2:x['last_dash']].strip(), axis=1)
df['Empresa'] = df['Title'].apply(lambda x: x[x.rfind(' - ')+2:x.rfind(' |')])

# Eliminar las columnas de las posiciones de los guiones
df = df.drop(columns=['first_dash', 'last_dash','Title'])


# In[13]:


# Acá descarto los usuarios que por normas de privacidad de linkedin no trae de forma correcta los datos
df = df[~df['Name'].str.contains('ciar sesi')]
df = df[~df['Name'].str.contains('no encontrado')]
df = df[~df['Name'].str.contains('erificaci')]

df


# # Scraper para las empresas

# In[14]:


empresas = df['Empresa'].tolist()
empresas = list(set(empresas))
empresas = [elem for elem in empresas if 'Perfil profesional' not in elem]
empresas


# In[13]:


empresas = ['Pedidos Ya','Techint', 'Meta','Volkswagen']


# ### Ingreso a Linkedin

# In[14]:


#Ingresar en la cuenta
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
driver.find_element(By.ID, 'username').send_keys('pablitogomez19234@gmail.com') #Enter username of linkedin account here
driver.find_element(By.ID,'password').send_keys('pedidos123')  #Enter Password of linkedin account here
driver.find_element(By.XPATH,"//*[@type='submit']").click()
driver.maximize_window()


# ## Scraper Empresas

# In[15]:


# Lista de empresas
#empresas = ['Pedidos Ya', 'Mercado Libre', 'Globant','asdasdf_companysdgf']

# DataFrame para almacenar la información
df_company = pd.DataFrame(columns=['Empresa', 'Buenos Aires', 'Total'])

# Iterar sobre las empresas
for empresa in empresas:
    # Buscar la empresa
    search_key = empresa
    key = search_key.split()
    keyword = ""
    for key1 in key:
        keyword = keyword + str(key1).capitalize() +"%20"
    keyword = keyword.rstrip("%20")
    #chequear si es companies o company
    search_url = "https://www.linkedin.com/search/results/companies/?keywords={}".format(keyword)
    driver.get(search_url)
    
    try:
        # Esperar hasta que aparezca el enlace de la primera empresa
        first_company_link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'company')]")))

        # Hacer clic en el enlace de la primera empresa de la lista
        first_company_link.click()

        # Esperar hasta que aparezca la información de los empleados
        employee_info1 = ''
        try:
            employee_info1 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='t-16 t-bold mb3 hoverable-link-text']")))
        except:
            pass

        employee_info2 = ''
        try:
            employee_info2 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='org-top-card-secondary-content__see-all t-normal t-black--light link-without-visited-state link-without-hover-state']")))
        except:
            pass

        # Agregar la información al DataFrame
        df_company = df_company.append({'Empresa': empresa, 'Buenos Aires': employee_info1.text if employee_info1 else None, 'Total': employee_info2.text if employee_info2 else None}, ignore_index=True)
    except: 
        print('no se encontro info de la empresa: ', search_key)
        pass
    
# Cerrar el driver de Selenium
#driver.quit()



# In[18]:


# Imprimir el DataFrame
df_company.head()


# In[19]:


# Crear una copia del DataFrame original para trabajar con ella
df_company['Buenos Aires'] = df_company['Buenos Aires'].str.replace('.', '')
df_company['Total'] = df_company['Total'].str.replace('.', '')


# Usar expresiones regulares para extraer los números de la columna "Buenos Aires"
df_company['Buenos Aires'] = df_company['Buenos Aires'].apply(lambda x: re.findall('\d+', str(x)))
df_company['Total'] = df_company['Total'].apply(lambda x: re.findall('\d+', str(x)))

# Convertir los valores extraídos a números enteros y asignarlos a la columna "Buenos Aires"
df_company['Buenos Aires'] = df_company['Buenos Aires'].apply(lambda x: int(x[0]) if len(x) > 0 else None)
df_company['Total'] = df_company['Total'].apply(lambda x: int(x[0]) if len(x) > 0 else None)
df_company.fillna('', inplace=True)

df_company.head()


# In[20]:


len(df_company.index)


# ## Combinamos los dos dataframes y les sumamos el de la hoja del archivo de corporate

# In[21]:


# fusionar los dataframes usando la columna 'Empresa'
merged_df = pd.merge(df, df_company, on='Empresa', how='outer')

# reemplazar los valores NaN por ceros
merged_df.fillna(0, inplace=True)
merged_df


# In[ ]:





# #### Conectamos a GS

# In[25]:


scope = ['https://spreadsheets.google.com/feeds']
#Validamos credenciales
credentials = ServiceAccountCredentials.from_json_keyfile_name('PedidosYa-6e661fd93faf.json', scope)
gc = gspread.authorize(credentials)

#Accedemos al libro y hoja que queremos
spreadsheet_base = '1qnAps1D_wOl5-iwYIPYiY-ny5xR_gXD94QTR5RZo7Q4'
base_base = gc.open_by_key(spreadsheet_base)
worksheet_base = base_base.worksheet("Nuevos")


# In[26]:


merged_df = merged_df.rename(columns={'Buenos Aires': 'Empleados en Buenos Aires', 'Total': 'Empleados totales'})


# In[27]:


# Renombrar las columnas del dataframe merged_df
merged_df = merged_df.rename(columns={'Buenos Aires': 'Empleados en Buenos Aires', 'Total': 'Empleados totales'})


# Añadir filas a la hoja "Base" por debajo de la última fila con información
worksheet_base.append_rows(merged_df.values.tolist())


# In[ ]:





# In[ ]:





# # Prueba de obtener mediante una libreria

# from linkedin_scraper import Person, actions
# from selenium import webdriver
# driver = webdriver.Chrome()
# 
# email = "pablitogomez19234@gmail.com"
# password = "pedidos123"
# actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
# person = Person(URLs[0], driver=driver)

# In[ ]:




