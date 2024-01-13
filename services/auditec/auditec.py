import os
import re
import string
import pandas
import requests
import zipfile

from logger import Logger

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


def transform_num_laudo(value):
    if value == "" or value == "N/I":
        value = "0"
    return int(float(value))


def transform_marca(row):
    marca = row["Marca"].upper().strip()
    return marca


def transform_modelo(row):
    modelo = row["Modelo"].upper().strip()
    blindado = row["Veículo Blindado"].upper().strip()

    if blindado == "SIM":
        modelo = modelo + " (BLINDADO)"

    return modelo


def transform_placa(row):
    return (row["Placa"] + " (" + row["UF"] + ")").upper().strip()


def transform_chassi(value):
    return value.upper().strip()


def transform_cidade(value):
    return value.upper().strip()


def transform_uf(value):
    return value.upper().strip()


def transform_no_de_portas(value):
    if value == "" or value == "N/I":
        value = "0"
    return int(float(value))


def transform_kilometragem(value):
    if value == "" or value == "N/I":
        value = "0"
    return int(float(value))


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


def map_chave_original():
    return {
        "OK": "Chave principal: Sim",
        "EXTRAVIOU": "Chave principal: Não",
        "DANIFICADO": "Chave principal: Não",
        "": "Chave principal: Não",
    }


def map_chave_reserva():
    return {
        "OK": "Chave reserva: Sim",
        "EXTRAVIOU": "Chave reserva: Não",
        "DANIFICADO": "Chave reserva: Não",
        "": "Chave reserva: Não",
    }


def map_manual():
    return {
        "OK": "Manual: Sim",
        "EXTRAVIOU": "Manual: Não",
        "DANIFICADO": "Manual: Não",
        "": "Manual: Não",
    }


def extract_direcao(value):
    if "DIRECAO HIDRAULICA" in value:
        return "Hidráulica"

    return ""


def extract_ar_condicionado(value):
    if "AR CONDICIONADO" in value:
        return "Sim"

    return ""


def extract_vidros(value):
    if "VIDRO ELETRICO" in value:
        return "Elétricos"
    elif "TRIO ELETRICO" in value:
        return "Elétricos"
    elif "VIDRO LATERAL CORREDICO" in value:
        return "Manuais"
    elif "VIDRO TRASEIRO CORREDICO" in value:
        return "Manuais"

    return ""


def extract_rodas(value):
    if "RODA LIGA LEVE/ESPORTIVA" in value:
        return "Liga-Leve"

    return ""


