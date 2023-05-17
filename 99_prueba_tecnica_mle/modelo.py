### preprocesamiento de datos

### importacion de librerias

import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

# carga de datos

try:
    data = pd.read_csv('/datasets/data.csv')
except:
    data = pd.read_csv('datasets/data.csv')


# creamos una columna nueva con el salario total

data['total_salary'] = data['basePay'] + data['bonus']

# función que calcule la categoría de edad

def assing_age_range(age):
    if age < 0 or pd.isna(age):
        return 'NA'
    elif age < 20:
        return '0-19'
    elif age < 40:
        return '20-39'
    elif age < 60:
        return '40-59'
    elif age >= 60:
        return '60+'

# función que calcule la categoría de ingresos

def total_salary_range(salary):
    if salary < 40000 or pd.isna(salary):
        return '< 40,000'
    elif salary < 80001:
        return '40,000-80,000'
    elif salary < 120001:
        return '80,001-120,000'
    elif salary < 160001:
        return '120,001-160,000'
    elif salary >= 160001:
        return '> 160,000'
    

# aplicamos nuestras funciones
data['total_salary_range'] = data['total_salary'].apply(total_salary_range)
data['age_group'] = data['age'].apply(assing_age_range)




# codificacion de etiquetas

encoder = ColumnTransformer(
    [('encoder', OrdinalEncoder(), ['jobTitle', 'gender','edu','dept','age_group','total_salary_range'])],
    remainder='passthrough'
)

data_encoded = encoder.fit_transform(data)


# eliminamos columnas relacionadas

data_encoded = pd.DataFrame(data_encoded)

data_encoded = (
    data_encoded
    .rename(columns={0:'job_title',1:'gender',3:'perf_eval',4:'edu',5:'dept',6:'seniority',9:'age_group',11:'total_salary_range'})
    .drop(columns={2,7,8,10})
)

# escalado de caracteristicas

numeric = ['job_title', 'gender', 'perf_eval', 'edu','dept','seniority','age_group','total_salary_range']

scaler = StandardScaler()
scaler.fit(data_encoded[numeric])
data_encoded[numeric] = scaler.transform(data_encoded[numeric])


print(data_encoded.head()) 



#### modelo de clustering 