import utils
import common
import xml.etree.ElementTree as ET
from services.base.logger import Logger

logger = Logger.__call__().get_logger()

CONST_BASE_ESTADUAL = "BaseEstadual_B"


def request_by_chassi(chassi):
    infocar_response = common.request_endpoint(CONST_BASE_ESTADUAL, None, chassi)
    return BaseEstadual(infocar_response)


def request_by_placa(placa):
    infocar_response = common.request_endpoint(CONST_BASE_ESTADUAL, placa, None)
    return BaseEstadual(infocar_response)


class BaseEstadual:
    def __init__(self, infocar_response):
        self.solicitacao = None
        self.dados_veiculo = None
        self.especificacoes = None
        self.restricoes = None
        self.intencao_financiamento = None
        self.debitos = None
        self.comunicacao_venda = None
        self.proprietario = None

        solicitacao_tag = None
        resposta_tag = None
        dados_veiculo_tag = None
        especificacoes_tag = None
        restricoes_tag = None
        restricoes_arr = []
        intencao_financiamento_tag = None
        debitos_tag = None
        comunicacao_venda_tag = None
        proprietario_tag = None

        envelope_tag = ET.fromstring(infocar_response)
        for body_tag in envelope_tag:
            for response_tag in body_tag:
                for result_tag in response_tag:
                    for info_xml_tag in result_tag:
                        for child in info_xml_tag:
                            if child.tag == "SOLICITACAO":
                                solicitacao_tag = child
                            if child.tag == "RESPOSTA":
                                resposta_tag = child

        for base_estadual_tag in resposta_tag:
            for child in base_estadual_tag:
                if child.tag == "DADOS_DO_VEICULO":
                    dados_veiculo_tag = child
                if child.tag == "INFORMACOES_TECNICAS_E_ADICIONAIS":
                    especificacoes_tag = child
                if child.tag == "RESTRICOES_E_IMPEDIMENTOS":
                    restricoes_tag = child
                    for restricao_inner in restricoes_tag:
                        if restricao_inner.tag == "RESTRICOES":
                            for restricoes in restricao_inner:
                                restricoes_arr.append(utils.to_string(restricoes.text))
                        if restricao_inner.tag == "INTENCAO_DE_FINANCIAMENTO":
                            intencao_financiamento_tag = restricao_inner
                if child.tag == "DEBITOS_ESTADUAIS":
                    debitos_tag = child
                if child.tag == "COMUNICACAO_DE_VENDAS":
                    comunicacao_venda_tag = child
                if child.tag == "PROPRIETARIO_S_":
                    proprietario_tag = child

        self.solicitacao = Solicitacao(solicitacao_tag)
        self.dados_veiculo = DadosVeiculo(dados_veiculo_tag)
        self.especificacoes = Especificacoes(especificacoes_tag)
        self.restricoes = Restricoes(restricoes_tag, restricoes_arr)
        self.intencao_financiamento = IntencaoFinanciamento(intencao_financiamento_tag)
        self.debitos = Debitos(debitos_tag)
        self.comunicacao_venda = ComunicacaoVenda(comunicacao_venda_tag)
        self.proprietario = Proprietario(proprietario_tag)

    def to_string(self):
        logger.debug(
            f"{self.solicitacao.to_string()}{self.dados_veiculo.to_string()}{self.especificacoes.to_string()}{self.restricoes.to_string()}{self.intencao_financiamento.to_string()}{self.debitos.to_string()}{self.comunicacao_venda.to_string()}{self.proprietario.to_string()}"
        )


