import base_estadual
import codificador_fipe

print("Base Estadual")
response = base_estadual.request_by_placa("AAA1111")
print(response)

print("Codificador FIPE")
response = codificador_fipe.request_by_placa("AAA1111")
print(response)
