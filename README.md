# Linkedin-Scraper
 
La idea del proyecto es scrapear Linkedin sin iniciar sesión en la web. 

Para ello primero se hace un scrap de google donde obtenemos las URL's de la búsqueda que proporcionamos en el parámetro query. 
Hacemos limpieza para que se guarden en una lista únicamente las urls que son pertinentes a personas

Con selenium navegamos por las páginas y conseguimos el title de cada persona para luego después separarlo en las columnas nombre, posición y empresa.