def extract_banco(value):
    if "BANCO COURO E ELETRICO" in value:
        return "Couro"
    elif "BANCO DE COURO" in value:
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
    acessorios = acessorios.replace("VIDRO VERDE, ", "").replace("VIDRO VERDE", "")
    acessorios = acessorios.replace("VIDROS VERDES, ", "").replace("VIDROS VERDES", "")
    acessorios = acessorios.replace("QUEBRA-SOL EXTERNO, ", "").replace(
        "QUEBRA-SOL EXTERNO", ""
    )
    acessorios = acessorios.replace("TURBO, ", "").replace("TURBO", "")
    acessorios = acessorios.replace("INSUFILME, ", "").replace("INSUFILME", "")
    acessorios = acessorios.replace("INSULFILME, ", "").replace("INSULFILME", "")
    acessorios = acessorios.replace("LIMPADOR TRASEIRO, ", "").replace(
        "LIMPADOR TRASEIRO", ""
    )
    acessorios = acessorios.replace("CARPETE, ", "").replace("CARPETE", "")
    acessorios = acessorios.replace("ENCOSTO DE CABECA, ", "").replace(
        "ENCONSTO DE CABECA", ""
    )
    acessorios = acessorios.replace("ENCOSTO DE CABEÇA, ", "").replace(
        "ENCONSTO DE CABEÇA", ""
    )
    acessorios = acessorios.replace("TAPETE, ", "").replace("TAPETE", "")
    acessorios = acessorios.replace("CONSOLE, ", "").replace("CONSOLE", "")
    acessorios = acessorios.replace("DESEMBACADOR TRASEIRO, ", "").replace(
        "DESEMBACADOR TRASEIRO", ""
    )
    acessorios = acessorios.replace("DESEMBAÇADOR TRASEIRO, ", "").replace(
        "DESEMBAÇADOR TRASEIRO", ""
    )
    acessorios = acessorios.replace("VOLANTE ESCAM., ", "").replace(
        "VOLANTE ESCAM.", ""
    )
    acessorios = acessorios.replace("VOLANTE ESCAMOTEAVEL, ", "").replace(
        "VOLANTE ESCAMOTEAVEL", ""
    )
    acessorios = acessorios.replace("VOLANTE ESCAMOTEÁVEL, ", "").replace(
        "VOLANTE ESCAMOTEÁVEL", ""
    )
    acessorios = acessorios.replace("AR QUENTE, ", "").replace("AR QUENTE", "")
    acessorios = acessorios.replace("AUTO-FAL. ORIG./SIMILAR., ", "").replace(
        "AUTO-FAL. ORIG./SIMILAR.", ""
    )
    acessorios = acessorios.replace("PARA-BRISA DIANT DEGRADE, ", "").replace(
        "PARA-BRISA DIANT DEGRADE", ""
    )
    acessorios = acessorios.replace("PARA-BRISA DIANT DEGRADE, ", "").replace(
        "PARA-BRISA DIANT DEGRADE", ""
    )
    acessorios = acessorios.replace("CAMBIO AUTOMAT./SIMILAR, ", "").replace(
        "CAMBIO AUTOMAT./SIMILAR", ""
    )
    acessorios = acessorios.replace("DVD/MULTIMIDIA, ", "").replace(
        "DVD/MULTIMIDIA", ""
    )
    acessorios = acessorios.replace("EQUIP SOM/IMAGEM/CONECT., ", "").replace(
        "EQUIP SOM/IMAGEM/CONECT.", ""
    )
    acessorios = acessorios.replace("RADIO AM/FM, ", "").replace("RADIO AM/FM", "")
    acessorios = acessorios.replace("RADIO AM/FM/DISC-LASER, ", "").replace(
        "RADIO AM/FM/DISC-LASER", ""
    )
    acessorios = acessorios.replace("RADIO AM/FM/TOCA-FITAS, ", "").replace(
        "RADIO AM/FM/TOCA-FITAS", ""
    )
    acessorios = acessorios.replace("RADIO COMUNIC./SIMILAR, ", "").replace(
        "RADIO COMUNIC./SIMILAR", ""
    )
    acessorios = acessorios.replace("RADIO DISC LASER F. REM., ", "").replace(
        "RADIO DISC LASER F. REM.", ""
    )
    acessorios = acessorios.replace("RADIO FM CD/DVD TELA LCD, ", "").replace(
        "RADIO FM CD/DVD TELA LCD", ""
    )
    acessorios = acessorios.replace("RADIO FM/T.FITAS/CD, ", "").replace(
        "RADIO FM/T.FITAS/CD", ""
    )
    acessorios = acessorios.replace("RADIO FM/T.FITAS/TV, ", "").replace(
        "RADIO FM/T.FITAS/TV", ""
    )
    acessorios = acessorios.replace("RADIO FM/T.FITAS-F. REM., ", "").replace(
        "RADIO FM/T.FITAS-F. REM.", ""
    )
    acessorios = acessorios.replace("RADIO FM-FRENTE REMOV., ", "").replace(
        "RADIO FM-FRENTE REMOV.", ""
    )
    acessorios = acessorios.replace("CACAMBA, ", "CAÇAMBA, ").replace(
        "CACAMBA", "CAÇAMBA"
    )
    acessorios = acessorios.replace("TRIANGULO, ", "TRIÂNGULO, ").replace(
        "TRIANGULO", "TRIÂNGULO"
    )
    acessorios = acessorios.replace("TROCA, ", "AVARIADO, ").replace(
        "TROCA", "AVARIADO"
    )
    acessorios = acessorios.replace("ARRANHADO, ", "RALADO, ").replace(
        "ARRANHADO", "RALADO"
    )
    acessorios = acessorios.replace("RISCADO, ", "RISCADO, ").replace(
        "RISCADO", "RISCADO"
    )
    acessorios = acessorios.replace("AMASSADO, ", "AMASSADO, ").replace(
        "AMASSADO", "AMASSADO"
    )
    acessorios = acessorios.replace("QUEBRADO, ", "AVARIADO, ").replace(
        "QUEBRADO", "AVARIADO"
    )
    acessorios = acessorios.replace("RECUPERA, ", "AVARIADO, ").replace(
        "RECUPERA", "AVARIADO"
    )
    acessorios = acessorios.replace("OUTROS, ", "AVARIADO, ").replace(
        "OUTROS", "AVARIADO"
    )
    acessorios = acessorios.replace(", ", " <br> ")

    avarias = row["Avarias"].upper().strip()
    avarias = re.sub(r" - \d+CM", "", avarias)
    avarias = avarias.replace("CARROCARIA, ", "CARROCERIA, ").replace(
        "CARROCARIA", "CARROCERIA"
    )
    avarias = avarias.replace("CACAMBA, ", "CAÇAMBA, ").replace("CACAMBA", "CAÇAMBA")
    avarias = avarias.replace("TRIANGULO, ", "TRIÂNGULO, ").replace(
        "TRIANGULO", "TRIÂNGULO"
    )
    avarias = avarias.replace("TROCA, ", "AVARIADO, ").replace("TROCA", "AVARIADO")
    avarias = avarias.replace("ARRANHADO, ", "RALADO, ").replace("ARRANHADO", "RALADO")
    avarias = avarias.replace("RISCADO, ", "RISCADO, ").replace("RISCADO", "RISCADO")
    avarias = avarias.replace("AMASSADO, ", "AMASSADO, ").replace(
        "AMASSADO", "AMASSADO"
    )
    avarias = avarias.replace("QUEBRADO, ", "AVARIADO, ").replace(
        "QUEBRADO", "AVARIADO"
    )
    avarias = avarias.replace("RECUPERA, ", "AVARIADO, ").replace(
        "RECUPERA", "AVARIADO"
    )
    avarias = avarias.replace("OUTROS, ", "AVARIADO, ").replace("OUTROS", "AVARIADO")
    avarias = avarias.replace(", ", " <br> ")

    if len(acessorios) > 0 and len(avarias) > 0:
        return (
            (
                "Acessórios:<br><br>"
                + string.capwords(acessorios).replace(" <br> ", "<br>")
                + "<br><br>Avarias:<br><br>"
                + string.capwords(avarias).replace(" <br> ", "<br>")
            )
            .replace(" - ", ": ")
            .replace("<br><br><br>", "<br><br>")
        )
    elif len(acessorios) > 0:
        return "Acessórios:<br><br>" + string.capwords(acessorios).replace(
            " <br> ", "<br>"
        ).replace(" - ", ": ").replace("<br><br><br>", "<br><br>")
    elif len(avarias) > 0:
        return "Avarias:<br><br>" + string.capwords(avarias).replace(
            " <br> ", "<br>"
        ).replace(" - ", ": ").replace("<br><br><br>", "<br><br>")

    return ""


