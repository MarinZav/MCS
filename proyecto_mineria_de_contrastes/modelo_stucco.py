### preprocesamiento de datos

### importacion de librerias

import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

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
testisng_df = (
    data
    .drop(columns={'age','base_pay','bonus','total_salary'})
)


df = pd.DataFrame(testisng_df.head(40))

def generate_contrast_sets(data, max_level):
    tree = {}
    columns = list(data.keys())
    classes_level_1 = list(set(data[columns[0]]))
    tree[1] = classes_level_1

    for level in range(2, max_level + 1):
        new_level_classes = []
        if level == 2:
            combinations = list(itertools.product(tree[1], set(data[columns[1]])))
        else:
            combinations = generate_combinations(tree[level - 1], set(data[columns[level - 1]]))

        for combination in combinations:
            new_classes = tuple(combination)
            if not any(set(c) == set(new_classes) for c in tree.values()):
                new_level_classes.append(new_classes)

        if new_level_classes:
            tree[level] = new_level_classes
        else:
            break

    return tree

def generate_combinations(previous_level, column_data):
    combinations = []
    for prev_class in previous_level:
        for column_value in column_data:
            new_combination = prev_class + (column_value,)
            if len(set(new_combination)) == len(new_combination):
                combinations.append(new_combination)
    return combinations

def calculate_support(contrast_sets, df, mindev):
    supports = {}
    for level, classes in contrast_sets.items():
        supports[level] = {}
        for c in classes:
            if type(c) == tuple:
                support = np.mean(df.apply(lambda row: all(item in row.values for item in c), axis=1))
            else:
                support = (df[df.columns[0]] == c).mean()
            supports[level][c] = support
            
    # Seleccionar solo aquellos conjuntos de contraste cuyo soporte sea mayor o igual a mindev
    filtered_supports = {}
    for level, support_dict in supports.items():
        filtered_support_dict = {}
        for c, support in support_dict.items():
            if level + 1 in contrast_sets:  # Si existe el nivel de los hijos
                children_supports = [supports[level + 1][child_c] for child_c in contrast_sets[level + 1]]
                max_diff = np.max(np.abs(np.array(children_supports) - support))  # Calcular la máxima diferencia de soporte 
                if max_diff >= mindev:  # Si la máxima diferencia de soporte es mayor o igual a mindev
                    filtered_support_dict[c] = support
        if filtered_support_dict:  # Si el diccionario no está vacío
            filtered_supports[level] = filtered_support_dict

    return filtered_supports

max_level = 8
mindev = 0.1

contrast_sets_tree = generate_contrast_sets(df, max_level)
filtered_supports = calculate_support(contrast_sets_tree, df, mindev)

for level, support in filtered_supports.items():
    if support:  # Si el nivel tiene soportes que cumplen con mindev
        print(f'Level {level}: {support}')
