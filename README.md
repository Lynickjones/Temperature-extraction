# Temperature-extraction
Code to extract temperature from NC files using a table of coordinates and labels.
Description
####################################### EN ####################################

This project extracts ocean temperature values from NetCDF files using geographic coordinates (latitude and longitude) and a classification previously assigned to each point through the label column in a CSV file.

NetCDF file selection is performed dynamically according to the label value associated with each point. The script extracts three temperature statistics for each location:

Maximum (max)
Mean (mean)
Minimum (min)
The data are extracted from NetCDF datasets representing different depth levels or vertical categories:
Label
Category

Datasets used
0 Shallow
Max, Mean, and Min
1 Average
Max, Mean, and Min
2 Deep
Max, Mean, and Min

The extracted values are appended to the input CSV file and exported in two formats: CSV and Excel (.xlsx).
####################################### PT-BR ####################################

Descrição

Este projeto realiza a extração de valores de temperatura oceânica a partir de arquivos NetCDF, utilizando coordenadas geográficas (latitude e longitude) e uma classificação previamente atribuída aos pontos por meio da coluna label de um arquivo CSV.

A seleção dos arquivos NetCDF é realizada dinamicamente, de acordo com o valor do label associado a cada ponto. O script extrai três estatísticas de temperatura para cada localização:
Máxima (max)
Média (mean)
Mínima (min)
Os dados são extraídos de conjuntos NetCDF referentes a diferentes profundidades ou categorias verticais:
Label
Categoria
Arquivos utilizados

0 Shallow
Max, Mean e Min
1 Average
Max, Mean e Min
2 Deep
Max, Mean e Min

Os resultados são incorporados ao CSV de entrada e exportados em dois formatos: CSV e Excel (.xlsx).



