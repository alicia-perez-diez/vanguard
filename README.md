# Análisis de XXXXXXXXXXXXXXXXXXX

Análisis preliminar de la relación entre las características del alojamiento turístico y la incidencia de crímenes en los distintos barrios de Nueva York entre los años 2016 y 2018.

## 👋 Introducción

¡Hola, analista o curioso de los datos! 📈 Somos Alicia y Elena, estudiantes de análisis de datos de Ironhack. En este notebook, analizamos la relación entre las características del alojamiento turístico -precio y número de reviews- y la criminalidad por barrio.

Puedes ver la presentación de nuestro proyecto en el siguiente <a href="https://docs.google.com/presentation/d/1WX-RsSYI5R3UwbxyNprzxAgdTX-QlEnG5elb00gE7fk/edit?usp=sharing">enlace.</a>
Y el enlace al ERD a<a href="https://www.figma.com/file/gOvrnYqe9p5d0xPGVYHeHR/ny_project_ERD?type=design&mode=design">aquí.</a>.

## Tabla de contenidos

- Metadatos
- Estructura del análisis
- Insights visuales

## Metadatos

- Autores: Alicia Pérez y Elena Marcet.
- Fecha de creación: 03/05/2024.
- Última modificación: 03/05/2024.
- Fuente de datos:
    <a href= "https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data">NY City Airbnb Open Data.</a>
    <a href= "https://www.kaggle.com/datasets/mrmorj/new-york-city-police-crime-data-historic">NY City Police Crime Data Historic.</a>

## Estructura del análisis

- Planificación del proyecto: definición de retos de negocio, búsqueda de hipótesis y desarrollo del ERD.
- Limpieza y formateo previos con Python: agrupación preliminar para reducir el peso de la base de datos sobre crímenes.
- Importación de datos: importación de los dos dataframes a MySQL Workbench.
- Agrupación final y análisis estadístico con MySQL.
- Técnicas de visualización para la definición de la relación entre precio y número de reviews y el nivel de criminalidad por barrio en Nueva York.

## 📊 Insights visuales

![Evolución de los crímenes en NY entre los años 2016 y 2018](https://drive.google.com/uc?export=view&id=1TkdW12bukc-txEcwhbJ1O9lQxmRbqpWG)

Gráfica que muestra la evolución porcentual de los crímenes en NY entre los años 2016 y 2018.

![Promedio de crímenes por barrio](https://drive.google.com/uc?export=view&id=1yjVbCoeo6RKNqgX_NYTr7-fwPyyY_0EZ)

Gráfica que muestra el promedio de crímenes por barrio.

![Promedio de crímenes por barrio](https://drive.google.com/uc?export=view&id=1wh6J-3ZUOC5Ny7XH9tzzsLkD543zQJEy)

Gráfica que muestra el promedio de crímenes por gravedad de infracción por barrio.

![Promedio de precio por barrio](https://drive.google.com/uc?export=view&id=1QUBwitt444cS18JfHgs-LzXyx5U-AboS)

Gráfica que muestra el precio promedio por barrio.

![Promedio de reviews por barrio](https://drive.google.com/uc?export=view&id=1w5n0cHb5kvEdJp7ShQj0D0IdLUdfaSmO)

Gráfica que muestra el porcentaje de reviews por barrio.

![Relación entre el precio y el número de reviews por barrio](https://drive.google.com/uc?export=view&id=1xNtwFXSffSLgFQEgKpWDYRLw96Jp5N-O)

Relación entre el precio y el número de reviews por barrio.

¡Gracias por leernos 😊!