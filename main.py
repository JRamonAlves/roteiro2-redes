def xor_bits(a: str, b: str) -> str:
    """
    Realiza a operação de XOR bit a bit entre duas strings binárias de mesmo
    comprimento.
    """
    resultado = ""
    # Garante que as strings tenham o mesmo comprimento
    assert len(a) == len(b)
    for i in range(len(a)):
        if a[i] == b[i]:
            resultado += '0'
        else:
            resultado += '1'
    return resultado


def calcular_crc_manual(dados_bits: str, gerador_bits: str) -> str:
    """
    Calcula o CRC para uma sequência de dados M(x) usando um gerador G(x),
    simulando a divisão polinomial com operações bit a bit.

    Args:
        dados_bits: A string binária representando o polinômio da mensagem, M(x).
        gerador_bits: A string binária representando o polinômio gerador, G(x).

    Returns:
        A string binária de r bits representando o CRC (o resto da divisão).
    """
    # 1. Obtenha o grau 'r' do gerador.
    #    Lembre-se que um gerador de n bits representa um polinômio de grau n-1.
    n = len(gerador_bits)
    r = n - 1

    # 2. Crie T(x) = M(x) * x^r, que é a mensagem com 'r' zeros anexados.
    #    Usamos uma lista de caracteres para que possamos modificar os bits.
    mensagem_aumentada = list(dados_bits + '0' * r)

    # 3. Implemente o loop de divisão.
    #    Percorra os bits da mensagem original (em uma janela), da esquerda para a direita.
    #    O loop vai até o último bit da mensagem original.
    for i in range(len(dados_bits)):
        # Se o bit mais significativo da 'janela' atual for '1', realize o XOR.
        # Este bit é mensagem_aumentada[i].
        if mensagem_aumentada[i] == '1':
            # A 'janela_atual' são os próximos 'n' bits (tamanho do gerador)
            # começando da posição 'i'.
            janela_atual = "".join(mensagem_aumentada[i: i + n])

            # Realiza o XOR entre a janela e o gerador.
            resultado_xor = xor_bits(janela_atual, gerador_bits)

            # Atualize a mensagem com o resultado do XOR.
            # O resultado do XOR substitui a janela na mensagem aumentada.
            for j in range(n):
                mensagem_aumentada[i + j] = resultado_xor[j]

    # 4. O resto da divisão são os 'r' bits finais da mensagem processada.
    resto = "".join(mensagem_aumentada[-r:])
    return resto

# --- Exemplo de Uso ---


def main():
    dados_teste = "1101011111"  # M(x)
    gerador_teste = "10011"    # G(x), representa x^4 + x + 1

# Calcular o CRC com os dados de teste
    crc_calculado = calcular_crc_manual(dados_teste, gerador_teste)

    print("--- Validação do Algoritmo CRC ---")
    print(f"Dados M(x):    {dados_teste}")
    print(f"Gerador G(x):  {gerador_teste}")
    print(f"CRC Calculado: {crc_calculado}")

# O quadro T(x) a ser transmitido é a mensagem original concatenada com o CRC
    quadro_transmitido = dados_teste + crc_calculado
    print(f"Quadro T(x):   {quadro_transmitido}")


if __name__ == "__main__":
    main()
