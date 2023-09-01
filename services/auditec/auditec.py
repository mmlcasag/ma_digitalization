import os
import string
import pandas
import requests
import zipfile

from services.base.logger import Logger

logger = Logger.__call__().get_logger()

input_folder = "input"
output_folder = "output"
images_folder = "images"
logs_folder = "logs"
xlsx_folder = "xlsx"
zip_folder = "zip"


def create_folder(folder_name, subfolder_name=""):
    if not subfolder_name:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    else:
        if not os.path.exists(os.path.join(folder_name, subfolder_name)):
            os.makedirs(os.path.join(folder_name, subfolder_name))


def get_files_list(folder_name, file_extension_list=[]):
    files_list = []

    if not os.path.isdir(folder_name):
        return files_list

    if len(file_extension_list) == 0:
        files_list = os.listdir(folder_name)
    else:
        for file_name in os.listdir(folder_name):
            for file_extension in file_extension_list:
                if file_name.endswith(file_extension):
                    files_list.append(file_name)

    return files_list


def get_columns_planilha_maisativo():
    return [
        "Lote Ref. / Ativo-Frota",
        "Tabela Molicar",
        "Tabela Fipe",
        "Proprietário/CNPJ (Proprietário do documento)",
        "Restrições",
        "Débitos (Total)",
        "Tipo",
        "Marca (SEMPRE MAIUSCULA)",
        "Modelo (SEMPRE MAIUSCULA)",
        "Ano Fab/Modelo",
        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))",
        "Chassi (SEMPRE MAIUSCULA)",
        "Renavam",
        "Cor",
        "Combustível",
        "Município",
        "UF",
        "Acessor",
        "Nº de Portas",
        "Kilometragem",
        "Motor",
        "Câmbio",
        "Direção",
        "Ar condicionado",
        "Vidros",
        "Rodas",
        "Banco",
        "Aparelho de Som",
        "Pintura",
        "Lataria",
        "Tapeçaria",
        "Pneus",
        "Obs.",
        "Informações para Análise",
        "Pendências",
        "Descrição Html",
        "Fotos",
    ]


def transform_placa(row):
    return (row["Placa"] + " (" + row["UF"] + ")").upper().strip()


def transform_chassi(value):
    return value.upper().strip()


def transform_cidade(value):
    return value.upper().strip()


def transform_uf(value):
    return value.upper().strip()


def transform_no_de_portas(value):
    return value.replace("N/I", "").upper().strip()


def transform_kilometragem(value):
    return str(value).replace("0", "").upper().strip()


def map_motor():
    return {
        "NAO INFORMADO": "Não testado",
        "FUNCIONANDO": "Funcionando",
        "NÃO FUNCIONA": "Não Funcionando",
        "NÃO TESTADO": "Não Testado",
        "FALTA": "Falta",
        "DESMONTADO/AVARIADO PODENDO FALTAR PEÇAS": "Desmontado/Avariado, podendo faltar peças",
        "AVARIADO PODENDO FALTAR PEÇAS E PARTES": "Avariado/Podendo faltas peças e partes",
        "AVARIADO FALTANDO PEÇAS E PARTES": "Avariado/Faltando peças e partes",
    }


def map_cambio():
    return {"AUTOMÁTICO": "Automático", "MECÂNICO": "Manual", "NÃO POSSUI": "Falta"}


def extract_direcao(value):
    if "DIRECAO HIDRAULICA" in value:
        return "Hidráulica"

    return ""


def extract_ar_condicionado(value):
    if "AR CONDICIONADO":
        return "Sim"

    return ""


def extract_vidros(value):
    if "VIDRO ELETRICO":
        return "Elétricos"
    elif "VIDRO LATERAL CORREDICO":
        return "Manuais"
    elif "VIDRO TRASEIRO CORREDICO":
        return "Manuais"

    return ""


def extract_rodas(value):
    if "RODA LIGA LEVE/ESPORTIVA":
        return "Liga-Leve"

    return ""


def extract_banco(value):
    if "BANCO COURO E ELETRICO":
        return "Couro"
    elif "BANCO DE COURO":
        return "Couro"

    return ""


def map_radio():
    return {
        "OK": "Sim",
        "FALTANTE": "Não",
        "QUEBRADO": "Avariado",
        "AMASSADO": "Avariado",
        "DESCASCADO": "Avariado",
        "CORTADO": "Avariado",
        "FURADO": "Avariado",
        "MANCHADO": "Avariado",
        "NAO FUNCIONA": "Avariado",
        "NAO INFORMADO": "",
    }