class Solicitacao:
    def __init__(self, solicitacao_tag):
        dado = solicitacao_tag.find("DADO").text
        numero_resposta = solicitacao_tag.find("NUMERO_RESPOSTA").text
        tempo = solicitacao_tag.find("TEMPO").text
        mensagem = solicitacao_tag.find("MENSAGEM").text
        horario = solicitacao_tag.find("HORARIO").text

        mensagem_extenso = ""
        match (int(mensagem)):
            case 0:
                mensagem_extenso = "Não Possui Registro"
            case 1:
                mensagem_extenso = "Possui Registro"
            case 2:
                mensagem_extenso = "Falha de Autenticação"
            case 3:
                mensagem_extenso = "Dado/Tipo Incorreto"
            case 4:
                mensagem_extenso = "Erro na Pesquisa/Sistema Indisponível"
            case 5:
                mensagem_extenso = "Limite Diário Excedido"
            case _:
                mensagem_extenso = "Erro Desconhecido"

        self.dado = utils.to_string(dado)
        self.numero_resposta = utils.to_string(numero_resposta)
        self.tempo = utils.to_float(tempo, "US")
        self.mensagem = utils.to_string(mensagem_extenso)
        self.horario = utils.to_datetime(horario)

    def to_string(self):
        return f"\nSOLICITACAO:\n* Dado: {self.dado}\n* Número Resposta: {self.numero_resposta}\n* Tempo: {utils.from_float_to_string(self.tempo, 4)}\n* Mensagem: {self.mensagem}\n* Horário: {utils.from_datetime_to_string(self.horario)}"


class DadosVeiculo:
    def __init__(self, dados_veiculo_tag):
        placa = dados_veiculo_tag.find("PLACA").text
        chassi = dados_veiculo_tag.find("CHASSI").text
        municipio = dados_veiculo_tag.find("MUNICIPIO").text
        uf = dados_veiculo_tag.find("UF").text
        municipio_emplacado = dados_veiculo_tag.find("ORIGEM_DE_EMPLACAMENTO").text
        renavam = dados_veiculo_tag.find("RENAVAM").text
        cor = dados_veiculo_tag.find("COR").text
        modelo = dados_veiculo_tag.find("MODELO").text
        ano_modelo = dados_veiculo_tag.find("ANOMODELO").text
        ano_fabricacao = dados_veiculo_tag.find("ANOFABRICACAO").text
        combustivel = dados_veiculo_tag.find("COMBUSTIVEL").text
        tipo_combustivel = dados_veiculo_tag.find("TIPOVEICULO").text

        self.placa = utils.to_string(placa)
        self.chassi = utils.to_string(chassi)
        self.municipio = utils.to_string(municipio)
        self.uf = utils.to_string(uf)
        self.municipio_emplacado = utils.to_string(municipio_emplacado[0:-4])
        self.uf_emplacado = utils.to_string(municipio_emplacado[-3:-1])
        self.renavam = utils.to_string(renavam)
        self.cor = utils.to_string(cor)
        self.modelo = utils.to_string(modelo)
        self.ano_modelo = utils.to_string(ano_modelo)
        self.ano_fabricacao = utils.to_string(ano_fabricacao)
        self.combustivel = utils.to_string(combustivel)
        self.tipo_combustivel = utils.to_string(tipo_combustivel)

    def to_string(self):
        return f"\nDADOS VEICULO:\n* Placa: {self.placa}\n* Chassi: {self.chassi}\n* Município: {self.municipio}\n* UF: {self.uf}\n* Município Emplacado: {self.municipio_emplacado}\n* UF Emplacado: {self.uf_emplacado}\n* Renavam: {self.renavam}\n* Cor: {self.cor}\n* Modelo: {self.modelo}\n* Ano Modelo: {self.ano_modelo}\n* Ano Fabricação: {self.ano_fabricacao}\n* Combustível: {self.combustivel}\n* Tipo Combustível: {self.tipo_combustivel}"


