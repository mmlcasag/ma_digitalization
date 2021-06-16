import os
import sys
import pandas
import openpyxl
import utils.os as os_utils
import utils.ma as ma_utils
import utils.html as html_utils
import utils.excel as excel_utils

sys.path.append("..\..")

absolute_path = os.getcwd()

input_folder = "input"
output_folder = "output"
csv_folder = "csv"
html_folder = "html"
excel_folder = "xlsx"

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(os.path.join(output_folder, csv_folder))
os_utils.create_folder(os.path.join(output_folder, html_folder))
os_utils.create_folder(os.path.join(output_folder, excel_folder))

allowed_extensions = ["xlsx", "xlsb", "xlsm"]

dataset_sheet_1 = {
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

for excel_file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    file_name = os_utils.get_file_name(excel_file_name)

    workbook = openpyxl.load_workbook(
        os.path.join(input_folder, excel_file_name), data_only=True
    )

    sheet = workbook["1. Materiais"]
    excel_utils.delete_until(sheet, "NM")
    excel_utils.export_to_csv(
        sheet,
        os.path.join(output_folder, csv_folder, file_name + "_sheet_1.csv"),
        ";",
        ",",
    )

    sheet = workbook["2. Lotes"]
    sheet.delete_cols(1, 1)
    excel_utils.delete_until(sheet, "Nº do Lote")
    excel_utils.export_to_csv(
        sheet,
        os.path.join(output_folder, csv_folder, file_name + "_sheet_2.csv"),
        ";",
        ",",
    )

    workbook.close()

    df1 = pandas.read_csv(
        os.path.join(output_folder, csv_folder, file_name + "_sheet_1.csv"),
        delimiter=";",
    )
    df1 = df1.astype(str)

    df1_cols = list(df1.columns.values)
    df1 = df1[df1_cols[0:13]]

    df1 = df1.mask(df1.eq("None")).dropna()

    df1.iloc[:, 8] = round(df1.iloc[:, 8].astype(float), 2)
    df1.iloc[:, 9] = round(df1.iloc[:, 9].astype(float), 2)
    df1.iloc[:, 10] = round(df1.iloc[:, 10].astype(float), 2)

    df2 = pandas.read_csv(
        os.path.join(output_folder, csv_folder, file_name + "_sheet_2.csv"),
        delimiter=";",
    )
    df2 = df2.astype(str)

    df2_cols = list(df2.columns.values)
    df2 = df2[df2_cols[0:6]]

    df2 = df2.mask(df2.eq("None")).dropna()

    df2.iloc[:, 2] = round(df2.iloc[:, 2].astype(float), 2)
    df2.iloc[:, 3] = round(df2.iloc[:, 3].astype(float), 2)
    df2.iloc[:, 4] = round(df2.iloc[:, 4].astype(float), 2)
    df2.iloc[:, 5] = round(df2.iloc[:, 5].astype(float), 2)

    for asset_number in df1["Número do Lote"].unique():
        local_df1 = df1.loc[df1["Número do Lote"] == str(asset_number)]
        local_df1 = local_df1.reset_index(drop=True)
        local_df1_cols = list(local_df1.columns.values)

        local_df2 = df2.loc[df2["Nº do Lote"] == str(asset_number)]
        local_df2 = local_df2.reset_index(drop=True)
        local_df2_cols = list(local_df2.columns.values)

        html_df = local_df1[
            local_df1_cols[0:7] + [local_df1_cols[8]] + [local_df1_cols[7]]
        ]
        html_content = html_df.to_html(index=False, na_rep="")
        html_content = html_utils.get_header() + html_content + html_utils.get_footer()
        html_file_name = os.path.join(
            output_folder, html_folder, file_name + "_" + str(asset_number) + ".html"
        )
        html_file = open(html_file_name, "w", newline="", encoding="utf-8")
        html_file.write(html_content)
        html_file.close()

        asset_description = ma_utils.get_asset_description(
            local_df1, "TEXTO BREVE", "VALOR CONTÁBIL ATUAL", 5
        )
        asset_reference_value = round(local_df2.at[0, "Valor contábil total"], 2)
        asset_initial_value = round(local_df2.at[0, "Lance de Partida Leilão"], 2)
        asset_increment_value = int(
            ma_utils.get_closest_value(
                ma_utils.get_available_increments(), asset_initial_value / 10
            )
        )

        dataset_sheet_1["Nº do lote"].append(asset_number)
        dataset_sheet_1["Status"].append("novo")
        dataset_sheet_1["Lote Ref. / Ativo-Frota"].append(asset_number)
        dataset_sheet_1["Nome do Lote (SEMPRE MAIUSCULA)"].append(asset_description)
        dataset_sheet_1["Descrição"].append(
            "Para maiores informações, clique em ANEXOS"
        )
        dataset_sheet_1["VI"].append(asset_initial_value)
        dataset_sheet_1["VMV"].append(0)
        dataset_sheet_1["VER"].append(0)
        dataset_sheet_1["Incremento"].append(asset_increment_value)
        dataset_sheet_1["Valor de Referência do Vendedor (Contábil)"].append(
            asset_reference_value
        )
        dataset_sheet_1["Comitente"].append("Petrobrás")
        dataset_sheet_1["Município"].append("")
        dataset_sheet_1["UF"].append("")
        dataset_sheet_1["Assessor"].append("Vendedor")
        dataset_sheet_1["Pendências"].append("")
        dataset_sheet_1["Restrições"].append("")
        dataset_sheet_1["Débitos (Total)"].append("")
        dataset_sheet_1["Unid. Métrica"].append("")
        dataset_sheet_1["Fator Multiplicativo"].append("1")
        dataset_sheet_1["Alteração/Adicionado"].append("")
        dataset_sheet_1["Descrição HTML"].append("Em arquivo separado")

        dataframe_sheet_1 = pandas.DataFrame(dataset_sheet_1)
        dataframe_sheet_2 = pandas.DataFrame(df1)

    # create an pandas excel writer using xlsxwriter as the engine
    excel_file = pandas.ExcelWriter(
        os.path.join(output_folder, excel_folder, file_name + ".xlsx"),
        engine="xlsxwriter",
    )

    # write each dataframe to a specific sheet
    dataframe_sheet_1.to_excel(excel_file, sheet_name="Colunada", index=False)
    dataframe_sheet_2.to_excel(excel_file, sheet_name="Listagem", index=False)

    # close the pandas excel writer and save the excel file
    excel_file.save()

print("Done")
