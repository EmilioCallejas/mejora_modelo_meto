#  Generamos un DataFrame con las columnas Vup Iup Vdow Idow
# la informacion de la muestra esta en el nombre del archivo generado
# ejemplo     nombre-muestra_ciclo_repeticion   
#              HF928_C1_R1

# Update Oct 9
# Nombre archivos: celda1_ciclo_0000.txt     

import pandas as pd
import numpy as np
import sys

# Leer el archivo de texto con pandas
def leer_txt_pandas(filepath):
    # Leer el archivo como texto y eliminar las primeras líneas de encabezado
    with open(filepath, 'r') as file:
        lines = file.readlines()

    ciclo = lines[0].strip()
    rep = lines[1].strip()
    # Extraer la fecha y hora
    date = lines[3].strip()  # Fecha en la línea 4
    time = lines[4].strip()  # Hora en la línea 5
    
    # Crear columna datetime
    datetime = pd.to_datetime(f"{date} {time}", format="%d-%m-%Y %H:%M:%S")
    
    # Leer datos de DIR UP (líneas 7 a 56) y DIR DOWN (líneas 63 a 113)
    df_up = pd.read_csv(filepath, sep=r'\s+', skiprows=6, nrows=50, names=["Vup", "Iup"])
    df_down = pd.read_csv(filepath, sep=r'\s+', skiprows=63, nrows=50, names=["Vdw", "Idw"])
    
    # Agregar la columna datetime
    df_up['datetime'] = datetime
   # df_down['datetime'] = datetime

    # Combinar ambos DataFrames
    df_final = pd.concat([df_up.reset_index(drop=True), df_down.reset_index(drop=True)], axis=1)
    
    return ([df_final, ciclo, rep])

#filephat = 'celda1.txt'

# Además, leer también el archivo del piranómetro 

##############
#Hacer un loop sobre todos los ciclos (anidar otro loop para las celdas) y correr hasta el parámetro entregado por el bash

m = sys.argv[1]                #Este argumento me indica la cantidad total del datos (dividir en 2 para trabajar por celda)
print(m)
filepath = 'SplitData/celda1_ciclo_0000.txt'            

# Llamar la función para procesar el archivo
df1 , ciclo , rep = leer_txt_pandas(filepath)   

# Poner la columna datetime como index      
df1.set_index('datetime', inplace=True)     

num_rows = len(df1)         
increments = pd.to_timedelta(4 * np.arange(0, len(df1) * 0.01, 0.01), unit='s')         # Revisar incremento
df1.index = df1.index + increments  # Sumar los incrementos al índice     


# Convertir las las ',' por '.' 
df1[['Vup', 'Iup', 'Vdw', 'Idw']] = df1[['Vup', 'Iup', 'Vdw', 'Idw']].replace(',', '.', regex=True)

# Convertir las columnas 'Vup', 'Iup', 'Vdw' e 'Idw' a tipo float
df1[['Vup', 'Iup', 'Vdw', 'Idw']] = df1[['Vup', 'Iup', 'Vdw', 'Idw']].astype(float)


###################    Clear comments once check it works properly

#Import data from pkl (provided by _macro-datos) 
#pklName = 'celda1_ciclo_1_repeticion_1'
#df1 = pd.read_pickle(pklName)

#Set area according to file name (ex: celda1 -> 1 cm^2 ; celda2 -> 20.25 cm^2)
if filepath[15] == "1":
    Ama = 1.0
elif filepath[15] == "2":     
    Ama = 20.25

#Hallar Parámetros fotovoltaicos 

pd.options.mode.copy_on_write = True
df = df1.rename(columns={"Iup": "iUp", "Idw": "iDw"})               #Adapt to local names   

def zeroMask(df1, var):
    return (df1[var] - 0.).abs().idxmin()                            #index of the 'var' value closest to zero 

def tangetMask(df1, x_var, y_var):
    x = df1[x_var] ; y = df1[y_var]
    return (np.abs(np.gradient(x, y/Ama) - 1.)).argmin()             #index where derivative of y_var w/r/ to x_var is closest to 1         

def productMask(df2, x_var, y_var):
    df3 = df2[df2[y_var] < 0]                                   # filter negative currents
    df3['product'] = (df3[x_var] * df3[y_var]).abs()            # add a new column to the local df
    return df3['product'].idxmax()

df[['iUp', 'iDw']] = df[['iUp', 'iDw']]*1000                    # [A] to [mA]    

    
jSC_up = df['iUp'][zeroMask(df, 'Vup')]  / Ama                  # [mA/cm²]  
jSC_dw = df['iDw'][zeroMask(df, 'Vdw')]  / Ama

Voc_up = df['Vup'][zeroMask(df, 'iUp')]                         # [V]
Voc_dw = df['Vdw'][zeroMask(df, 'iDw')] 

#Vmax_up = df['Vup'][tangetMask(df, 'Vup', 'iUp')]                # Voltaje en Pmax  -  [V]        
#jMax_up = df['iUp'][tangetMask(df, 'Vup', 'iUp')] / Ama          # densidad de Corriente en Pmax  -  [mA/cm²]
    
#Vmax_dw = df['Vdw'][tangetMask(df, 'Vdw', 'iDw')]                # Cálculo usando la derivada (deprecado)
#jMax_dw = df['iDw'][tangetMask(df, 'Vdw', 'iDw')] / Ama          

Vmax_up = df['Vup'][productMask(df, 'Vup', 'iUp')]                
jMax_up = df['iUp'][productMask(df, 'Vup', 'iUp')] / Ama          
    
Vmax_dw = df['Vdw'][productMask(df, 'Vdw', 'iDw')]                
jMax_dw = df['iDw'][productMask(df, 'Vdw', 'iDw')] / Ama          

Voc = [Voc_up, Voc_dw] ; jSC = [jSC_up, jSC_dw]
Vmax = [Vmax_up, Vmax_dw] ; jMax = [jMax_up, jMax_dw]

dir = ['Up', 'Down'] 
for i in range(2):
    print("Voc {} = {}".format(dir[i],Voc[i]))
    print("jSC {} = {}".format(dir[i],jSC[i]))
    print("jmax {} = {}".format(dir[i],jMax[i]))
    print("Vmax {} = {}".format(dir[i], Vmax[i]))

#Define functions: FF & PCE for each run ; HI for each cicle (i.e. up and down runs)

def FF(Vmax, jmax, Voc, jSC):
    return Vmax*jmax / Voc*jSC                      # Adimensional

def PCE(Vmax, jmax, Pin=100.0):                       # Eficiencia
    return np.abs(100.0*Vmax*jmax / Pin)              # [%]  ;  Pin: dato piranómetro ; (lab) P_In = 100 mW/cm^2 = 100 V*mA/cm^2

def HI(jMaxFor, jMaxRev):
    return 1.0 + jMaxFor / jMaxRev 

# Llamar a las funciones (estos outputs pasarlos a un archivo)

for i in [0,1]:
    print("Field Factor ({} run) = {}".format(dir[i], round(FF(Vmax[i], jMax[i], Voc[i], jSC[i]), 4)))
    print("PCE ({} run) \t\t= {} %".format(dir[i], round(PCE(Vmax[i], jMax[i]),4)))
    
print("HI \t\t\t=", round(HI(jMax[0], jMax[-1]),4))       

# Dejar las salidas en un pkl (para nosostros) y tambien en un csv (para leer en Excel)

# Estos datos debemos cruzarlos con los tiempos para hacer el pkl    

# DataFrame.to_csv     

# Definir el Pin a partir de la columna del piranómetro