class Especificacoes:
    def __init__(self, especificacoes_tag):
        motor = especificacoes_tag.find("MOTOR").text
        cambio = especificacoes_tag.find("CAIXADECAMBIO").text
        passageiros = especificacoes_tag.find("CAPACIDADEDEPASSAGEIROS").text
        potencia = especificacoes_tag.find("POTENCIA").text
        eixos = especificacoes_tag.find("QUANTIDADEDEEIXOS").text
        carga = especificacoes_tag.find("CAPACIDADEDECARGA").text
        cmt = especificacoes_tag.find("CMT").text
        pbt = especificacoes_tag.find("PBT").text
        num_carroceria = especificacoes_tag.find("NCARROCERIA").text
        eixo_traseiro = especificacoes_tag.find("NDOEIXOTRASEIRODIFERENCIAL").text
        terceiro_eixo = especificacoes_tag.find("NDOTERCEIROEIXO").text
        cilindradas = especificacoes_tag.find("CILINDRADAS").text
        especie = especificacoes_tag.find("ESPECIE").text
        categoria = especificacoes_tag.find("CATEGORIA").text
        carroceria = especificacoes_tag.find("CARROCERIA").text
        procedencia = especificacoes_tag.find("PROCEDENCIA").text
        data_atualizacao = especificacoes_tag.find("DATAATUALIZACAO").text
        situacao_chassi = especificacoes_tag.find("SITUACAODOCHASSI").text
        tipo_docto_faturado = especificacoes_tag.find("TIPODOCUMENTOFATURADO").text
        num_docto_faturado = especificacoes_tag.find("DOCUMENTOFATURADO").text
        uf_docto_faturado = especificacoes_tag.find("UFFATURADO").text

        self.motor = utils.to_string(motor)
        self.cambio = utils.to_string(cambio)
        self.passageiros = utils.to_string(passageiros)
        self.potencia = utils.to_string(potencia)
        self.eixos = utils.to_string(eixos)
        self.carga = utils.to_string(carga)
        self.cmt = utils.to_string(cmt)
        self.pbt = utils.to_string(pbt)
        self.num_carroceria = utils.to_string(num_carroceria)
        self.eixo_traseiro = utils.to_string(eixo_traseiro)
        self.terceiro_eixo = utils.to_string(terceiro_eixo)
        self.cilindradas = utils.to_string(cilindradas)
        self.especie = utils.to_string(especie)
        self.categoria = utils.to_string(categoria)
        self.carroceria = utils.to_string(carroceria)
        self.procedencia = utils.to_string(procedencia)
        self.data_atualizacao = utils.to_string(data_atualizacao)
        self.situacao_chassi = utils.to_string(situacao_chassi)
        self.tipo_docto_faturado = utils.to_string(tipo_docto_faturado)
        self.num_docto_faturado = utils.to_string(num_docto_faturado)
        self.uf_docto_faturado = utils.to_string(uf_docto_faturado)

    def to_string(self):
        return f"\nESPECIFICAÇÕES:\n* Motor: {self.motor}\n* Câmbio: {self.cambio}\n* Passageiros: {self.passageiros}\n* Potência: {self.potencia}\n* Eixos: {self.eixos}\n* Carga: {self.carga}\n* CMT: {self.cmt}\n* PBT: {self.pbt}\n* Número Carroceria: {self.num_carroceria}\n* Eixo Traseiro: {self.eixo_traseiro}\n* Terceiro Eixo: {self.terceiro_eixo}\n* Cilindradas: {self.cilindradas}\n* Espécie: {self.especie}\n* Categoria: {self.categoria}\n* Carroceria: {self.carroceria}\n* Procedência: {self.procedencia}\n* Data Atualização: {self.data_atualizacao}\n* Situação Chassi: {self.situacao_chassi}\n* Tipo Documento Faturado: {self.tipo_docto_faturado}\n* Número Documento Faturado: {self.num_docto_faturado}\n* UF Documento Faturado: {self.uf_docto_faturado}"


