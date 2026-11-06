import random
import os
import json
import time
from datetime import datetime

# 1. Parâmetros fixos do sistema
setpoint_temperatura = 30.0  # Temperatura desejada (°C)
setpoint_ph = 7 # pH desejado para o crescimento bacteriano 
setpoint_carbono = 550 #mg/L de Glicerol ou Glicose
setpoint_nitrogenio = 1250 #mg/L NH4-+
setpoint_fosforo = 3000 #mg/L de fosfatos
setpoint_magnesio = 300 #mg/L Mg-2+
setpoint_calcio = 30 #mg/L Ca-2+
setpoint_ferro = 8 #mg/L Fe-2+/Fe-3+
setpoint_zinco = 3 #mg/L Zn-2+
setpoint_manganes = 2 #mg/L Mn-2+
setpoint_cobre = 0.5 #mg/L Cu-2+
setpoint_molibdenio = 0.5 #mg/L Mo-2+
intervalo_leitura = 10  # segundos
tempo_total = 120  # 2 minutos em segundos

# 2. Variaveis com intervalo inicial de inóculo (inicio do funcionamento do controle automático do biorreator)
temperatura_atual = random.randint(15, 35)
ph_atual = random.randint(6, 8)
carbono_atual = random.randint(500, 600)
nitrogenio_atual = random.randint(1200, 1300)
fosforo_atual = random.randint(2900, 3100)
magnesio_atual = random.randint(250, 350)
calcio_atual = random.randint(25, 35)
ferro_atual = random.randint(5, 10)
zinco_atual = random.randint(2, 4)
manganes_atual = random.randint(1, 3)
cobre_atual = random.uniform(0.3, 0.7) # Usando uniform para gerar decimais (float)
molibdenio_atual = random.uniform(0.3, 0.7)

# Lista para armazenar o histórico
historico_biorreator = []

print(f"Temperatura Inicial Sorteada: {temperatura_atual:.2f} °C")
print(f"pH Inicial Sorteado: {ph_atual:.2f}")
print(f"Carbono Inicial Sorteado: {carbono_atual:.2f} mg/L")
print(f"Nitrogênio Inicial Sorteado: {nitrogenio_atual:.2f} mg/L")
print(f"Fósforo Inicial Sorteado: {fosforo_atual:.2f} mg/L")
print(f"Magnésio Inicial Sorteado: {magnesio_atual:.2f} mg/L")
print(f"Cálcio Inicial Sorteado: {calcio_atual:.2f} mg/L")
print(f"Ferro Inicial Sorteado: {ferro_atual:.2f} mg/L")
print(f"Zinco Inicial Sorteado: {zinco_atual:.2f} mg/L")
print(f"Manganês Inicial Sorteado: {manganes_atual:.2f} mg/L")
print(f"Cobre Inicial Sorteado: {cobre_atual:.2f} mg/L")
print(f"Molibdênio Inicial Sorteado: {molibdenio_atual:.2f} mg/L\n")

# Calculamos quantos ciclos vão rodar (120 / 10 = 12 ciclos)
total_ciclos = tempo_total // intervalo_leitura

