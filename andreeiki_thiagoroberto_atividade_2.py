# -*- coding: utf-8 -*-
"""AndreEiki_ThiagoRoberto_Atividade_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15ftDo6KWJAOTQl_ugqjujyRHhIR8_P0j

# <font color=orange> Módulo Aprendizagem:

> ## <font color=#EE9A4D> Obtenção dos Dados:
"""

from google.colab import drive # Conectando ao Google Drive
drive.mount('/content/drive')

import pandas as pd
import zipfile
import numpy as np

zf = zipfile.ZipFile('/content/drive/MyDrive/Data/House_Sale/House_Sale.zip')  # aloca o arquivo zip

data = pd.read_csv(zf.open('kc_house_data.csv')) # abre o arquivo CSV 'kc_house_data.csv' presente dentro do ZIP
datacopy = data.copy() # Cria uma cópia do dataset original

data.head() # Imprime os dados

"""> ## <font color=#EE9A4D> Análise de Correlação e Exclusão de Dados Não Importantes:"""

import matplotlib.pyplot as plt
import seaborn as sns

corr  = data.corr() # Calcula a correlação presente entre todos os elementos contidos na matriz de dados

f, ax = plt.subplots(figsize=(17, 12))
sns.heatmap(corr, cmap=sns.color_palette("Blues"), linewidths=.5, annot=True);

# ID, date, lat e long são colunas visivelmente desnecessárias para o treinamente dos modelos
# Zipcode e Condition possuem uma baixa correlação com todos os outros elementos, por isso são da base de dados
data = data.drop(['id', 'date', 'lat', 'long', 'zipcode', 'condition'], axis=1) # Remove todas as colunas desnecessárias

"""> ## <font color=#EE9A4D> Tratando valores 'Not a Number'"""

data.isnull().sum()

# como NaN sempre nos causa problemas, (1) retiramos esse atributo ou (2) preenchemos com valores médios
np.where(data['sqft_above'].isnull().values==True)

data = data.drop([10, 17])
data.isnull().sum()

"""> ## <font color=#EE9A4D> Separando os dados"""

from sklearn.model_selection import train_test_split # separa os dados em treinamento e teste de forma aleatória

y = data['price']
X = data.iloc[:, 1:17]
print(y.shape)
print(X.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42) # Separando 20% do conjunto para teste

"""> ## <font color=#EE9A4D> Árvore de Decisão:"""

from sklearn import tree
# Criando uma árvore de decisão com regressão e profundidade máxima de 5

clf = tree.DecisionTreeRegressor(random_state=0,max_depth=5)
clf = clf.fit(X_train, y_train)

tree.plot_tree(clf) # Plot da árvore
plt.show()

dt_predicao = clf.predict(X_test) # Realiza as predições com o conjunto de teste

from sklearn import metrics

print("Decision Tree") # Métricas calculadas
print('MAE:', metrics.mean_absolute_error(y_test, dt_predicao))
print('MSE:', metrics.mean_squared_error(y_test, dt_predicao))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, dt_predicao)))

print("Coefficient of determination: %.2f" % metrics.r2_score(y_test, dt_predicao))

# Plot do comportamento de h(x) árvore de decisão e f(x) que representa o valor real
plt.scatter(y_test, dt_predicao, color="black")
plt.plot(np.arange(np.min(y_test),np.max(y_test)),
         np.arange(np.min(y_test),np.max(y_test)),color="red", linewidth=3)

plt.show()

"""> ## <font color=#EE9A4D> Modelo Linear"""

from sklearn import datasets, linear_model

regr = linear_model.LinearRegression() # Modelo linear com regressão

# Treina o modelo com o conjunto de treino
regr.fit(X_train, y_train)

# Realiza as predições com o conjunto de teste
regr_predicao = regr.predict(X_test)

# Métricas
print("Coefficients: \n", regr.coef_)
print('MAE:', metrics.mean_absolute_error(y_test, regr_predicao))
print('MSE:', metrics.mean_squared_error(y_test, regr_predicao))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, regr_predicao)))
print("Coefficient of determination: %.2f" % metrics.r2_score(y_test, regr_predicao))

# Plot do comportamento de h(x) do modelo linear e f(x) que representa o valor real
plt.scatter(y_test, regr_predicao, color="blue")
plt.plot(np.arange(np.min(y_test),np.max(y_test)),np.arange(np.min(y_test),np.max(y_test)),color="red", linewidth=3)

plt.show()

"""> ## <font color=#EE9A4D> Rede Neural"""

import tensorflow as tf
from tensorflow.keras import models, regularizers
from tensorflow.keras.layers import Dense, Dropout, GaussianNoise
from tensorflow.keras.constraints import max_norm
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.metrics import mean_absolute_percentage_error