def transform_informacoes_analise(row):
    motor = row["Motor"].replace("-", "").upper().strip()
    ressalvas = row["Motivos de Ressalva"].upper().strip()
    obs = row["OBS"].upper().strip()

    count = 0
    informacoes_analise = ""

    if len(motor) > 0:
        count = count + 1
        if count == 1:
            informacoes_analise = "MOTOR: " + motor
        else:
            informacoes_analise = informacoes_analise + " / MOTOR: " + motor

    if len(ressalvas) > 0:
        count = count + 1
        if ressalvas[-1] == ",":
            ressalvas = ressalvas[0 : len(ressalvas) - 1]
        if count == 1:
            informacoes_analise = "MOTIVOS DE RESSALVA: " + ressalvas
        else:
            informacoes_analise = (
                informacoes_analise + " / MOTIVOS DE RESSALVA: " + ressalvas
            )

    if len(obs) > 0:
        count = count + 1
        if count == 1:
            informacoes_analise = "OBSERVAÇÕES: " + obs
        else:
            informacoes_analise = informacoes_analise + " / OBSERVAÇÕES: " + obs

    return informacoes_analise


def transform_nome_caminhao(row):
    tipo = row["Tipo / Categoria"].upper().strip()

    arr_partes = tipo.split("/")
    nome = arr_partes[0].strip()

    if nome == "CAMINHAO TRATOR":
        nome = "CAVALO MECÂNICO"

    return nome


