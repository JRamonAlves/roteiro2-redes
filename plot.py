import time
import os
from crc import Calculator, Crc16
import matplotlib.pyplot as plt
from main import calcular_crc_manual

gerador_modbus = "11000000000000101"
calculator_lib = Calculator(Crc16.MODBUS)

tamanhos_bytes = [1500, 3000, 4500, 6000, 9000]
resultados = []

for tamanho in tamanhos_bytes:
    print(f"Analisando para mensagem de {tamanho} bytes...")

    mensagem_bytes = os.urandom(tamanho)
    mensagem_bits = "".join(format(byte, '08b') for byte in mensagem_bytes)

    start_time = time.perf_counter()
    crc_manual = calcular_crc_manual(mensagem_bits, gerador_modbus)
    end_time = time.perf_counter()

    tempo_manual = end_time - start_time

    start_time = time.perf_counter()
    crc_lib = calculator_lib.checksum(mensagem_bytes)
    end_time = time.perf_counter()

    tempo_lib = end_time - start_time

    resultados.append({
        "tamanho": tamanho,
        "tempo_manual": tempo_manual,
        "tempo_lib": tempo_lib,
    })

print()
print("--- Resultados Finais (Dados Brutos) ---")
for res in resultados:
    print(res)

tamanhos = [r['tamanho'] for r in resultados]
tempos_manual = [r['tempo_manual'] for r in resultados]
tempos_lib = [r['tempo_lib'] for r in resultados]

plt.figure(figsize=(10, 6))
plt.plot(tamanhos, tempos_manual, 'r-o',
         label='Implementação Manual (Python Puro)')
plt.plot(tamanhos, tempos_lib, 'b-s', label='Biblioteca Otimizada (crc)')
plt.title('Comparativo de Tempo de Execução: Manual vs. Biblioteca')
plt.xlabel('Tamanho da Mensagem (bytes)')
plt.ylabel('Tempo de Execução (segundos)')
plt.legend()
plt.grid(True)
plt.show()
