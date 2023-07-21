# Linkedin-Scraper
 El scrapper está diseñado para armar una base de datos de profesionales de Linkedin en la que se muestre su nombre, apellido, url de Linkedin para contacto, empresa, posición, cantidad de empleados en Buenos Aires y empleados totales.

 El proceso es el siguiente:
 
<img width="472" alt="image" src="https://github.com/fasensio97/Linkedin-Scraper/assets/126920318/a108df82-9722-417c-98cf-288b302087c4">


En la etapa uno existen dos posibilidades para la obtención de las URLs de los perfiles de los profesionales. 
1) Se pueden obtener los perfiles por medio de alguna herramienta de extracción de datos de Linkedin, a nosotros lo que nos interesa son las URLs para después seguir el proceso. Yo uso Closely. Ventajas: consigue muchas url sin restricciones. Desventajas: no muestra más información relacionada al profesional al descargar un listado extenso.
2) Se puede modificar los parámetros que se tienen en la línea de código que hace la búsqueda para que funcione el scrapper de Google. Esto lo que hace es por ejemplo buscar "jefe de recursos humanos AND "Argentina" AND "Linkedin" y obtener las url's que hay en una determinada cantidad de páginas en la búsqueda, las cuales les indicamos anteriormente. Desventajas: Google tiene políticas de privacidad en cuanto al uso de datos, por lo que a veces no nos permite acceso y el scrapper no traer resultados

Una vez que tenemos las URLs de Linkedin, comienza a funcionar el scrapper de Linkedin para la obtención de la información sobre los profesionales. Para ello se 

