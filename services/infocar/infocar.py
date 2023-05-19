import extrato
import base_estadual
import codificador_fipe

response = extrato.request_extrato()
response.to_string()

response = base_estadual.request_by_placa("AEF9041")
response.to_string()

response = codificador_fipe.request_by_placa("AEF9041")
response.to_string()
