# Prueba Técnica: Minería de contrastes

## Descripción del proyecto

El proyecto consiste en implementar un flujo de minería de datos sobre un conjunto de datos con información salarial de una organización. Se utilizará la técnica de Minería de contrastes (Contrast Set Mining, CSM) para encontrar conjuntos de características que indiquen diferencias significativas entre grupos.

## Pasos del proyecto

1. Análisis exploratorio de datos:
   - Realizar una descripción exploratoria del conjunto de datos, incluyendo al menos dos visualizaciones de datos.

2. Pre-procesamiento de datos:
   - Convertir las variables numéricas en variables categóricas, ya que la minería de contrastes trabaja exclusivamente con datos categóricos.

3. Minería de contrastes:
   - Implementar un algoritmo de minería de contrastes que recupere todos los conjuntos de contraste en los datos proporcionados.
   - Ejecutar el algoritmo una vez por cada variable del conjunto de datos, tomando cada una como variable de grupo.


4. Resultados y concluisones

## Tecnologías y Herramientas utilizadas

El proyecto se desarrollará utilizando las siguientes tecnologías y herramientas:

- Python

### Librerías de Python utilizadas:

- pandas
- seaborn
- scipy.stats (importada como st)
- matplotlib.pyplot (importada como plt)
- matplotlib.colors (importada como LinearSegmentedColormap)
- itertools

Librerías de Machine Learning utilizadas:

- scikit-learn
  - from sklearn.preprocessing import OrdinalEncoder
  - from sklearn.compose import ColumnTransformer
  - from sklearn.preprocessing import StandardScaler
  - from sklearn.decomposition import PCA



## Descripción de los datos

### Características

- `JobTitle`: El puesto al cual pertenece el empleado.
- `Gender`: Sexo del empleado.
- `Age`: Edad del empleado.
- `PerfEval`: Rendimiento de evaluación en una escala del 1 al 5, donde 1 es el mínimo y 5 es el máximo.
- `Edu`: Nivel de educación del empleado.
- `Dept`: Área/Departamento de trabajo del empleado.
- `Seniority`: Antigüedad/Maestría en el puesto del empleado.
- `BasePay`: Sueldo base del empleado.
- `Bonus`: Bonos salariales recibidos por el empleado.


### Instrucciones de uso


pip install -r requirements.txt


## Referencias

- Stephen D. Bay, Michael J. Pazzani. Detecting Change in Categorical Data:
Mining Contrast Sets. In Proc. 1999 ACM SIGKDD International Conference
on Knowledge Discovery and Data Mining
- Amit Satsangi, Osmar R. Zaïane. Contrasting the Contrast Sets: An
Alternative Approach. Database Engineering and Applications Symposium,
2007
- Stephen D. Bay, Michael J. Pazzani. Detecting Group Differences: Mining
Contrast Sets. Data Mining and Knowledge Discovery. Volume 5, Number 3 /
July, 2001. Pages 213-246. Springer Netherlands.