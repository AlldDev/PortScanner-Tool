import pandas as pd

_PORT = str(443)

# Lendo o CSV | Definindo o separador por ',' | Definido o Index sendo a tabela que eu quiser
df = pd.read_csv('service-names-port-numbers.csv', sep=',', index_col='Port Number')

#print(df)

# Var recebe os valores de Port e a descrição
# _PORT busca pelo indexador
# ['Description'] retorna apenas a coluna desejada
porta_aberta = df.loc[_PORT, ['Description']]

dicionario_portas = porta_aberta.to_dict(orient='records')
print(dicionario_portas)


porta = int(_PORT)
print(dicionario_portas[porta, 0])

#for item in dicionario_portas:
#    for key, value in item.itens():
#        print(_PORT, value)
#
#print('[{}] - [{}]'.format(df.loc[_PORT, ['Description']]))






# Pesquisar dentro do arquivo
# print(df.query('`Port Number` == "3"'))

# query = df.loc[df[3 == "Port Number"]]

# query = df.query("'Port Number' == @_PORT")

# print(query)
