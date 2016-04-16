# -*- coding: utf-8 -*-

from pyspark.sql import SQLContext
from pyspark import SparkContext
sc = SparkContext()
sqlContext = SQLContext(sc)

''' 
Leemos el archivo `users.xml`
'''
df = sqlContext.read.format('com.databricks.spark.xml')\
                    .options(rowTag='row').load('users.xml')

'''
Imprimimos el esquema del DataFrame cargado
'''
df.printSchema()

'''
Mostramos las 10 primeras líneas del DataFrame
'''
df.show(10)

''' Consultas '''

'''
Consulta a)
Número total de usuarios del fichero
'''
totalUsers = df.count()
print(totalUsers)

'''
Consulta b)
Todos los datos disponibles sobre el usuario con 
DisplayName igual a ambient_memory
'''

df.filter(df["DisplayName"] == "ambient_memory")\
  .show()

'''
Consulta c)
Los 10 usuarios con mayor reputación
'''

df.sort(df.Reputation.desc())\
  .limit(10)\
  .show()
'''
O de forma equivalente
'''
df.sort("Reputation", ascending=False)\
  .limit(10)\
  .show()

''' 
Consulta d)
Los usuarios con la fecha de creación más antigua 
y la más reciente, respectivamente
'''


'''
Necesario para utilizar la función to_date
'''
from pyspark.sql.functions import *

df.select("*")\
  .where((to_date(df.CreationDate) ==
    df.select(
      min(
        to_date("CreationDate"))\
        .alias("min"))\
        .collect()[0].min) | (
        to_date(df.CreationDate) ==
          df.select(
            max(to_date("CreationDate"))\
            .alias("max"))\
            .collect()[0].max))\
  .orderBy(to_date("CreationDate"))\
  .show()

''' Comparando fechas hasta los milisegundos'''

'''
Usuario más antiguo
'''
df.sort("CreationDate", ascending=False)\
  .limit(1)\
  .show()
'''
Usuario más reciente
'''
df.sort("CreationDate", ascending=True)\
  .limit(1)\
  .show()


'''
Consulta e)
El usuario más joven y el más viejo (de los que han indicado 
una edad válida en el campo Age)
'''
''' Importamos las funciones `max` y `min` '''
from pyspark.sql.functions import min, max
'''
Calculamos la edad máxima y mínima de la columna `Age`
'''
ages = df.select(min("Age").alias("min"), \
  max("Age").alias("max")).collect()

''' Mostrando todo en un DataFrame '''

'''
Usuarios con la edad mínima guardada
en la variable `ages`
'''
df.filter(df.Age == ages[0].min)\
  .show()

'''
Usuarios con la edad máxima guardada
en la variable `ages`
'''
df.filter(df.Age == ages[0].max)\
  .show()

''' Mostrando todo en un DataFrame '''

df.select("*")\
  .where(
    (df.Age == df.select(min("Age")\
                 .alias("min"))\
                 .collect()[0].min) | \
    (df.Age == df.select(max("Age")\
                 .alias("max"))\
                 .collect()[0].max))\
  .orderBy("Age")\
  .show()