class Restricoes:
    def __init__(self, restricoes_tag, restricoes_arr):
        situacao_veiculo = restricoes_tag.find("SITUACAO_VEICULO").text
        roubo_furto = restricoes_tag.find("ROUBO_E_FURTO").text

        self.situacao_veiculo = utils.to_string(situacao_veiculo)
        self.roubo_furto = utils.to_string(roubo_furto)
        self.restricoes = restricoes_arr

    def to_string(self):
        string = f"\nRESTRIÇÕES:\n* Situação do Veículo: {self.situacao_veiculo}\n* Roubo/Furto: {self.roubo_furto}\n* Lista de Restrições:"

        if len(self.restricoes) == 0:
            string = string + f"\n  * Nenhuma restrição encontrada"
        else:
            for restricao in self.restricoes:
                string = string + f"\n  * {restricao}"

        return string


class IntencaoFinanciamento:
    def __init__(self, intencao_financiamento_tag):
        nome_financiado = intencao_financiamento_tag.find("NOMEDOFINANCIADO").text
        docto_financiado = intencao_financiamento_tag.find("DOCUMENTOFINANCIADO").text
        restricao_documento = intencao_financiamento_tag.find(
            "RESTRICAODOCUMENTOARRENDATARIO"
        ).text
        data_inclusao = intencao_financiamento_tag.find("DATAINCLUSAO").text
        cod_financeira = intencao_financiamento_tag.find("CODIGOAGENTEFINANCEIRO").text
        nome_financeira = intencao_financiamento_tag.find("AGENTE").text
        restricao_financeira = intencao_financiamento_tag.find(
            "RESTRICAOFINANCEIRA"
        ).text
        num_contrato = intencao_financiamento_tag.find("NCONTRATO").text
        dat_vigencia_contrato = intencao_financiamento_tag.find(
            "DATADAVIGENCIADOCONTRATOFINANCEIRA"
        ).text

        self.nome_financiado = utils.to_string(nome_financiado)
        self.docto_financiado = utils.to_string(docto_financiado)
        self.restricao_documento = utils.to_string(restricao_documento)
        self.data_inclusao = utils.to_date(data_inclusao)
        self.cod_financeira = utils.to_string(cod_financeira)
        self.nome_financeira = utils.to_string(nome_financeira)
        self.restricao_financeira = utils.to_string(restricao_financeira)
        self.num_contrato = utils.to_string(num_contrato)
        self.dat_vigencia_contrato = utils.to_date(dat_vigencia_contrato)

    def to_string(self):
        return f"\nINTENÇÃO DE FINANCIAMENTO:\n* Nome do Financiado: {self.nome_financiado}\n* Documento do Financiado: {self.docto_financiado}\n* Restrição no Documento: {self.restricao_documento}\n* Data de Inclusão: {utils.from_date_to_string(self.data_inclusao)}\n* Código da Financeira: {self.cod_financeira}\n* Nome da Financeira: {self.nome_financeira}\n* Restrição na Financeira: {self.restricao_financeira}\n* Número do Contrato: {self.num_contrato}\n* Data de Vigência do Contrato: {utils.from_date_to_string(self.dat_vigencia_contrato)}"


