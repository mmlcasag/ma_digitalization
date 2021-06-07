import os
import csv
import shutil

import pandas
import openpyxl

# https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

print('Carregando os dados do arquivo Excel...', end='')
# the argument data_only tells openpyxl to get only cell values, not formulas
excel = openpyxl.load_workbook('./input/CheckList_MRO.xlsx', data_only=True)
print('OK')

print('Selecionando a aba ativa da planilha...', end='')
sheet = excel.active
print('OK')

print('Apagando as linhas iniciais da planilha...', end='')
sheet.delete_rows(1,10)
print('OK')

print('Criando diretórios necessários para o projeto...', end='')
if not os.path.exists('input'):
    os.makedirs('input')
if not os.path.exists('output'):
    os.makedirs('output')
if not os.path.exists('tmp'):
    os.makedirs('tmp')
print('OK')

print('Criando o arquivo CSV temporário...', end='')
csv_file = open('./tmp/CheckList_MRO.csv', 'w', newline='', encoding='utf-8')
print('OK')

print('Convertendo a planilha para o arquivo CSV...', end='')
col = csv.writer(csv_file)
for r in sheet.rows:
    col.writerow([cell.value for cell in r])
print('OK')

print('Carregando os dados do arquivo CSV...', end='')
df = pandas.read_csv('./tmp/CheckList_MRO.csv')
print('OK')

print('Fechando o arquivo CSV temporário...', end='')
csv_file.close()
print('OK')

print('Removendo o arquivo CSV temporário...', end='')
os.remove('./tmp/CheckList_MRO.csv')
print('OK')

print('Ajustando os nomes das colunas...', end='')
df = df.rename(columns={'PMM': 'Unitário', 'Valor': 'Total', 'UM': 'UN'})
print('OK')

print('Removendo colunas desnecessárias...', end='')
unwanted_columns = [
    'Motivo', 
    'Analista ',
    'Aprovador',
    'Diretoria',
    'Gerência',
    'Código Grupo de mercadorias',
    'Descrição do grupo de mercadorias',
    'Preço da última compra ou valor comercial\n(PREÇO UNITÁRIO)',
    'Endereço do item',
    'Campo de conferência para armazem',
    'Campo de conferência para CMD (opcional)',
    'Peso estimado em Kg',
    'Valor estimado do sucateamento',
    'Responsável CMD',
    'CMD / Mina\n(selecionar a opção da lista)',
    'Cidade / Estado\n(onde se encontra o lote fisicamente)'
]
df_excel = df.drop(columns=unwanted_columns)
print('OK')

print('Gerando arquivo Excel processado...', end='')
# you will probably notice that by default, pandas writes the line index as the first column in the spreadsheet
# if you don't want that, you can switch it off by adding the parameter index=False
df_excel.to_excel('./output/CheckList_MRO.xlsx', index=False)
print('OK')

print('Desconsiderando colunas de valores para geração do arquivo HTML...', end='')
df_html = df_excel.drop(columns=['Unitário','Total'])
print('OK')

print('Movendo colunas de posição no arquivo HTML...', end='')
cols = list(df_html.columns.values)
df_html = df_html[cols[0:4] + cols[5:8] + [cols[4]] + [cols[8]]]
print('OK')

print('Convertendo conteúdo do DataFrame para HTML...', end='')
# you will probably notice that by default, pandas writes the line index as the first column in the spreadsheet
# if you don't want that, you can switch it off by adding the parameter index=False
html = df_html.to_html(index=False)
html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  <style>
    * {
      font-family: Arial;
      font-size: x-small;
    }
    th {
      text-align: left;
      padding: 3px;
    }
    tr {
      text-align: left;
      padding: 3px;
    }
    td {
      text-align: left;
      padding: 3px;
    }
  </style>
</head>
<body>
  ''' + html + '''
</body>
</html>
'''
print('OK')

print('Gerando arquivo HTML processado...', end='')
text_file = open('./output/CheckList_MRO.html', "w", newline='', encoding='utf-8')
text_file.write(html)
text_file.close()
print('OK')

print('Pegando o nome do responsável do lote...', end='')
nom_acessor = df['Responsável CMD'][0]
print('OK')

print('Pegando o nome da unidade do lote...', end='')
nom_unidade = df['CMD / Mina\n(selecionar a opção da lista)'][0]
print('OK')

print('Pegando o município e o estado do lote...', end='')
cidade_estado = df['Cidade / Estado\n(onde se encontra o lote fisicamente)'][0]
cidade_estado = cidade_estado.replace(' / ','/').split('/')
print('OK')

print('Pegando a referência do lote...', end='')
ref_lote = df['Nº lote'][0]
print('OK')

print('Buscando a quantidade total de produtos no lote...', end='')
qtd_produtos = df['Cód.'].count()
print('OK')

print('Somando o valor total dos produtos do lote...', end='')
vlr_produtos = round(df['Total'].sum(),2)
print('OK')

print('Pegando os três produtos de valor mais expressivo...', end='')
produtos = df.sort_values(['Total'], ascending=False)[0:3]['Descrição']
print('OK')

print('Montando a descrição do lote...', end='')
des_lote = ''

# monta a descrição do lote baseado no primeiro nome do array dos produtos
for produto in produtos.values:
    des_lote = des_lote + produto[0:produto.find(' ')] + ', '

# apaga a última vírgula da string
des_lote = des_lote[0: len(des_lote) - 2]

# concatena na descrição a quantidade restante de produtos
if qtd_produtos > 3:
    des_lote = des_lote + ' e outros'

# converte tudo para maiúsculo
des_lote = des_lote.upper()
print('OK')

print('Calculando valores de VI e incremento...', end='')
vi = round(vlr_produtos / 100,0)
possiveis_incrementos = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
incremento = closest(possiveis_incrementos, vi / 10)
print('OK')

print('Criando planilha colunada...', end='')
df_colunada = pandas.DataFrame({
  'Nº do lote': 1,
  'Status': 'novo',
  'Lote Ref. / Ativo-Frota': ref_lote,
  'Nome do Lote (SEMPRE MAIUSCULA)': des_lote,
  'Descrição': 'Para maiores informações, clique em ANEXOS',
  'VI': vi,
  'VMV': 0,
  'VER': 0,
  'Incremento': incremento,
  'Valor de Referência do Vendedor (Contábil)': vlr_produtos,
  'Comitente': nom_unidade,
  'Município': cidade_estado[0],
  'UF': cidade_estado[1],
  'Assessor': nom_acessor,
  'Pendências': '',
  'Restrições': '',
  'Débitos (Total)': '',
  'Unid. Métrica' : '',
  'Fator Multiplicativo': '1',
  'Alteração/Adicionado': '',
  'Descrição HTML': 'Em arquivo separado'
}, index=[0])
print('OK')

print('Exportando planilha coluna para Excel...', end='')
# you will probably notice that by default, pandas writes the line index as the first column in the spreadsheet
# if you don't want that, you can switch it off by adding the parameter index=False
df_colunada.to_excel('./output/Geral_UtilizadaAtualmente.xlsx', index=False)
print('OK')

print('Processo finalizado com sucesso')