input_shape = (14, )
model = Sequential([
Dense(1000, input_shape=input_shape, activation='relu', kernel_regularizer=regularizers.L2(0.01)),
GaussianNoise(0.2), # Ruído
Dropout(0.2), # Poda 
Dense(1000, activation = 'relu', kernel_regularizer=regularizers.L2(0.01)), #  Regularização Ativa
Dropout(0.2), # Poda 
Dense(1000, activation = 'relu', kernel_constraint=max_norm(2.)), # Restrição de Pesos
Dropout(0.2),
Dense(64, activation = 'relu', kernel_regularizer=regularizers.L2(0.01)), #  Regularização Ativa
Dropout(0.2), # Poda 
Dense(8, activation = 'relu', kernel_regularizer=regularizers.L2(0.01)), #  Regularização Ativa
Dropout(0.2), # Poda 
Dense(1, activation='linear')
])

model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_squared_error'])

history = model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1, validation_split=0.2) # Treinando o modelo
rna_preds = model.predict(X_test) # Realiza a predição com o conjunto de teste

# Métricas
print('MAE:', metrics.mean_absolute_error(y_test, rna_preds))
print('MSE:', metrics.mean_squared_error(y_test, rna_preds))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, rna_preds)))
print('MAPE:', mean_absolute_percentage_error(y_test, rna_preds))

# Plotando a Loss durante o treino e durante a validação do modelo
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper right')
plt.show()

# Plot do comportamento de h(x) da rede neural e f(x) que representa o valor real
plt.scatter(y_test, rna_preds[:, 0].flatten(), color='green')
plt.plot(np.arange(np.min(y_test),np.max(y_test)),np.arange(np.min(y_test),np.max(y_test)),color="red", linewidth=3)

plt.show()

"""> ## <font color=#EE9A4D> Análise de Resultados"""

fig = plt.figure()
ax = fig.add_subplot(111)

# Plot do comportamento de h(x) paras os três modelos anteriores e f(x)
ax.scatter(y_test, dt_predicao,  color="black") # Preto = Árvore de Decisão
ax.scatter(y_test, regr_predicao, color="blue") # Azul = Modelo Linear
ax.scatter(y_test, rna_preds[:, 0].flatten(), color='green') # Verde = Rede Neural
ax.plot(np.arange(np.min(y_test),np.max(y_test)),np.arange(np.min(y_test),np.max(y_test)),color="red", linewidth=3) # Vermelho = Valor Esperado

ax.figure.show()

dt_diff = np.absolute(y_test - dt_predicao) # Cálculo da diferença absoluta entre o valor real e a predição da árvore de decisão
regr_diff = np.absolute(y_test - regr_predicao) # Cálculo da diferença absoluta entre o valor real e a predição do modelo linear
rna_diff = np.absolute(y_test - rna_preds.flatten()) # Cálculo da diferença absoluta entre o valor real e a predição da rede neural

# Menor e maior diferença registrada para cada modelo, com relação ao valor real
print("Min dt_diff: ", np.min(dt_diff)/100000, "Max dt_diff", np.max(dt_diff)/100000)
print("Min regr_diff: ", np.min(regr_diff), "Max regr_diff", np.max(regr_diff))
print("Min rna_diff: ", np.min(rna_diff), "Max rna_diff", np.max(rna_diff))

# Plot do valor real e a predição da árvore de decisão
dt_outcomes = pd.DataFrame({'Predicted value':dt_predicao, 'Actual value':y_test})
fig= plt.figure(figsize=(16,8))
dt_outcomes = dt_outcomes.reset_index()
dt_outcomes = dt_outcomes.drop(['index'],axis=1)
plt.plot(dt_outcomes[:50])
plt.legend(['Actual value','Predicted value'])

# Plot do valor real e a predição do modelo linear
regr_outcomes = pd.DataFrame({'Predicted value':regr_predicao, 'Actual value':y_test})
fig= plt.figure(figsize=(16,8))
regr_outcomes = regr_outcomes.reset_index()
regr_outcomes = regr_outcomes.drop(['index'],axis=1)
plt.plot(regr_outcomes[:50])
plt.legend(['Actual value','Predicted value'])

# Plot do valor real e a predição da rede neural
rna_outcomes = pd.DataFrame({'Predicted value':list(rna_preds), 'Actual value':y_test})
fig= plt.figure(figsize=(16,8))
rna_outcomes = rna_outcomes.reset_index()
rna_outcomes = rna_outcomes.drop(['index'],axis=1)
plt.plot(rna_outcomes[:50])
plt.legend(['Actual value','Predicted value'])