class Debitos:
    def __init__(self, debitos_tag):
        debitos_ipva = debitos_tag.find("DEBITOSDEIPVA").text
        debitos_licenciamento = debitos_tag.find("DEBITOSDELICENCIAMENTO").text
        debitos_dpvat = debitos_tag.find("DEBITOSDEDPVAT").text
        debitos_multas = debitos_tag.find("DEBITOSDEMULTAS").text
        multas_detran = debitos_tag.find("MULTASDETRAN").text
        multas_cetesb = debitos_tag.find("MULTASCETESB").text
        multas_municipais = debitos_tag.find("MULTASMUNICIPAIS").text
        multas_renainf = debitos_tag.find("MULTASRENAINF").text
        multas_dersa = debitos_tag.find("MULTASDERSA").text
        multas_der = debitos_tag.find("MULTASDER").text
        multas_prf = debitos_tag.find("MULTASPOLICIARODOVIARIAFEDERAL").text
        data_licenciamento = debitos_tag.find("DATALICENCIAMENTO").text
        exercicio_licenciamento = debitos_tag.find("EXERCICIOLICENCIAMENTO").text

        self.debitos_ipva = utils.to_float(debitos_ipva, "BR")
        self.debitos_licenciamento = utils.to_float(debitos_licenciamento, "BR")
        self.debitos_dpvat = utils.to_float(debitos_dpvat, "BR")
        self.debitos_multas = utils.to_float(debitos_multas, "BR")
        self.multas_detran = utils.to_float(multas_detran, "BR")
        self.multas_cetesb = utils.to_float(multas_cetesb, "BR")
        self.multas_municipais = utils.to_float(multas_municipais, "BR")
        self.multas_renainf = utils.to_float(multas_renainf, "BR")
        self.multas_municipais = utils.to_float(multas_municipais, "BR")
        self.multas_dersa = utils.to_float(multas_dersa, "BR")
        self.multas_der = utils.to_float(multas_der, "BR")
        self.multas_prf = utils.to_float(multas_prf, "BR")
        self.data_licenciamento = utils.to_date(data_licenciamento)
        self.exercicio_licenciamento = utils.to_date(exercicio_licenciamento)

    def to_string(self):
        return f"\nDÉBITOS:\n* Débitos de IPVA: {utils.from_float_to_string(self.debitos_ipva, 2)}\n* Débitos de Licenciamento: {utils.from_float_to_string(self.debitos_licenciamento, 2)}\n* Débitos de DPVAT: {utils.from_float_to_string(self.debitos_dpvat, 2)}\n* Débitos de Multas: {utils.from_float_to_string(self.debitos_multas, 2)}\n* Multas DETRAN: {utils.from_float_to_string(self.multas_detran, 2)}\n* Multas CETESB: {utils.from_float_to_string(self.multas_cetesb, 2)}\n* Multas Municipais: {utils.from_float_to_string(self.multas_municipais, 2)}\n* Multas RENAINF: {utils.from_float_to_string(self.multas_renainf, 2)}\n* Multas DERSA: {utils.from_float_to_string(self.multas_dersa, 2)}\n* Multas DER: {utils.from_float_to_string(self.multas_der, 2)}\n* Multas PRF: {utils.from_float_to_string(self.multas_prf, 2)}\n* Data de Licenciamento: {utils.from_date_to_string(self.data_licenciamento)}\n* Exercício do Licenciamento: {utils.from_date_to_string(self.exercicio_licenciamento)}"


class ComunicacaoVenda:
    def __init__(self, comunicacao_venda_tag):
        comunicado = comunicacao_venda_tag.find("COMUNICACAODEVENDAS").text
        data_comunicado = comunicacao_venda_tag.find("DATACOMUNICACAO").text
        data_venda = comunicacao_venda_tag.find("DATADEVENDAS").text

        self.comunicado = utils.to_string(comunicado)
        self.data_comunicado = utils.to_datetime(data_comunicado)
        self.data_venda = utils.to_datetime(data_venda)

    def to_string(self):
        return f"\nCOMUNICAÇÃO DE VENDA:\n* Comunicado: {self.comunicado}\n* Data Comunicado: {utils.from_datetime_to_string(self.data_comunicado)}\n* Data Venda: {utils.from_datetime_to_string(self.data_venda)}"


class Proprietario:
    def __init__(self, proprietario_tag):
        nome = proprietario_tag.find("PROPRIETARIO_ATUAL").text
        documento = proprietario_tag.find("DOCUMENTO").text

        self.nome = utils.to_string(nome)
        self.documento = utils.to_string(documento)

    def to_string(self):
        return f"\nPROPRIETÁRIO:\n* Nome: {self.nome}\n* Documento: {self.documento}"
