#!/bin/sh

#Opcionalente: La ruta original de los datos y en la que queremos dejar los split, 
#se la podríamos pasar como argumento a este script

cd /home/jorge/Escritorio/Lic.\ Física/Ramos/1Semestre\ VIII/Proyecto/Paneles

echo "Splitting Celda1  --- % ---"
split -l 114 celda1_continua -d -a 4 --additional-suffix=.txt celda1_ciclo_

echo "Moving txt files --- % ---"

mv celda1_ciclo_*.txt /home/jorge/Escritorio/Lic.\ Física/Ramos/1Semestre\ VIII/Proyecto/Paneles/SplitData

echo "Splitting Celda2 --- % ---"
split -l 114 celda2_continua -d -a 4 --additional-suffix=.txt celda2_ciclo_

echo "Moving txt files --- % ---"

mv celda2_ciclo_*.txt /home/jorge/Escritorio/Lic.\ Física/Ramos/1Semestre\ VIII/Proyecto/Paneles/SplitData

file_count=$(ls SplitData/ | wc -l)	           	

python3 JoinedCode.py $file_count       

exit 0