create_folder(input_folder)
create_folder(output_folder)
create_folder(output_folder, images_folder)
create_folder(output_folder, logs_folder)
create_folder(output_folder, xlsx_folder)
create_folder(output_folder, zip_folder)

for excel_file_name in get_files_list(input_folder, ["xlsx"]):
    logger.info(f'Lendo a planilha da Auditec "{excel_file_name}"')
    planilha_auditec = pandas.read_excel(os.path.join(input_folder, excel_file_name))

    logger.info("Convertendo todas as colunas para texto")
    planilha_auditec = planilha_auditec.astype(str)

    logger.info(
        "Desconsiderando as linhas cujos valores de todas as colunas estão vazios"
    )
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("None")).dropna(
        how="all"
    )
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("None")).fillna("")
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("nan")).dropna(
        how="all"
    )
    planilha_auditec = planilha_auditec.mask(planilha_auditec.eq("nan")).fillna("")

    logger.info("Criando a planilha da Mais Ativo")
    excel_file = pandas.ExcelWriter(
        os.path.join(
            "output", "xlsx", "Planilha_Unificada_2022_v7.2_" + excel_file_name
        ),
        engine="xlsxwriter",
    )

    # VEÍCULOS LEVES
    logger.info("Processando Veículos Leves")

    logger.info("* Filtrando os dados de Veículos Leves da planilha da Auditec")
    dados_auditec_veiculos_leves = planilha_auditec.query(
        'TEMPLATE == "VEÍCULOS LEVES"'
    )

    logger.info("* Formatando os dados de Veículos Leves para a planilha da Mais Ativo")
    aba_veiculos_leves = pandas.DataFrame(
        columns=[
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
            "Assessor",
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
    )

    aba_veiculos_leves["Lote Ref. / Ativo-Frota"] = dados_auditec_veiculos_leves[
        "Laudo N°"
    ].map(transform_num_laudo)
    aba_veiculos_leves["Tabela Molicar"] = ""
    aba_veiculos_leves["Tabela Fipe"] = ""
    aba_veiculos_leves["Proprietário/CNPJ (Proprietário do documento)"] = ""
    aba_veiculos_leves["Restrições"] = ""
    aba_veiculos_leves["Débitos (Total)"] = ""
    aba_veiculos_leves["Tipo"] = ""
    aba_veiculos_leves["Marca (SEMPRE MAIUSCULA)"] = dados_auditec_veiculos_leves.apply(
        transform_marca, axis=1
    )
    aba_veiculos_leves[
        "Modelo (SEMPRE MAIUSCULA)"
    ] = dados_auditec_veiculos_leves.apply(transform_modelo, axis=1)
    aba_veiculos_leves["Ano Fab/Modelo"] = ""
    aba_veiculos_leves[
        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))"
    ] = dados_auditec_veiculos_leves.apply(transform_placa, axis=1)
    aba_veiculos_leves["Chassi (SEMPRE MAIUSCULA)"] = dados_auditec_veiculos_leves[
        "Chassi"
    ].map(transform_chassi)
    aba_veiculos_leves["Renavam"] = ""
    aba_veiculos_leves["Cor"] = ""
    aba_veiculos_leves["Combustível"] = ""
    aba_veiculos_leves["Município"] = dados_auditec_veiculos_leves["Cidade"].map(
        transform_cidade
    )
    aba_veiculos_leves["UF"] = dados_auditec_veiculos_leves["UF"].map(transform_uf)
    aba_veiculos_leves["Assessor"] = "AUDITEC"
    aba_veiculos_leves["Nº de Portas"] = dados_auditec_veiculos_leves["Nr. Portas"].map(
        transform_no_de_portas
    )
    aba_veiculos_leves["Kilometragem"] = dados_auditec_veiculos_leves["KM"].map(
        transform_kilometragem
    )
    aba_veiculos_leves["Motor"] = dados_auditec_veiculos_leves["Condição do Motor"].map(
        map_motor()
    )
    aba_veiculos_leves["Câmbio"] = dados_auditec_veiculos_leves["Tipo de Câmbio"].map(
        map_cambio()
    )
    aba_veiculos_leves["Direção"] = dados_auditec_veiculos_leves["Acessórios"].map(
        extract_direcao
    )
    aba_veiculos_leves["Ar condicionado"] = dados_auditec_veiculos_leves[
        "Acessórios"
    ].map(extract_ar_condicionado)
    aba_veiculos_leves["Vidros"] = dados_auditec_veiculos_leves["Acessórios"].map(
        extract_vidros
    )
    aba_veiculos_leves["Rodas"] = dados_auditec_veiculos_leves["Acessórios"].map(
        extract_rodas
    )
    aba_veiculos_leves["Banco"] = dados_auditec_veiculos_leves["Acessórios"].map(
        extract_banco
    )
    aba_veiculos_leves["Aparelho de Som"] = dados_auditec_veiculos_leves[
        "Rádio / CD / DVD"
    ].map(map_radio())
    aba_veiculos_leves["Pintura"] = ""
    aba_veiculos_leves["Lataria"] = ""
    aba_veiculos_leves["Tapeçaria"] = ""
    aba_veiculos_leves["Pneus"] = ""
    aba_veiculos_leves["Obs."] = (
        dados_auditec_veiculos_leves["Chave Original"].map(map_chave_original())
        + "<br>"
        + dados_auditec_veiculos_leves["Chave Reserva"].map(map_chave_reserva())
        + "<br>"
        + dados_auditec_veiculos_leves["Manual Uso / Manutenção"].map(map_manual())
        + "<br><br>"
        + dados_auditec_veiculos_leves.apply(transform_observacoes, axis=1)
    )
    aba_veiculos_leves["Informações para Análise"] = dados_auditec_veiculos_leves.apply(
        transform_informacoes_analise, axis=1
    )
    aba_veiculos_leves["Pendências"] = ""
    aba_veiculos_leves["Descrição Html"] = ""
    aba_veiculos_leves["Fotos"] = ""

    logger.info(
        "* Gravando os dados para a aba de Veículos Leves na planilha da Mais Ativo"
    )
    aba_veiculos_leves.to_excel(excel_file, sheet_name="Veic.Leves", index=False)
    # FIM VEÍCULOS LEVES

    # CAMINHÕES
    logger.info("Processando Caminhões")

    logger.info("* Filtrando os dados de Caminhões da planilha da Auditec")
    dados_auditec_caminhoes = planilha_auditec.query('TEMPLATE == "CAMINHÕES"')

    logger.info("* Formatando os dados de Veículos Leves para a planilha da Mais Ativo")
    aba_caminhoes = pandas.DataFrame(
        columns=[
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
            "Endereço (via geolocalização Memento)",
            "Município",
            "UF",
            "Assessor",
            "Nome (CAMINHÃO + CARROCERIA OU CAVALO MECÂNICO)",
            "Kilometragem",
            "Eixos",
            "Tração",
            "Carroceria",
            "Cardan",
            "Diferencial",
            "Motor",
            "Câmbio",
            "Tapeçaria/Forração",
            "Pintura",
            "Lataria",
            "Bancos",
            "Qtd. de Pneus",
            "Estado dos Pneus",
            "Obs.",
            "Informações para Análise",
            "Pendências",
            "Descrição Html",
            "Fotos",
        ]
    )

    aba_caminhoes["Lote Ref. / Ativo-Frota"] = dados_auditec_caminhoes["Laudo N°"].map(
        transform_num_laudo
    )
    aba_caminhoes["Tabela Molicar"] = ""
    aba_caminhoes["Tabela Fipe"] = ""
    aba_caminhoes["Proprietário/CNPJ (Proprietário do documento)"] = ""
    aba_caminhoes["Restrições"] = ""
    aba_caminhoes["Débitos (Total)"] = ""
    aba_caminhoes["Tipo"] = ""
    aba_caminhoes["Marca (SEMPRE MAIUSCULA)"] = dados_auditec_caminhoes.apply(
        transform_marca, axis=1
    )
    aba_caminhoes["Modelo (SEMPRE MAIUSCULA)"] = dados_auditec_caminhoes.apply(
        transform_modelo, axis=1
    )
    aba_caminhoes["Ano Fab/Modelo"] = ""
    aba_caminhoes[
        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))"
    ] = dados_auditec_caminhoes.apply(transform_placa, axis=1)
    aba_caminhoes["Chassi (SEMPRE MAIUSCULA)"] = dados_auditec_caminhoes["Chassi"].map(
        transform_chassi
    )
    aba_caminhoes["Renavam"] = ""
    aba_caminhoes["Cor"] = ""
    aba_caminhoes["Combustível"] = ""
    aba_caminhoes["Endereço (via geolocalização Memento)"] = ""
    aba_caminhoes["Município"] = dados_auditec_caminhoes["Cidade"].map(transform_cidade)
    aba_caminhoes["UF"] = dados_auditec_caminhoes["UF"].map(transform_uf)
    aba_caminhoes["Assessor"] = "AUDITEC"
    aba_caminhoes[
        "Nome (CAMINHÃO + CARROCERIA OU CAVALO MECÂNICO)"
    ] = dados_auditec_caminhoes.apply(transform_nome_caminhao, axis=1)
    aba_caminhoes["Kilometragem"] = dados_auditec_caminhoes["KM"].map(
        transform_kilometragem
    )
    aba_caminhoes["Eixos"] = ""
    aba_caminhoes["Tração"] = ""
    aba_caminhoes["Carroceria"] = ""
    aba_caminhoes["Cardan"] = ""
    aba_caminhoes["Diferencial"] = ""
    aba_caminhoes["Motor"] = dados_auditec_caminhoes["Condição do Motor"].map(
        map_motor()
    )
    aba_caminhoes["Câmbio"] = dados_auditec_caminhoes["Tipo de Câmbio"].map(
        map_cambio()
    )
    aba_caminhoes["Tapeçaria/Forração"] = ""
    aba_caminhoes["Pintura"] = ""
    aba_caminhoes["Lataria"] = ""
    aba_caminhoes["Bancos"] = dados_auditec_caminhoes["Acessórios"].map(extract_banco)
    aba_caminhoes["Qtd. de Pneus"] = ""
    aba_caminhoes["Estado dos Pneus"] = ""
    aba_caminhoes["Obs."] = (
        dados_auditec_caminhoes["Chave Original"].map(map_chave_original())
        + "<br>"
        + dados_auditec_caminhoes["Chave Reserva"].map(map_chave_reserva())
        + "<br>"
        + dados_auditec_caminhoes["Manual Uso / Manutenção"].map(map_manual())
        + "<br><br>"
        + dados_auditec_caminhoes.apply(transform_observacoes, axis=1)
    )
    aba_caminhoes["Informações para Análise"] = dados_auditec_caminhoes.apply(
        transform_informacoes_analise, axis=1
    )
    aba_caminhoes["Pendências"] = ""
    aba_caminhoes["Descrição Html"] = ""
    aba_caminhoes["Fotos"] = ""

    logger.info("* Gravando os dados para a aba de Caminhões na planilha da Mais Ativo")
    aba_caminhoes.to_excel(excel_file, sheet_name="Camin.", index=False)
    # FIM CAMINHÕES

    logger.info("Salvando e fechando a planilha da Mais Ativo")
    excel_file.close()

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