# Plot do valor real e a predição da árvore de decisão e modelo linear
model_outcomes = pd.DataFrame({'DT':dt_predicao, 'Linear Model':regr_predicao, 'Actual value':y_test})
fig= plt.figure(figsize=(16,8))
model_outcomes = model_outcomes.reset_index()
model_outcomes = model_outcomes.drop(['index'],axis=1)
plt.plot(model_outcomes[:50])
plt.legend(['Actual value','DT','Linear Model'])

# Plot do valor real e a predição da árvore de decisão e rede neural
model_outcomes = pd.DataFrame({'DT':dt_predicao, 'RNA Model':rna_preds.flatten(), 'Actual value':y_test})
fig= plt.figure(figsize=(16,8))
model_outcomes = model_outcomes.reset_index()
model_outcomes = model_outcomes.drop(['index'],axis=1)
plt.plot(model_outcomes[:50])
plt.legend(['Actual value','DT', 'RNA Model'])

import numpy as np
import matplotlib.pyplot as plt

# Histograma referente a diferença entre o preço real e preço estimado pela árvore de decisão
n, bins, patches = plt.hist(dt_diff, density=True)
plt.xlabel('Diff Price')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Histograma referente a diferença entre o preço real e preço estimado pelo modelo linear
regr_diff.values.sort()
values = regr_diff.values
n, bins, patches = plt.hist(values, density=True)
plt.xlabel('Diff Price')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Histograma referente a diferença entre o preço real e preço estimado pela rede neural
rna_diff.values.sort()
values = regr_diff.values
n, bins, patches = plt.hist(values, density=True)
plt.xlabel('Diff Price')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.grid(True)
plt.show()

from sklearn import metrics 

# Salvando as métricas de cada modelo em listas
line1 = [metrics.mean_absolute_error(y_test, dt_predicao), metrics.mean_absolute_error(y_test, regr_predicao), metrics.mean_absolute_error(y_test, rna_preds)]
line2 = [metrics.mean_squared_error(y_test, dt_predicao), metrics.mean_squared_error(y_test, regr_predicao), metrics.mean_squared_error(y_test, rna_preds)]
line3 = [np.sqrt(metrics.mean_squared_error(y_test, dt_predicao)), np.sqrt(metrics.mean_squared_error(y_test, regr_predicao)), np.sqrt(metrics.mean_squared_error(y_test, rna_preds))]
line4 = [mean_absolute_percentage_error(y_test, dt_predicao), mean_absolute_percentage_error(y_test, regr_predicao), mean_absolute_percentage_error(y_test, rna_preds)]

# Plot de tabela comparativa entre os 3 modelos
fig, ax = plt.subplots()
colors = plt.cm.BuPu(np.linspace(0, 0.5, 4))

fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table(cellText=[line1, line2, line3, line4], 
         rowLabels = ['MAE', 'MSE', 'RMSE', 'MAPE'], 
         colLabels = ['Decision Tree', 'Linear Model', 'RNA Model'], 
         colColours = colors, 
         loc='center')

fig.tight_layout()

plt.show()

"""> ## <font color=#EE9A4D> 5-Fold Crossvalidation"""

# Crossvalidation protocol

import numpy as np
from sklearn.model_selection import KFold
import torch

y = data['price']
X = data.iloc[:, 1:17]

kf = KFold(n_splits=5,shuffle=True) # Define em quantas partes o conjunto será dividido
kf.get_n_splits(X)

print(kf)

for i, (train_index, test_index) in enumerate(kf.split(X)):
    print(f"Fold {i+1}:")
    print(f"  Train: index={train_index}")
    print(f"  Test:  index={test_index}")

X_train = X.values[train_index]
print("X_train: ",X_train.shape)
y_train = y.values[train_index]
print("y_train: ",y_train.shape)

X_test = X.values[test_index]
print("X_test: ",X_test.shape)
y_test = y.values[test_index]
print("y_test: ",y_test.shape)

from sklearn import metrics
import torch

