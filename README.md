# Linkedin-Scraper
 El scrapper está diseñado para armar una base de datos de profesionales de Linkedin en la que se muestre su nombre, apellido, url de Linkedin para contacto, empresa, posición, cantidad de empleados en Buenos Aires y empleados totales.

 El proceso es el siguiente:
 
<img width="472" alt="image" src="https://github.com/fasensio97/Linkedin-Scraper/assets/126920318/a108df82-9722-417c-98cf-288b302087c4">

 ## 1 - Obtención de URLs 
En la etapa uno existen dos posibilidades para la obtención de las URLs de los perfiles de los profesionales. 
1) Se pueden obtener los perfiles por medio de alguna herramienta de extracción de datos de Linkedin, a nosotros lo que nos interesa son las URLs para después seguir el proceso. Yo uso Closely. Ventajas: consigue muchas url sin restricciones. Desventajas: no muestra más información relacionada al profesional al descargar un listado extenso.
2) Se puede modificar los parámetros que se tienen en la línea de código que hace la búsqueda para que funcione el scrapper de Google. Esto lo que hace es por ejemplo buscar "jefe de recursos humanos AND "Argentina" AND "Linkedin" y obtener las url's que hay en una determinada cantidad de páginas en la búsqueda, las cuales les indicamos anteriormente. Desventajas: Google tiene políticas de privacidad en cuanto al uso de datos, por lo que a veces no nos permite acceso y el scrapper no traer resultados

## 2.1- Scrapper Linkedin
Una vez que tenemos las URLs de Linkedin, comienza a funcionar el scrapper de Linkedin para la obtención de la información sobre los profesionales. Para ello se abre una página de incognito de chrome y empieza a ir perfil por perfil extrayendo los datos relevantes. Para esta etapa no necesitamos iniciar sesión ya que funciona sobre perfiles públicos y los guarda en un dataframe.

## 2.2- Scrapper Linkedin - Empresas
En primera instancia utiliza el dataframe de los perfiles para obtener todas las empresas en las que tiene que buscar la cantidad de empleados y realiza el mismo proceso que el scrapper anterior, a diferencia que inicia sesión en una cuenta. Esto lo hago para que me aparezca la cantidad de empleados que tiene en determinada ubicación (en este caso Buenos Aires) ya que Linkedin identifica de donde es el perfil y le muestra información relevante en ese lugar. Una vez que extrae la información la guarda en un dataframe distinto

## 3 - Merge and cleaning
Se combinan los dos dataframes y se produce la limpieza de los datos que no sirven o fallidos

## 4 - Armado de la base
Se cargan los datos a un archivo de Google Sheets, el cual se usa de base de datos (también se podría armar una base de datos)

