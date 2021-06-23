import os
import pandas
from services.base.spreadsheet_converter import SpreadsheetConverter


class DedaloConverter(SpreadsheetConverter):
    def process_file(self, file):
        print("IMPORTANDO AQUIVO")
        sheet = pandas.read_excel(file)
        sheet["DESCRIÇÃO"] = sheet["DESCRIÇÃO"].apply(
            lambda x: self.remove_prefix(x, "Lote com").strip().capitalize()
        )

        if "INFORMAÇÕES COMPLEMENTARES" in sheet.columns:
            sheet["INFORMAÇÕES COMPLEMENTARES"] = sheet[
                "INFORMAÇÕES COMPLEMENTARES"
            ].fillna("")

            sheet[
                "INFORMAÇÕES COMPLEMENTARES"
            ] = "<br><br>#PRODUCT_DESCRIPTION" + sheet[
                "INFORMAÇÕES COMPLEMENTARES"
            ].astype(
                str
            )

            sheet["INFORMAÇÕES COMPLEMENTARES"] = sheet.apply(
                lambda x: x["INFORMAÇÕES COMPLEMENTARES"].replace(
                    "#PRODUCT_DESCRIPTION", x["DESCRIÇÃO"]
                ),
                axis=1,
            )

        data = sheet.to_dict("list")
        data_to_output = dict()
        data_to_output["Nº do lote"] = data["LOTE"]
        data_to_output["Status"] = "novo"
        data_to_output["Lote Ref. / Ativo-Frota"] = ""
        data_to_output["Nome do Lote (SEMPRE MAIUSCULA)"] = sheet[
            "DESCRIÇÃO"
        ].str.upper()
        data_to_output["Descrição"] = (
            data["INFORMAÇÕES COMPLEMENTARES"]
            if "INFORMAÇÕES COMPLEMENTARES" in data
            else ""
        )
        data_to_output["VI"] = data["BASE"]
        data_to_output["VMV"] = ""
        data_to_output["VER"] = ""
        data_to_output["Incremento"] = data["INCREMENTO"]
        data_to_output["Valor de Referência do Vendedor (Contábil)"] = ""
        data_to_output["Comitente"] = "Dédalo Leilões"
        data_to_output["Município"] = "São Paulo"
        data_to_output["UF"] = "SP"
        data_to_output["Assessor"] = "Vendedor"
        data_to_output["Pendências"] = ""
        data_to_output["Restrições"] = ""
        data_to_output["Débitos (Total)"] = ""
        data_to_output["Unid. Métrica"] = ""
        data_to_output["Fator Multiplicativo"] = "1"
        data_to_output["Alteração/Adicionado"] = ""
        data_to_output["Descrição HTML"] = ""

        file_name = os.path.basename(file)
        writer = pandas.ExcelWriter(
            f"{os.path.join('output/xlsx')}/{file_name}", engine="xlsxwriter"
        )

        df = pandas.DataFrame(data_to_output)
        df["VI"] = pandas.to_numeric(df["VI"])
        df.to_excel(writer, sheet_name="Colunada", index=False)
        writer.save()


if __name__ == "__main__":
    dedaloConverter = DedaloConverter(
        ".",
        ["input"],
        [
            "output",
            os.path.join("output", "xlsx"),
        ],
    )
    dedaloConverter.execute()
