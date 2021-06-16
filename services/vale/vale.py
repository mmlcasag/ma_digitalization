import os
import csv

import pandas
import openpyxl


# https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


contador = 0

input_folder = "input"
output_folder = "output"

colunada = {
    "Nº do lote": [],
    "Status": [],
    "Lote Ref. / Ativo-Frota": [],
    "Nome do Lote (SEMPRE MAIUSCULA)": [],
    "Descrição": [],
    "VI": [],
    "VMV": [],
    "VER": [],
    "Incremento": [],
    "Valor de Referência do Vendedor (Contábil)": [],
    "Comitente": [],
    "Município": [],
    "UF": [],
    "Assessor": [],
    "Pendências": [],
    "Restrições": [],
    "Débitos (Total)": [],
    "Unid. Métrica": [],
    "Fator Multiplicativo": [],
    "Alteração/Adicionado": [],
    "Descrição HTML": [],
}

if not os.path.exists(input_folder):
    os.makedirs(input_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(os.path.join(output_folder, "Backup")):
    os.makedirs(os.path.join(output_folder, "Backup"))
if not os.path.exists(os.path.join(output_folder, "csv")):
    os.makedirs(os.path.join(output_folder, "csv"))
if not os.path.exists(os.path.join(output_folder, "Html")):
    os.makedirs(os.path.join(output_folder, "Html"))
if not os.path.exists(os.path.join(output_folder, "Planilha")):
    os.makedirs(os.path.join(output_folder, "Planilha"))

for full_file_name in os.listdir(input_folder):
    if full_file_name.endswith("xlsx"):
        contador = contador + 1

        full_file_path = os.path.join(input_folder, full_file_name)
        file_name = os.path.splitext(full_file_name)[0]
        file_extension = os.path.splitext(full_file_name)[1]

        print('\nPROCESSANDO O ARQUIVO "' + full_file_name + '"')

        print("-- Carregando os dados do arquivo Excel...", end="")
        # the argument data_only tells openpyxl to get only cell values, not formulas
        excel = openpyxl.load_workbook(full_file_path, data_only=True)
        print("OK")

        print("-- Selecionando a aba ativa da planilha...", end="")
        sheet = excel.active
        print("OK")

        linenum = 0
        print(
            '-- Verificando quantidade de linhas de cabeçalho antes de chegar em "Cód."...',
            end="",
        )
        for row in sheet.rows:
            columns = [cell.value for cell in row]

            if columns[0] == "Cód.":
                break

            linenum = linenum + 1
        print("OK")

        print(
            "-- Apagando as " + str(linenum) + " linhas iniciais da planilha...", end=""
        )
        sheet.delete_rows(1, linenum)
        print("OK")

        print("-- Criando o arquivo CSV...", end="")
        csv_file = open(
            os.path.join(output_folder, "csv", file_name + ".csv"),
            "w",
            newline="",
            encoding="utf-8",
        )
        print("OK")

        print("-- Convertendo a planilha para o arquivo CSV...", end="")
        writer = csv.writer(csv_file)
        for row in sheet.rows:
            writer.writerow([cell.value for cell in row])
        print("OK")

        print("-- Carregando os dados do arquivo CSV...", end="")
        df = pandas.read_csv(os.path.join(output_folder, "csv", file_name + ".csv"))
        print("OK")

        print("-- Fechando o arquivo CSV...", end="")
        csv_file.close()
        print("OK")

        print("-- Ajustando os nomes das colunas...", end="")
        df = df.rename(columns={"PMM": "Unitário", "Valor": "Total", "UM": "UN"})
        print("OK")

        print("-- Removendo colunas desnecessárias...", end="")
        unwanted_columns = [
            "Motivo",
            "Analista ",
            "Aprovador",
            "Diretoria",
            "Gerência",
            "Código Grupo de mercadorias",
            "Descrição do grupo de mercadorias",
            "Preço da última compra ou valor comercial\n(PREÇO UNITÁRIO)",
            "Endereço do item",
            "Campo de conferência para armazem",
            "Campo de conferência para CMD (opcional)",
            "Peso estimado em Kg",
            "Valor estimado do sucateamento",
            "Responsável CMD",
            "CMD / Mina\n(selecionar a opção da lista)",
            "Cidade / Estado\n(onde se encontra o lote fisicamente)",
        ]
        df_excel = df.drop(columns=unwanted_columns)
        print("OK")

        print("-- Gerando arquivo Excel processado...", end="")
        # you will probably notice that by default, pandas writes the line index as the first column in the spreadsheet
        # if you don't want that, you can switch it off by adding the parameter index=False
        df_excel.to_excel(
            os.path.join(output_folder, "Backup", file_name + ".xlsx"), index=False
        )
        print("OK")

        print(
            "-- Desconsiderando colunas de valores para geração do arquivo HTML...",
            end="",
        )
        df_html = df_excel.drop(columns=["Unitário", "Total"])
        print("OK")

        print("-- Movendo colunas de posição no arquivo HTML...", end="")
        cols = list(df_html.columns.values)
        df_html = df_html[cols[0:4] + cols[5:8] + [cols[4]] + [cols[8]]]
        print("OK")

        print("-- Convertendo conteúdo do DataFrame para HTML...", end="")
        # you will probably notice that by default, pandas writes the line index as the first column in the spreadsheet
        # if you don't want that, you can switch it off by adding the parameter index=False
        # na_rep ==> here you can set the value you want to replace with NaN values
        html = df_html.to_html(index=False, na_rep="")
        html = (
            """
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
        """
            + html
            + """
        </body>
        </html>
        """
        )
        print("OK")

        print("-- Gerando arquivo HTML processado...", end="")
        text_file = open(
            os.path.join(output_folder, "Html", file_name + ".html"),
            "w",
            newline="",
            encoding="utf-8",
        )
        text_file.write(html)
        text_file.close()
        print("OK")

        print("-- Pegando o nome do responsável do lote...", end="")
        nom_acessor = df["Responsável CMD"][0]
        print("OK")

        print("-- Pegando o nome da unidade do lote...", end="")
        nom_unidade = df["CMD / Mina\n(selecionar a opção da lista)"][0]
        print("OK")

        print("-- Pegando o município e o estado do lote...", end="")
        cidade_estado = df["Cidade / Estado\n(onde se encontra o lote fisicamente)"][0]
        cidade_estado = cidade_estado.replace(" / ", "/").replace(" - ", "/").split("/")
        print("OK")

        print("-- Pegando a referência do lote...", end="")
        ref_lote = df["Nº lote"][0]
        print("OK")

        print("-- Buscando a quantidade total de produtos no lote...", end="")
        qtd_produtos = df["Cód."].count()
        print("OK")

        print("-- Somando o valor total dos produtos do lote...", end="")
        vlr_produtos = round(df["Total"].sum(), 2)
        print("OK")

        print("-- Pegando os três produtos de valor mais expressivo...", end="")
        produtos = df.sort_values(["Total"], ascending=False)[0:3]["Descrição"]
        print("OK")

        print("-- Montando a descrição do lote...", end="")
        des_lote = ""

        # monta a descrição do lote baseado no primeiro nome do array dos produtos
        for produto in produtos.values:
            des_lote = des_lote + produto[0 : produto.find(" ")] + ", "

        # apaga a última vírgula da string
        des_lote = des_lote[0 : len(des_lote) - 2]

        # concatena na descrição a quantidade restante de produtos
        if qtd_produtos > 3:
            des_lote = des_lote + " e outros"

        # converte tudo para maiúsculo
        des_lote = des_lote.upper()
        print("OK")

        print("-- Calculando valores de VI e incremento...", end="")
        vi = round(vlr_produtos / 100, 0)
        possiveis_incrementos = [
            50,
            100,
            200,
            500,
            1000,
            2000,
            5000,
            10000,
            20000,
            50000,
            100000,
        ]
        incremento = closest(possiveis_incrementos, vi / 10)
        print("OK")

        print("-- Inserindo linha na planilha colunada...", end="")
        colunada["Nº do lote"].append(contador)
        colunada["Status"].append("novo")
        colunada["Lote Ref. / Ativo-Frota"].append(ref_lote)
        colunada["Nome do Lote (SEMPRE MAIUSCULA)"].append(des_lote)
        colunada["Descrição"].append("Para maiores informações, clique em ANEXOS")
        colunada["VI"].append(vi)
        colunada["VMV"].append(0)
        colunada["VER"].append(0)
        colunada["Incremento"].append(incremento)
        colunada["Valor de Referência do Vendedor (Contábil)"].append(vlr_produtos)
        colunada["Comitente"].append(nom_unidade)
        colunada["Município"].append(cidade_estado[0])
        colunada["UF"].append(cidade_estado[1])
        colunada["Assessor"].append(nom_acessor)
        colunada["Pendências"].append("")
        colunada["Restrições"].append("")
        colunada["Débitos (Total)"].append("")
        colunada["Unid. Métrica"].append("")
        colunada["Fator Multiplicativo"].append("1")
        colunada["Alteração/Adicionado"].append("")
        colunada["Descrição HTML"].append("Em arquivo separado")
        df_colunada = pandas.DataFrame(colunada)
        print("OK")
    else:
        print('\nNÃO PROCESSANDO O ARQUIVO "' + full_file_name + '"')
        print("-- Este script processa apenas arquivos com extensão XLSX.")

print("\nExportando planilha resultante para Excel...", end="")
# you will probably notice that by default, pandas writes the line index as the first column in the spreadsheet
# if you don't want that, you can switch it off by adding the parameter index=False
df_colunada.to_excel(
    os.path.join(output_folder, "Planilha", "Geral_UtilizadaAtualmente" + ".xlsx"),
    index=False,
)
print("OK")

print("Processo finalizado com sucesso")
