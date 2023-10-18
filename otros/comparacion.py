import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from scipy.optimize import curve_fit

# Cargar los datos de los archivos PKL en DataFrames
path1 = 'meteo-2017-21019_por-hora_formato.csv'
path2 = 'Weather_pronostico_1dia.pkl'

df_obs = pd.read_csv(path1)
df_wrf = pd.read_pickle(path2)


### correcciones de formato para los indices de cada dataframe
df_obs.index =df_obs['Unnamed: 0']
df_obs.index = pd.to_datetime(df_obs.index)

df_wrf['T2']=df_wrf['T2']-273.16

# reagrupamos para las columnas de interes en un mismo orden.
columnas_interes = ['td', 'rh_out', 't_out','wind', 'wind_dir']
df_obs =df_obs[columnas_interes]

# Renombrar las columnas
nuevos_nombres = {'td': 'td2_obs', 'rh_out': 'rh2_obs', 't_out': 'T2_obs','wind':'ws10_obs', 'wind_dir': 'wd10_obs'}
df_obs.rename(columns=nuevos_nombres, inplace=True)
df_obs = df_obs.rename_axis('time')


# Definir arreglos para los valores de RMSE y BIAS
rmse_values = []
bias_values = []


# Calcular RMSE y BIAS para diferentes variables entre df_wrf y df_obs
variables = ['T2', 'td2', 'ws10']#,'wd10']  # Agrega aquí las variables que deseas comparar

for var in variables:
    df_common_var = df_common[[var, var + '_obs']]  # Seleccionar las columnas relevantes
    #df_common_var.dropna(inplace=True)  # Eliminar filas con NaN
    
    rmse_value = rmse(df_common_var[var], df_common_var[var + '_obs'])
    bias_value = bias(df_common_var[var], df_common_var[var + '_obs'])
    
    print(f"Variable: {var}")
    print("RMSE:", rmse_value)
    print("BIAS:", bias_value)
    print("\n")

# Agregar los valores de RMSE y BIAS a los arreglos
    rmse_values.append(rmse_value)
    bias_values.append(bias_value)
    


'''

# Gráfico de dispersión
    plt.figure(figsize=(10,10))
    plt.scatter(df_common_var[var + '_obs'], df_common_var[var], s=0.2)
    plt.xlabel(f'{var}_obs')
    plt.ylabel(var)
    plt.title(f'Comparación entre {var}_obs y {var}')
    plt.grid(True)
    #plt.plot([5,30],[5,30],'k')
   
    
    plt.show()

 
  fig=plt.figure()
plt.scatter(df_obs2['t_out'][ix1],df_wrf2['T2'][ix1] -273.16,s=0.1)
plt.plot([5,30],[5,30],'k')
plt.xlim(5,30)
plt.ylim(5,30)
plt.show()

 # Gráfico de dispersión
    plt.figure(figsize=(8, 6))
    plt.scatter(df_common_var[var + '_obs'], df_common_var[var], alpha=0.5)
    plt.xlabel(f'{var}_obs')
    plt.ylabel(var)
    plt.title(f'Comparación entre {var}_obs y {var}')
    plt.grid(True)
    plt.show()
'''
