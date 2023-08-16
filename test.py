## comentario:
import pandas as pd
from datetime import datetime
###FILTRAR DATOS
##Filtro f1: elimina datos de valores no esperados.

#Creamos df_f1, para los datos con Filtro : f0 + f1 +f2
df_f11 = pd.read_csv('df_f0+f2.csv',index_col='Time')
## generamos indice en formato TIME

df_f1 = df_f11 
#df_f1.index = pd.to_datetime(df_f1.index)

date_index = [datetime.strptime(date_str, '%H:%M %d/%m/%Y') for date_str in df_f1.index ]
df_f1.index = date_index

###Se aplica los filtros por columna:
#se ingresan los valores de referencia.
#se completa con "nan numerico" los valores fuera del intervalo:

#t_out: 
t_min_ref=5.0  # ref_armada: 7.3  #ref_datos: 4.8   
t_max_ref=30.0 #ref_armada: 25.9  #ref_datos: 31.3

df_f1.t_out[(df_f1.t_out<t_min_ref)]=float("nan") 
df_f1.t_out[(df_f1.t_out>t_max_ref)]=float("nan")

#rh_out:
rh_min_ref=0   #ref_armada: 34  #ref_datos:11
rh_max_ref=100 #ref_armada: 99  #ref_datos:100

df_f1.rh_out[(df_f1.rh_out<rh_min_ref)]=float("nan") 
df_f1.rh_out[(df_f1.rh_out>rh_max_ref)]=float("nan")

#wind:(m/s)
wind_min_ref=0   #ref_armada: 0  #ref_datos:0
wind_max_ref=25  ##ref_armada: 23  #ref_datos: 21

df_f1.wind[(df_f1.wind<wind_min_ref)]=float("nan") 
df_f1.wind[(df_f1.wind>wind_max_ref)]=float("nan")

#td:
td_min_ref=0   ##ref_armada: 0.8  #ref_datos:0.0
td_max_ref=19  #ref_armada: 18.8  #ref_datos:18.4

df_f1.td[(df_f1.td<td_min_ref)]=float("nan") 
df_f1.td[(df_f1.td>td_max_ref)]=float("nan")


#p_abs:
pabs_min_ref=990  #ref_armada: sin info  #ref_datos:995.5
pabs_max_ref=1100  #ref_armada: sin info  #ref_datos:1026.5

df_f1.p_abs[(df_f1.p_abs<pabs_min_ref)]=float("nan") 
df_f1.p_abs[(df_f1.p_abs>pabs_max_ref)]=float("nan")

#p_rel
prel_min_ref=990  #ref_armada: 1008   #ref_datos:995.6
prel_max_ref=1100 #ref_armada: 1029.9 #ref_datos:1026

df_f1.p_rel[(df_f1.p_rel<prel_min_ref)]=float("nan") 
df_f1.p_rel[(df_f1.p_rel>prel_max_ref)]=float("nan")

#df_f1.p_abs.plot(color='b')
#df_f1.p_rel.plot(color='r')
#pl.show()
#rain
rain_min_ref=0  #sin ref   #ref_armada: sin info  #ref_datos:0
rain_max_ref=20 #sin ref   #ref_armada: sin info  #ref_datos:19.8

df_f1.rain_rate[(df_f1.rain_rate<rain_min_ref)]=float("nan") 
df_f1.rain_rate[(df_f1.rain_rate>rain_max_ref)]=float("nan")

#df_f1.to_csv('meteo-2017-21019_completo_formato.csv') 
#df_f1.to_pickle('meteo-2017-2019_completo_formato.pkl')
