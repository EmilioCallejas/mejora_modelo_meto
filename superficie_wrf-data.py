
from netCDF4 import Dataset
import wrf
from wrf import getvar, ALL_TIMES, ll_to_xy, interplevel
import pandas as pd
import os

# Ruta al archivo WRF que deseamos cargar

path = 'wrf_valpo'
#os.chdir(path)

dirs = os.listdir(path)
dirs.sort()


dirs = dirs[-10:]
#print(dirs)


#path = ["valpo/wrfout_d04_2019-12-28_00:00:00", "valpo/wrfout_d04_2019-12-29_00:00:00", "valpo/wrfout_d04_2019-12-30_00:00:00"]

df_d1 = pd.DataFrame()
df_d2 = pd.DataFrame()
df_d3 = pd.DataFrame()
###cordenadas datos observados:
lat = -33.01
lon = -71.6

for archivo in dirs:
	
	wrf_file = os.path.join(path,archivo) 
	#print(wrf_file)
	try:	
	## cargamos los datos del archivo wrf a formato dataset
		wrf_data = Dataset(wrf_file)

	## obtenemos las variables de interes
		td2 = getvar(wrf_data, "td2", timeidx= ALL_TIMES, method="cat")
		rh2 = getvar(wrf_data, "rh2", timeidx= ALL_TIMES, method="cat")
		T2 = getvar(wrf_data, "T2", timeidx= ALL_TIMES, method="cat")
		uvmet10 = getvar(wrf_data, "uvmet10_wspd_wdir", timeidx= ALL_TIMES, method="cat")
		tt = getvar(wrf_data, "times", timeidx= ALL_TIMES, method="cat")
	
		tt = pd.to_datetime(tt)
		
	## obtenemos los datos de la variable en un punto de cordenada
		lat_index , lon_index = ll_to_xy(wrf_data, lat, lon, timeidx=ALL_TIMES)
		td2=td2[:,lat_index,lon_index]
		rh2=rh2[:,lat_index,lon_index]
		T2=T2[:,lat_index,lon_index]
		ws10=uvmet10[0,:,lat_index,lon_index]
		wd10=uvmet10[1,:,lat_index,lon_index]


        ## probando con variables 3d
                tk = getvar(wrf_data,"tk", timeidx=ALL_TIMES, method="cat")
                P = getvar(wrf_data,"pressure", timeidx=ALL_TIMES, method="cat")
                td = getvar(wrf_data,"td", timeidx=ALL_TIMES, method="cat")
                rh = getvar(wrf_data,"rh", timeidx=ALL_TIMES, method="cat")
                uvmet = getvar(wrf_data,"uvmet_wspd_wdir", timeidx=ALL_TIMES, method="cat")

                z = getvar(wrf_data,"z", timeidx=ALL_TIMES, method="cat")

        ##interpoland la altura correspondiente a las variables
                tk=interplevel(tk,z,68) #la estacion se estacion a 68 amsl(por encima del nivel promedio del mar)
                P = interplevel(P,z,68)
                td = interplevel(td,z,68)
                rh = interplevel(rh,z,68)
                uvmet = interplevel(uvmet,z,68)

        ##obteniendo los datos 3d en la coordenada correspodiente
                tk=tk[:,lat_index,lon_index]
                P = P[:,lat_index,lon_index]
                td = td[:,lat_index,lon_index]
                rh = rh[:,lat_index,lon_index]
                ws = uvmet[0,:,lat_index,lon_index]
                wd = uvmet[1,:,lat_index,lon_index]
	##no para obtener el dataframe de estas variables, me salta un error si lo hago como el de las variables 2d

		
	## creamos data frame con columnas por variable, manteniendo el index		
		df = pd.DataFrame({
            		'td2': td2.data,
            		'rh2': rh2.data,
            		'T2': T2.data,
            		'ws10': ws10.data,
            		'wd10': wd10.data
        		}, index=tt)
        
     
	## cerramos el archivo wrf
		wrf_data.close()

	except 	Exception as e:
		print("Error procesando {wrf_file}: {e}")
		continue		


	## agrupamos con frecuencia diaria:
	groups = df.groupby(pd.Grouper(freq='D'))

	## guardamos cadagrupo en un nuevo dataframe
	dfs = []
	for name, group in groups:
		dfs.append(group)
	#print(dfs)	
	try:
	## guardamos los valores de la variable correspondiente al dia de pronostico
		df_d1 = pd.concat([df_d1, dfs[0]])
		df_d2 = pd.concat([df_d2, dfs[1]])
		df_d3 = pd.concat([df_d3, dfs[2]])
	except Exception as e:
		print("Error en la creacion del dataframe {wrf_file}: {e}")
		continue
	
df_d1.to_pickle("Weather_pronostico_1dia.pkl")
df_d2.to_pickle("Weather_pronostico_2dia.pkl")
df_d3.to_pickle("Weather_pronostico_3dia.pkl")
