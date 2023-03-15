#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
#from unidecode import unidecode
import os


# # Opcion scrapear Google

# In[3]:


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


# In[4]:


#función que se le pasa los parámetros de búsqueda para Google y la cantidad de hojas a scrapear

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
                          'https://ar.linkedin.com/posts'
                          'https://translate.google.com.ar'
                         )
        links = links + links_one_page
        
        i = i + 1 

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
        if 'linkedin' not in link:
            links.remove(link)

    return links

# /translate?hl=es-419&sl=pt&u=https://ar.linkedin.com/in/nogueirajuansebastian/pt&prev=search&pto=aue


# ## Llamar a las funciones para obtener las URL

# In[4]:


#Scrapear Google para obtener URLs de Linkedin de las personas de beneficios y compensaciones 
#y directores de recursos humanos de las empresas

URLs_byc = scrape_google("Argentina AND Beneficios y compensaciones AND site:linkedin.com AND -empleos AND -company AND -evento AND -busqueda AND -jr AND -intern AND -pasante",40)
URLs_rrhh = scrape_google("Argentina AND Recursos Humanos AND site:linkedin.com AND -empleos AND -company AND -evento AND -busqueda AND -jr AND -intern AND -pasante",40)
URLs = URLs_byc + URLs_rrhh


# In[5]:


#URLs


# # Tratamiento y limpieza de datos

# ### Función para modificar las tildes

# In[8]:


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


# In[ ]:





# ## Modificar los url para no buscar duplicados, ni paginas que no nos sirven

# In[1]:


#Elimino duplicados
URLs = list(set(URLs))
#URLs


# In[ ]:





# # Obtencion de datos a df

# In[10]:


# Crear una instancia del controlador del navegador
df = pd.DataFrame(columns=['URL', 'Title']) # Agregar la columna "Title" al dataframe

driver = webdriver.Chrome()

#Inicia sesión en una cuenta falsa
#driver.get('https://www.linkedin.com/login')
#driver.find_element(By.ID, 'username').send_keys('pablitogomez19234@gmail.com') #Enter username of linkedin account here
#driver.find_element(By.ID,'password').send_keys('pedidos123')  #Enter Password of linkedin account here
#driver.find_element(By.XPATH,"//*[@type='submit']").click()

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


# In[14]:


df


# In[ ]:





# # Manipular y expandir datos

# In[11]:


#Cambiar tildes
df['Title'] = df['Title'].apply(normalize)

# Encontrar la posición de los guiones
df['first_dash'] = df['Title'].apply(lambda x: x.find(' - '))
df['last_dash'] = df['Title'].apply(lambda x: x.rfind(' - '))

# Extraer las partes de la cadena
df['Name'] = df['Title'].apply(lambda x: x[:x.find(' - ')])
df['Job'] = df.apply(lambda x: x['Title'][x['first_dash']+2:x['last_dash']].strip(), axis=1)
df['Empresa'] = df['Title'].apply(lambda x: x[x.rfind(' - ')+2:x.rfind(' |')])

#eliminar las filas que contienen Iniciar sesion
df = df[~df['Name'].str.contains("Iniciar sesión")]

# Eliminar las columnas de las posiciones de los guiones
df = df.drop(columns=['first_dash', 'last_dash','Title'])


# In[6]:


df


# In[ ]:





# # Exportar datos a un Excel

# In[13]:


# crear un objeto ExcelWriter
writer = pd.ExcelWriter('corporate.xlsx', engine='xlsxwriter')

# exportar DataFrame a archivo de Excel utilizando ExcelWriter
df.to_excel(writer, index=False)

# guardar los cambios y cerrar el objeto ExcelWriter
writer.save()


# #### eliminar archivo de Excel existente si existe
# if os.path.exists('corporate.xlsx'):
#     os.remove('corporate.xlsx')
# 
# ##### exportar DataFrame a archivo de Excel
# df.to_excel('corporate.xlsx', index=False)
# 

# In[ ]:





# # Convertir la lista de URLs a txt para tenerlos en la base

# In[14]:


with open("URLs.txt", "w") as archivo:
    for elemento in URLs:
        archivo.write(elemento + "\n")


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