for i, (train_index, test_index) in enumerate(kf.split(X)):
    print(f"\nFold {i+1}:")

    X_train = X.values[train_index]
    y_train = y.values[train_index]
    
    X_test = X.values[test_index]
    y_test = y.values[test_index]

    history = model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1, validation_split=0.2)
    rna_preds = model.predict(X_test, verbose=0)

    torch.save((X_test, y_test), f'./AndreEiki_ThiagoRoberto_FOLDS/Valores_de_Teste_Fold{i+1}.pth') # Salva o conjunto de teste de cada fold
    torch.save((X_train, y_train), f'./AndreEiki_ThiagoRoberto_FOLDS/Valores_de_Treino_Fold{i+1}.pth') # Salva o conjunto de treino de cada fold
    model.save_weights('./AndreEiki_ThiagoRoberto_FOLDS/AndreEiki_ThiagoRoberto_RNA_FOLD'+str(i+1)) # Salva os pesos utilizados em cada Fold

    print('MAE:', metrics.mean_absolute_error(y_test, rna_preds))
    print('MSE:', metrics.mean_squared_error(y_test, rna_preds))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, rna_preds)))
    print('MAPA:', mean_absolute_percentage_error(y_test, rna_preds))

data['new_price'] = model.predict(X) # Criando nova coluna com os preços estimados pela rede neural

"""# <font color=orange> Módulo Interface:

> ## <font color=#EE9A4D> Gerando Mapa:
"""

import folium 

map = folium.Map(location=[47.608013, -122.257], zoom_start=8, tiles = 'stamenterrain')

map

"""> ## <font color=#EE9A4D> Heatmap:"""

from folium.plugins import HeatMap

HeatMap(datacopy.iloc[:, [-4, -3, 2]], min_opacity = 0.2, name = 'heatmap').add_to(map) # Cria um heat map baseado nos preços das casas
map

"""> ## <font color=#EE9A4D> Aplicando Borda em Washington:"""

borderStyle = {
    'color': 'red',
    'weight': 2,
}

folium.GeoJson('/content/drive/MyDrive/Data/House_Sale/us-states.json', 
               name = 'Washington',
               style_function=lambda x: borderStyle).add_to(map)

map

folium.LayerControl().add_to(map)
map

"""> ## <font color=#EE9A4D> Plotando casas:"""

datacopy['new_price'] = data['new_price'] # Adiciona uma nova coluna 'new_price' ao dataset cópia

datacopy.price.quantile([0.25, 0.5, 0.75]) # Encontrando os quartis da coluna preço

i = 0
for index, row in datacopy.iterrows(): # Aplicando marcadores personalizados a cada casa
    # Popup que aparece ao clicar em um marcador
    popup = (folium.Html('<b>Price:</b> U$' + str(row['price']) + 
                        '<br><b>New Price:</b> U$' + str(row['new_price']) +
                        '<br><b>Bedrooms:</b> ' + str(row['bedrooms']) + 
                        '<br><b>Bathrooms:</b> ' + str(row['bathrooms']) +
                        '<br><b>Living Area:</b> ' + str(row['sqft_living']) + 'm²' +
                        '<br><b>Lot Area:</b> ' + str(row['sqft_lot']) +  'm²' +
                        '<br><b>Floors:</b> ' + str(row['floors']) +
                        '<br><b>Waterfront:</b> ' + str(row['waterfront']) +
                        '<br><b>Condition:</b> ' + str(row['condition']) +
                        '<br><b>Grade:</b> ' + str(row['grade']) +
                        '<br><b>Above:</b> ' + str(row['sqft_above']) +  'm²' +
                        '<br><b>Basement:</b> ' + str(row['sqft_basement']) +  'm²' +
                        '<br><b>Year Built:</b> ' + str(row['yr_built']) + 
                        '<br><b>Year Renovated:</b> ' + str(row['yr_renovated']) +
                        '<br><b>Zipcode:</b> ' + str(row['zipcode']), script=True))

    if (row['price'] >= 645000.0): # Marcadores para as 25% casas mais caras
      folium.Marker(location = [row['lat'], row['long']],
                  icon = folium.Icon(icon = 'glyphicon-home', color='darkred'),
                  tooltip = 'ID: ' + str(row['id']),
                  popup=folium.Popup(popup, max_width=500)).add_to(map)

    elif (row['price'] < 645000.0 and row['price'] >= 450000.0): # Marcadores para as casas mais próximas da mediana
      folium.Marker(location = [row['lat'], row['long']],
                  icon = folium.Icon(icon = 'glyphicon-home', color='orange'),
                  tooltip = 'ID: ' + str(row['id']),
                  popup=folium.Popup(popup, max_width=500)).add_to(map)
    else: # Marcadores para as 25% casas mais baratas
      folium.Marker(location = [row['lat'], row['long']],
                  icon = folium.Icon(icon = 'glyphicon-home', color='green'),
                  tooltip = 'ID: ' + str(row['id']),
                  popup=folium.Popup(popup, max_width=500)).add_to(map)
    i += 1
    if i > 1000: # Marca apenas as 1000 primeiras casas
      break
map

"""> ## <font color=#EE9A4D> Salvando Mapa:"""

map.save('mapa.html')