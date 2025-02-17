# -*- coding: utf-8 -*-
"""Teste Engenharia - Problema 1.ipynb


Uma loja de perfumes possui uma tabela de notas fiscais (notas_fiscais) que registra os dados básicos de cada venda, como:

*   id_nota: Identificador único da nota fiscal.
*   data: Data de emissão da nota fiscal.
*   id_vendedor: Identificador do vendedor responsável pela venda.


Além disso, há uma tabela de vendedores (vendedores), que contém os seguintes campos:


*   id_vendedor: Identificador único do vendedor.
*   nome: Nome do vendedor.
*   gerente: Nome do gerente associado ao vendedor.
*   data_inicial_gerencia: Data de início da associação do vendedor ao gerente.
*   data_final_gerencia: Data de término da associação do vendedor ao gerente.

Rafaela dona da loja deseja saber a quantidade de vendas por gerente e vendedor. 
Com base nos datafremes abaixo, crie a logica de programação para trazer a analise que Rafaela deseja.
"""

import pandas as pd

# Criando o dataframe de notas fiscais
notas_fiscais = pd.DataFrame({
    "id_nota": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "data": ["2023-12-01", "2023-12-02", "2023-12-03", "2023-12-04", "2023-12-05", "2023-12-06", "2024-01-10", "2024-01-01", "2023-12-31"],
    "id_vendedor": [101, 102, 103, 101, 102, 103, 101, 101, 101]
})

# Convertendo a coluna de data para datetime
notas_fiscais["data"] = pd.to_datetime(notas_fiscais["data"])

# Criando o dataframe de vendedores
vendedores = pd.DataFrame({
    "id_vendedor": [101,101, 102, 103],
    "nome": ["Ana", "Ana" , "Carlos", "Bruno"],
    "gerente": ["Mariana","Marcos", "João", "João"],
    "data_inicial_gerencia": ["2023-01-01","2024-01-01", "2023-01-01", "2023-01-01"],
    "data_final_gerencia": ["2023-12-31","2024-02-01", "2023-12-31", "2023-06-30"]
})

# Convertendo as colunas de data para datetime
vendedores["data_inicial_gerencia"] = pd.to_datetime(vendedores["data_inicial_gerencia"])
vendedores["data_final_gerencia"] = pd.to_datetime(vendedores["data_final_gerencia"])

# Exibindo os dataframes criados
print("Notas Fiscais:")
print(notas_fiscais)
print("\nVendedores:")
print(vendedores)

# --------------------------------------------------------------------------------------------------

# mesclar tabelas
vendas_completas = pd.merge(notas_fiscais, vendedores, on="id_vendedor", how="left")

# filtrando periodos de gerencia válidos
vendas_completas = vendas_completas[
    (vendas_completas["data"] >= vendas_completas["data_inicial_gerencia"]) &
    (vendas_completas["data"] <= vendas_completas["data_final_gerencia"])
]

# quantidade de vendas por vendedor
df_vendedor = vendas_completas.groupby(["nome"]).size().reset_index(name="quantidade_vendas")
print(df_vendedor)

# quantidade de vendas por gerente
df_gerente = vendas_completas.groupby(["gerente"]).size().reset_index(name="quantidade_vendas")
print(df_gerente)

