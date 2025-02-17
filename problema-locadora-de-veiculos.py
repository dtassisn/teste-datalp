# -*- coding: utf-8 -*-
"""
Desafio – Manutenção para Locadora de Veículos

Uma locadora de veículos possui uma base de dados que registra, diariamente, o status de cada veículo. 
Os status possíveis são:
•	Alugado – Veículo atualmente alugado por um cliente.
•	Em manutenção – Veículo que está indisponível devido a manutenção.
•	Em estoque – Veículo disponível na loja para aluguel.

Com base no excel disponivel ("Veiculos em manutenção.xlsx") apresente as seguintes informações:

• Dos veículos que estão em manutenção hoje ( considere hoje como 30/01/2025). A quanto tempo ele está em manutenção?
• Dos últimos 3 meses  considere hoje como 30/01/2025) , quantos dias o veiculo ficou em manutenção?
• Quantidade de manutenções por veiculo, cada sequencia de dias em manutenção, é considerada 1 manuteção.
• Total de dias alocado por veiculo
• Veiculo que ficou mais tempo em estoque e a quantidade de dias
"""
# import bibliotecas e funções
import pandas as pd
from datetime import timedelta, datetime

# caminho do arquivo local
caminho = r'veiculos_em_manutencao.xlsx'

# montando dataframe
df = pd.read_excel(caminho, sheet_name=0)

# variável para armazenar o dia atual
data_hoje = datetime(2025, 1, 30)
data_inicio = data_hoje - timedelta(days=90)

print(data_inicio)

# conterter colunas
df["DATA"] = pd.to_datetime(df["DATA"])
df["EQUIPAMENTO"] = df["EQUIPAMENTO"].astype(str)

## Veículos em manutenção hoje (30/01/2025) e quantidade de dias em manutenção ---------------------------------------------------------

# dataframe com veículos em manutenção hoje
df_manutencao_hoje = df.query("DATA == @data_hoje and STATUS == 'EM MANUTENÇÃO'")
df_inicio_manutencao = df.query("STATUS != 'EM MANUTENÇÃO'").groupby("EQUIPAMENTO").agg(DATA_INICIO_MANUTENCAO=("DATA", "max")).reset_index()

# merge das tabelas
df_manutencao_hoje = df_manutencao_hoje.merge(df_inicio_manutencao[["EQUIPAMENTO", "DATA_INICIO_MANUTENCAO"]], on="EQUIPAMENTO", how="left")

# adição da coluna que conta a diferença de dias desde a ultima data 'não manutenção' até o dia de hoje (30/01/2025)
df_manutencao_hoje["DIAS_EM_MANUTENCAO"] = (data_hoje - df_manutencao_hoje["DATA_INICIO_MANUTENCAO"]).dt.days
print(df_manutencao_hoje)

## Quantidade de dias em manutenção nos últimos 3 meses -----------------------------------------------------

df_ultimos_3_meses = df.query("DATA >= @data_inicio and DATA <= @data_hoje and STATUS == 'EM MANUTENÇÃO'")

df_dias_manutencao = df_ultimos_3_meses.groupby(["EQUIPAMENTO", "MODELO", "ANO"]).agg(DIAS_EM_MANUTENCAO=("DATA", "count")).reset_index()
print(df_dias_manutencao)

## Quantidades de manutenções distintas ------------------------------------------------------------------------------------------

# quantidade de manutenções realizadas por veículo
df = df.sort_values(by=["EQUIPAMENTO", "DATA"])

# troca de status
df["STATUS_ANTERIOR"] = df.groupby("EQUIPAMENTO")["STATUS"].shift(1)

# flag
df["NOVA_MANUTENCAO"] = (df["STATUS"] == "EM MANUTENÇÃO") & (df["STATUS_ANTERIOR"] != "EM MANUTENÇÃO")

# quantidade de vezes que o veiculo entrou em manutenção
df_qtd_manutencoes = df.groupby(["EQUIPAMENTO", "MODELO", "ANO"]).agg(QUANTIDADE_MANUTENCOES=("NOVA_MANUTENCAO", "sum")).reset_index()
print(df_qtd_manutencoes)

## Quantidades de dias alocado  ------------------------------------------------------------------------------------------

df_dias_alocados = df.query("STATUS == 'ALUGADO'").groupby("EQUIPAMENTO").agg(DIAS_ALUGADO=("DATA", "count")).reset_index()
print(df_dias_alocados)

## Veiculo que ficou mais tempo em estoque e a quantidade de dias  ------------------------------------------------------------------------------------------

df_dias_estoque = df.query("STATUS == 'EM ESTOQUE'").groupby(["EQUIPAMENTO", "MODELO", "ANO"]).agg(DIAS_EM_ESTOQUE=("DATA", "count")).reset_index()

resultado = df_dias_estoque.nlargest(1, 'DIAS_EM_ESTOQUE')
print(resultado)

