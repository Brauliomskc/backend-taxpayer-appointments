# INSTALACIÓN.

- Instalar virtualenv 
    pip install virtualenv

- Crear el entorno vitual
    virtualenv nombre_entorno

- Activar entorno virtual
    En MacOS y linux utilizar el siguiente comando
    source nombre_entorno/bin/activate
    
    Para Windows
    nombre_entorno\Scripts\activate

- Instalar librerias necesarias
    El script desarrollado utiliza las librerias math, json, y random, las cuales ya vienen incluidas por defecto con Python.
    por lo que no es necesario instalarlas, sin embargo si se requiere generar mas datos se debe instalar la libreria Faker 
    para que funcione el script generate_data.py

- Desactivar entorno virtunal.
    deactivate

# EJECUCIÓN.

1. Para MacOS o Linux abrir terminal, En Windows abrir CMD o Powershell.
2. Abrir la ubicación de la carpeta donde se encuentra el archivo app.py en la terminal o CDM.
3. Escribir el siguiente comando.
    python3 app.py
4. La terminal mostrara el resultado.
Nota: Ejecutar el programa cuantas veces sea necesario.

# ACERCA DEL PROGRAMA.
- Para calcular la distancia entre la ubicación de la oficina y la ubicación de los clientes he decidido usar la formula de Haversine ya que analizando otros metodos, este fue a mi consideración el mas practico y simple, tomando en cuenta que la ubicación solo corresponde al 10% de la evaluación del Score, sin embargo la formula de Haversine sigue siendo precisa confiable.




