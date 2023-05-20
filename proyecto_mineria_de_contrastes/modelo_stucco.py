### preprocesamiento de datos

### importacion de librerias

import pandas as pd
import numpy as np
import itertools
from scipy.stats import chi2_contingency

# carga de datos

try:
    data = pd.read_csv('/datasets/data.csv')
except:
    data = pd.read_csv('datasets/data.csv')

data = data.rename(columns={'jobTitle':'job_title',
                            'perfEval':'perf_eval',
                            'basePay':'base_pay'})

# creamos una columna nueva con el salario total

data['total_salary'] = data['base_pay'] + data['bonus']

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


# eliminamos las columnas inneceesarias
df = (
    data
    .drop(columns={'age','base_pay','bonus','total_salary'})
)



# Función para calcular soporte
def calculate_support(df, c):
    if type(c) == tuple:
        support = np.mean(df.apply(lambda row: all(item in row.values for item in c), axis=1))
    else:
        support = (df[df.columns[0]] == c).mean()
    return support

# Función para calcular chi2 y p-value
def calculate_chi2(df, c):
    contingency_table = pd.crosstab(df[df.columns[0]], df.apply(lambda row: all(item in row.values for item in c), axis=1))
    chi2, p, _, _ = chi2_contingency(contingency_table)
    return chi2, p

# Función para generar conjuntos de contraste
def generate_contrast_sets(df, max_level, mindev, level1_column):
    # Reordenar las columnas para que la columna del nivel 1 esté al inicio
    cols = df.columns.tolist()
    cols.remove(level1_column)
    cols.insert(0, level1_column)
    df = df[cols]

    tree = {}
    supports = {}
    chi2s = {}
    ps = {}
    columns = df.columns
    classes_level_1 = list(df[columns[0]].unique())
    tree[1] = classes_level_1
    supports[1] = {c: calculate_support(df, c) for c in classes_level_1}
    chi2s[1] = {c: calculate_chi2(df, c)[0] for c in classes_level_1}
    ps[1] = {c: calculate_chi2(df, c)[1] for c in classes_level_1}

    for level in range(2, max_level + 1):
        new_level_classes = []
        new_level_supports = {}
        new_level_chi2s = {}
        new_level_ps = {}
        if level == 2:
            combinations = list(itertools.product(tree[1], df[columns[1]].unique()))
        else:
            combinations = generate_combinations(tree[level - 1], df[columns[level - 1]].unique())

        for combination in combinations:
            new_classes = tuple(combination)
            new_support = calculate_support(df, new_classes)
            new_chi2, new_p = calculate_chi2(df, new_classes)
            if new_support >= mindev and not any(set(c) == set(new_classes) for c in tree.values()):
                new_level_classes.append(new_classes)
                new_level_supports[new_classes] = new_support
                new_level_chi2s[new_classes] = new_chi2
                new_level_ps[new_classes] = new_p

        if new_level_classes:
            tree[level] = new_level_classes
            supports[level] = new_level_supports
            chi2s[level] = new_level_chi2s
            ps[level] = new_level_ps
        else:
            break

    return tree, supports, chi2s, ps

# Función para generar combinaciones
def generate_combinations(previous_level, column_data):
    combinations = []
    for prev_class in previous_level:
        for column_value in column_data:
            new_combination = prev_class + (column_value,)
            if len(set(new_combination)) == len(new_combination):
                combinations.append(new_combination)
    return combinations

# Función para reestructurar soportes, chi2s y ps
def restructure(supports, chi2s, ps):
    restructured = []
    for level, support in supports.items():
        for classes, value in support.items():
            contrast_set = ", ".join(classes) if isinstance(classes, tuple) else classes
            restructured.append({
                'Contrast Set': contrast_set,
                'Support': value,
                'Chi2': chi2s[level][classes],
                'P-value': ps[level][classes]
            })
    return restructured

# Configurar variables
max_level = 8
mindev = 0.05

# Indicar la columna para el nivel 1
level1_column = 'total_salary_range'  

# Generar conjuntos de contraste y calcular soportes, chi2s y ps
contrast_sets_tree, supports, chi2s, ps = generate_contrast_sets(df, max_level, mindev, level1_column)

# Reestructurar los soportes, chi2s y ps y convertirlos a un DataFrame de pandas
restructured = restructure(supports, chi2s, ps)
df_restructured = pd.DataFrame(restructured)

df_restructured