def transform_observacoes(row):
    acessorios = row["Acessórios"].upper().strip()
    avarias = (
        row["Avarias"]
        .upper()
        .strip()
        .replace(" - 1CM", "")
        .replace(" - 99CM", "")
        .replace(" - ", ": ")
    )

    acessorios = acessorios.replace("DIRECAO HIDRAULICA, ", "").replace(
        "DIRECAO HIDRAULICA", ""
    )
    acessorios = acessorios.replace("AR CONDICIONADO, ", "").replace(
        "AR CONDICIONADO", ""
    )
    acessorios = acessorios.replace("VIDRO ELETRICO, ", "").replace(
        "VIDRO ELETRICO", ""
    )
    acessorios = acessorios.replace("VIDRO LATERAL CORREDICO, ", "").replace(
        "VIDRO LATERAL CORREDICO", ""
    )
    acessorios = acessorios.replace("VIDRO TRASEIRO CORREDICO, ", "").replace(
        "VIDRO TRASEIRO CORREDICO", ""
    )
    acessorios = acessorios.replace("RODA LIGA LEVE/ESPORTIVA, ", "").replace(
        "RODA LIGA LEVE/ESPORTIVA", ""
    )
    acessorios = acessorios.replace("BANCO COURO E ELETRICO, ", "").replace(
        "BANCO COURO E ELETRICO", ""
    )
    acessorios = acessorios.replace("BANCO DE COURO, ", "").replace(
        "BANCO DE COURO", ""
    )

    acessorios = acessorios.replace(", ", " <br> ")
    avarias = avarias.replace(", ", " <br> ")

    if len(acessorios) > 0 and len(avarias) > 0:
        return (
            "ACESSÓRIOS:<br><br>"
            + string.capwords(acessorios).replace(" <br> ", "<br>")
            + "<br><br>AVARIAS:<br/><br/>"
            + string.capwords(avarias).replace(" <br> ", "<br>")
        )
    elif len(acessorios) > 0:
        return "ACESSÓRIOS:<br><br>" + string.capwords(acessorios).replace(
            " <br> ", "<br>"
        )
    elif len(avarias) > 0:
        return "AVARIAS:<br><br>" + string.capwords(avarias).replace(" <br> ", "<br>")

    return ""


def transform_informacoes_analise(row):
    motor = row["Motor"].replace("-", "").upper().strip()
    obs = row["OBS"].upper().strip()

    if len(motor) > 0 and len(obs) > 0:
        return "MOTOR: " + motor + " / OBSERVAÇÕES: " + obs
    elif len(motor) > 0:
        return "MOTOR: " + motor
    elif len(obs) > 0:
        return "OBSERVAÇÕES: " + obs

    return ""


create_folder(input_folder)
create_folder(output_folder)
create_folder(output_folder, images_folder)
create_folder(output_folder, logs_folder)
create_folder(output_folder, xlsx_folder)
create_folder(output_folder, zip_folder)

