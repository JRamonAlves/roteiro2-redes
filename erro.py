from main import calcular_crc_manual, xor_bits
import random
from crc import Calculator, Crc16, Configuration


def str_to_bits(s: str) -> str:
    """Converte uma string de texto para uma string de bits (UTF-8)."""
    return "".join(format(byte, '08b') for byte in s.encode('utf-8'))


def bits_to_bytes(s: str) -> bytes:
    """Converte uma string de bits para bytes."""
    s_padded = s + '0' * ((8 - len(s) % 8) % 8)
    return int(s_padded, 2).to_bytes(len(s_padded) // 8, byteorder='big')


NOME_COMPLETO = "José Ramon Severo Alves"
GERADOR_BITS = "10001000000100001"

MENSAGEM_BASE = str_to_bits(NOME_COMPLETO)
CRC_ORIGINAL = calcular_crc_manual(MENSAGEM_BASE + '0' * 16, GERADOR_BITS)
QUADRO_TRANSMITIDO = MENSAGEM_BASE + CRC_ORIGINAL

print("--- Cenário Personalizado Definido ---")
print(f"Nome: {NOME_COMPLETO}")
print(f"Matrícula Final: 3 -> Gerador: CRC-16/ARC ({GERADOR_BITS})")
print(f"Mensagem Base (bits): {MENSAGEM_BASE[:64]}...")
print(f"CRC da Mensagem Base: {CRC_ORIGINAL}")
print(f"Quadro a ser Transmitido: {QUADRO_TRANSMITIDO[:64]}...")
print("-" * 30)

# --- 4.2: A Caça aos Erros ---
# Preparar a calculadora da biblioteca para verificação
# Crc16.ARC é o identificador para CRC-16/ARC na biblioteca
config_justa = Configuration(
    width=16,
    polynomial=0x1021,
    init_value=0x0000,
    final_xor_value=0x0000,
    reverse_input=False,
    reverse_output=False,
)
calculator_lib = Calculator(config_justa)
resultados_testes = []
NUM_TESTES = 10

teste_cego = random.randint(1, NUM_TESTES)

for i in range(1, NUM_TESTES + 1):
    print(f"--- Teste #{i} ---")

    if i == teste_cego:
        erro_pattern = GERADOR_BITS
        print("Inserindo erro de 'Ponto Cego' (padrão do gerador)...")
    else:
        tamanho_rajada = random.randint(2, 16)
        erro_pattern = ''.join(random.choice('10')
                               for _ in range(tamanho_rajada))
        if '1' not in erro_pattern:
            erro_pattern = '1'

    pos_max = len(QUADRO_TRANSMITIDO) - len(erro_pattern)
    pos_erro = random.randint(0, pos_max)

    erro_mascara = '0' * pos_erro + erro_pattern + '0' * \
        (len(QUADRO_TRANSMITIDO) - pos_erro - len(erro_pattern))

    QUADRO_CORROMPIDO = xor_bits(QUADRO_TRANSMITIDO, erro_mascara)

    resto_manual = calcular_crc_manual(QUADRO_CORROMPIDO, GERADOR_BITS)
    detectado_manual = int(resto_manual, 2) != 0

    dados_corrompidos_bits = QUADRO_CORROMPIDO[:-16]
    crc_corrompido_bits = QUADRO_CORROMPIDO[-16:]

    dados_corrompidos_bytes = bits_to_bytes(dados_corrompidos_bits)
    crc_corrompido_int = int(crc_corrompido_bits, 2)

    is_valid = calculator_lib.verify(
        dados_corrompidos_bytes, crc_corrompido_int)
    detectado_lib = not is_valid

    print(f"Padrão de erro: {erro_pattern} (Tamanho: {len(erro_pattern)})")
    print(f"Posição do erro: {pos_erro}")
    print(f"CRC Manual Resultante: {
          resto_manual} -> Detectado: {detectado_manual}")
    print(f"Verificação Biblioteca -> Detectado: {detectado_lib}")
    print("-" * 20 + "\n")

    resultados_testes.append({
        "teste_n": i, "erro": erro_pattern, "posicao": pos_erro,
        "detectado_manual": detectado_manual, "detectado_lib": detectado_lib
    })

# --- Relatório Final ---
print("\n--- Relatório Final da Caça aos Erros ---")
for res in resultados_testes:
    status = "DETECTADO"
    if not res['detectado_manual']:
        status = "FALHA NA DETECÇÃO (PONTO CEGO)!"
    print(f"Teste #{res['teste_n']}: Padrão='{res['erro']
                                              }', Posição={res['posicao']} -> Status: {status}")