# Loop de controle
for ciclo in range(1, total_ciclos + 1):
    # Pega data e hora atual do ciclo
    agora = datetime.now()
    data_str = agora.strftime("%Y-%m-%d")
    hora_str = agora.strftime("%H:%M:%S")

    # Adiciona um erro de variação aleatório e aceitável no sensor de temperatura
    erro_sensor_temperatura = random.uniform(-0.5, 0.5)
    temperatura_com_erro = temperatura_atual + erro_sensor_temperatura

    # Ruído aleatório de leitura do eletrodo de pH (+- 0.05)
    erro_sensor_ph = random.uniform(-0.05, 0.05)
    ph_com_erro = ph_atual + erro_sensor_ph

    print(f"Número de ciclos: {ciclo}/{total_ciclos} | Horário: {hora_str} | Temp. Lida: {temperatura_com_erro:.2f} °C | pH Lido: {ph_com_erro:.2f}")

    # =========================================================================
    # Lógica de controle do Biorreator (Atuadores: Resfriador / Aquecedor)
    # =========================================================================
    if temperatura_com_erro > setpoint_temperatura:
        print("  -> Status: Temperatura alta.\nLIGANDO O RESFRIADOR")
        temperatura_atual -= random.uniform(0, 1)  # Resfria aleatóriamente
    elif temperatura_com_erro < setpoint_temperatura:
        print("  -> Status: Temperatura baixa.\nDESLIGANDO RESFRIADOR")
        temperatura_atual += random.uniform(0, 1)  # Aquece 1°C por ciclo
    else:
        print("  -> Status: Temperatura adequada. Sistema estabilizado.")

    # =========================================================================
    # Lógica de controle do Biorreator (Atuadores: Bombas de pH)
    # =========================================================================
    if ph_com_erro > setpoint_ph:
        print("  -> Status: Meio alcalino.\nINJETANDO 1 mL DE HCl")
        ph_atual -= random.uniform(0, 0.5)  # Abaixa aleatoriamente o pH
    elif ph_com_erro < setpoint_ph:
        print("  -> Status: Meio ácido.\nINJETANDO 1 mL DE NaOH")
        ph_atual += random.uniform(0, 0.5)  # Sobe o pH
    else:
        print("  -> Status: pH adequado. Sistema estabilizado.")

    # =========================================================================
    # Lógica de controle do Biorreator (Atuadores: Bombas de Nutrientes)
    # =========================================================================
    # 1. Simulação de leitura dos sensores on-line com pequenos ruídos
    carbono_com_erro = carbono_atual + random.uniform(-5, 5)
    nitrogenio_com_erro = nitrogenio_atual + random.uniform(-10, 10)
    fosforo_com_erro = fosforo_atual + random.uniform(-20, 20)
    magnesio_com_erro = magnesio_atual + random.uniform(-2, 2)
    calcio_com_erro = calcio_atual + random.uniform(-1, 1)
    ferro_com_erro = ferro_atual + random.uniform(-0.5, 0.5)
    zinco_com_erro = zinco_atual + random.uniform(-0.2, 0.2)
    manganes_com_erro = manganes_atual + random.uniform(-0.1, 0.1)
    cobre_com_erro = cobre_atual + random.uniform(-0.05, 0.05)
    molibdenio_com_erro = molibdenio_atual + random.uniform(-0.05, 0.05)

    nutrientes_injetados = []

    # 2. Lógica de Consumo Celular e Reposição (Fed-Batch)
    # Carbono
    if carbono_com_erro < setpoint_carbono:
        carbono_atual += random.uniform(10, 20) # Injeta via bomba
        nutrientes_injetados.append("Carbono")
    else:
        carbono_atual -= random.uniform(2, 10)  # Consumido naturalmente pelas bactérias

    # Nitrogênio
    if nitrogenio_com_erro < setpoint_nitrogenio:
        nitrogenio_atual += random.uniform(20, 40)
        nutrientes_injetados.append("Nitrogênio")
    else:
        nitrogenio_atual -= random.uniform(5, 20)

    # Fósforo
    if fosforo_com_erro < setpoint_fosforo:
        fosforo_atual += random.uniform(50, 100)
        nutrientes_injetados.append("Fósforo")
    else:
        fosforo_atual -= random.uniform(10, 50)

    # Magnésio
    if magnesio_com_erro < setpoint_magnesio:
        magnesio_atual += random.uniform(5, 10)
        nutrientes_injetados.append("Magnésio")
    else:
        magnesio_atual -= random.uniform(1, 5)

    # Cálcio
    if calcio_com_erro < setpoint_calcio:
        calcio_atual += random.uniform(1, 3)
        nutrientes_injetados.append("Cálcio")
    else:
        calcio_atual -= random.uniform(0.2, 1)

    # Ferro
    if ferro_com_erro < setpoint_ferro:
        ferro_atual += random.uniform(0.5, 1.5)
        nutrientes_injetados.append("Ferro")
    else:
        ferro_atual -= random.uniform(0.1, 0.5)

    # Zinco
    if zinco_com_erro < setpoint_zinco:
        zinco_atual += random.uniform(0.2, 0.6)
        nutrientes_injetados.append("Zinco")
    else:
        zinco_atual -= random.uniform(0.05, 0.2)

    # Manganês
    if manganes_com_erro < setpoint_manganes:
        manganes_atual += random.uniform(0.1, 0.3)
        nutrientes_injetados.append("Manganês")
    else:
        manganes_atual -= random.uniform(0.02, 0.1)

    # Cobre
    if cobre_com_erro < setpoint_cobre:
        cobre_atual += random.uniform(0.05, 0.1)
        nutrientes_injetados.append("Cobre")
    else:
        cobre_atual -= random.uniform(0.01, 0.05)

    # Molibdênio
    if molibdenio_com_erro < setpoint_molibdenio:
        molibdenio_atual += random.uniform(0.05, 0.1)
        nutrientes_injetados.append("Molibdênio")
    else:
        molibdenio_atual -= random.uniform(0.01, 0.05)

    # 3. Print de status dos nutrientes consolidados (Para não poluir o terminal)
    if nutrientes_injetados:
        print(f"  -> Status Nutricional: INJETANDO {', '.join(nutrientes_injetados)}\n")
    else:
        print("  -> Status Nutricional: Níveis adequados. Consumo celular ocorrendo normalmente.\n")

    # =========================================================================
    # Salvar dados no histórico
    # =========================================================================
    dados_ciclo = {
        "data": data_str,
        "hora": hora_str,
        "leituras": {
            "temperatura_C": round(temperatura_com_erro, 2),
            "pH": round(ph_com_erro, 2),
            "carbono_mg_L": round(carbono_com_erro, 2),
            "nitrogenio_mg_L": round(nitrogenio_com_erro, 2),
            "fosforo_mg_L": round(fosforo_com_erro, 2),
            "magnesio_mg_L": round(magnesio_com_erro, 2),
            "calcio_mg_L": round(calcio_com_erro, 2),
            "ferro_mg_L": round(ferro_com_erro, 2),
            "zinco_mg_L": round(zinco_com_erro, 2),
            "manganes_mg_L": round(manganes_com_erro, 2),
            "cobre_mg_L": round(cobre_com_erro, 2),
            "molibdenio_mg_L": round(molibdenio_com_erro, 2)
        }
    }
    historico_biorreator.append(dados_ciclo)


# =========================================================================
# Geração do Arquivo JSON
# =========================================================================
nome_arquivo = 'registros_biorreator.json'

if not os.path.exists(nome_arquivo):
    print(f"Criando arquivo {nome_arquivo}")
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(historico_biorreator, arquivo, indent=4, ensure_ascii=False)
else:
    print(f"Sobreescrevendo dados do arquivo {nome_arquivo}")
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(historico_biorreator, arquivo, indent=4, ensure_ascii=False)
    
# Exibe a lista final
print("Leitura finalizada! O arquivo JSON foi gerado com sucesso com todos os parâmetros.")