for excel_file_name in get_files_list(input_folder, ["xlsx"]):
    logger.info("Lendo o arquivo Excel no pandas")
    planilha_auditec = pandas.read_excel(os.path.join(input_folder, excel_file_name))

    logger.info("Convertendo todas as colunas para texto")
    planilha_auditec = planilha_auditec.astype(str)

    logger.info("Desconsiderando linhas cujos valores de todas as colunas estão vazios")
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("None")).dropna(
        how="all"
    )
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("None")).fillna("")
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("nan")).dropna(
        how="all"
    )
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("nan")).fillna("")

    logger.info("Convertendo apenas algumas colunas para numérico")
    planilha_auditec["Item"] = planilha_auditec["Item"].astype(float).astype(int)
    planilha_auditec["Agendamento"] = (
        planilha_auditec["Agendamento"].astype(float).astype(int)
    )
    planilha_auditec["Laudo N°"] = (
        planilha_auditec["Laudo N°"].astype(float).astype(int)
    )
    planilha_auditec["Ano Fabricação"] = (
        planilha_auditec["Ano Fabricação"].astype(float).astype(int)
    )
    planilha_auditec["Ano Modelo"] = (
        planilha_auditec["Ano Modelo"].astype(float).astype(int)
    )
    planilha_auditec["Renavam"] = planilha_auditec["Renavam"].astype(float).astype(int)
    planilha_auditec["Nr. CRLV"] = (
        planilha_auditec["Nr. CRLV"].astype(float).astype(int)
    )
    planilha_auditec["KM"] = planilha_auditec["KM"].astype(float).astype(int)

    logger.info("Formatando a planilha no padrão unificada da Mais Ativo")
    planilha_maisativo = pandas.DataFrame(columns=get_columns_planilha_maisativo())
    planilha_maisativo["Lote Ref. / Ativo-Frota"] = planilha_auditec["Laudo N°"]
    planilha_maisativo["Tabela Molicar"] = ""
    planilha_maisativo["Tabela Fipe"] = ""
    planilha_maisativo["Proprietário/CNPJ (Proprietário do documento)"] = ""
    planilha_maisativo["Restrições"] = ""
    planilha_maisativo["Débitos (Total)"] = ""
    planilha_maisativo["Tipo"] = ""
    planilha_maisativo["Marca (SEMPRE MAIUSCULA)"] = ""
    planilha_maisativo["Modelo (SEMPRE MAIUSCULA)"] = ""
    planilha_maisativo["Ano Fab/Modelo"] = ""
    planilha_maisativo[
        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))"
    ] = planilha_auditec.apply(transform_placa, axis=1)
    planilha_maisativo["Chassi (SEMPRE MAIUSCULA)"] = planilha_auditec["Chassi"].map(
        transform_chassi
    )
    planilha_maisativo["Renavam"] = ""
    planilha_maisativo["Cor"] = ""
    planilha_maisativo["Combustível"] = ""
    planilha_maisativo["Município"] = planilha_auditec["Cidade"].map(transform_cidade)
    planilha_maisativo["UF"] = planilha_auditec["UF"].map(transform_uf)
    planilha_maisativo["Acessor"] = "AUDITEC"
    planilha_maisativo["Nº de Portas"] = planilha_auditec["Nr. Portas"].map(
        transform_no_de_portas
    )
    planilha_maisativo["Kilometragem"] = planilha_auditec["KM"].map(
        transform_kilometragem
    )
    planilha_maisativo["Motor"] = planilha_auditec["Condição do Motor"].map(map_motor())
    planilha_maisativo["Câmbio"] = planilha_auditec["Tipo de Câmbio"].map(map_cambio())
    planilha_maisativo["Direção"] = planilha_auditec["Acessórios"].map(extract_direcao)
    planilha_maisativo["Ar condicionado"] = planilha_auditec["Acessórios"].map(
        extract_ar_condicionado
    )
    planilha_maisativo["Vidros"] = planilha_auditec["Acessórios"].map(extract_vidros)
    planilha_maisativo["Rodas"] = planilha_auditec["Acessórios"].map(extract_rodas)
    planilha_maisativo["Banco"] = planilha_auditec["Acessórios"].map(extract_banco)
    planilha_maisativo["Aparelho de Som"] = planilha_auditec["Rádio / CD / DVD"].map(
        map_radio()
    )
    planilha_maisativo["Pintura"] = ""
    planilha_maisativo["Lataria"] = ""
    planilha_maisativo["Tapeçaria"] = ""
    planilha_maisativo["Pneus"] = ""
    planilha_maisativo["Obs."] = planilha_auditec.apply(transform_observacoes, axis=1)
    planilha_maisativo["Informações para Análise"] = planilha_auditec.apply(
        transform_informacoes_analise, axis=1
    )
    planilha_maisativo["Pendências"] = ""
    planilha_maisativo["Descrição Html"] = ""
    planilha_maisativo["Fotos"] = ""

    logger.info("Gerando o arquivo Excel resultante")

    logger.info("Montando o objeto de geração do arquivo Excel")
    excel_file = pandas.ExcelWriter(
        os.path.join(
            "output", "xlsx", "Planilha_Unificada_2022_v7.2_" + excel_file_name
        ),
        engine="xlsxwriter",
    )

    logger.info("Escrevendo na primeira aba da planilha")
    planilha_maisativo.to_excel(excel_file, sheet_name="Veículos Leves", index=False)

    logger.info("Salvando e fechando o arquivo Excel resultante")
    excel_file.close()

    logger.info("Arquivo Excel gerado com sucesso")

    logger.info("Extraindo as imagens da vistoria")

    for index, row in planilha_auditec.iterrows():
        laudo_number = str(row["Laudo N°"])
        zip_file_link = str(row["Fotos"])
        zip_file_path = os.path.join(output_folder, zip_folder, laudo_number + ".zip")

        logger.info("Linha: " + str(index))
        logger.info("Laudo Nº: " + laudo_number)
        logger.info("Link: " + zip_file_link)

        logger.info("* Baixando o arquivo zipado com as fotos")
        zip_file_data = requests.get(zip_file_link).content
        with open(zip_file_path, "wb") as handler:
            handler.write(zip_file_data)

        logger.info("* Extraindo as fotos do arquivo zipado")
        with zipfile.ZipFile(zip_file_path, "r") as zip_file:
            zip_file.extractall(
                os.path.join(output_folder, images_folder, laudo_number)
            )

        logger.info("* Deletando o arquivo zipado")
        os.remove(zip_file_path)

logger.info("Deletando a pasta de arquivos zipados")
os.rmdir(os.path.join(output_folder, zip_folder))

logger.info("Processo finalizado com sucesso.")
done = str(input("Pressione ENTER para encerrar..."))
