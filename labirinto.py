import random
import os
import time

def gerar_labirinto(linhas, colunas):
    labirinto = []
    for i in range(linhas):
        linha_atual = []
        for j in range(colunas):
            linha_atual.append(1)
        labirinto.append(linha_atual)

    def gerar_caminho(linha, col):
        labirinto[linha][col] = 0
        direcoes = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(direcoes)

        for direcao in direcoes:
            dl = direcao[0]
            dc = direcao[1]

            nova_linha = linha + dl
            nova_col = col + dc

            dentro_do_labirinto = (nova_linha >= 0 and nova_linha < linhas and nova_col >= 0 and nova_col < colunas)

            if dentro_do_labirinto:
                if labirinto[nova_linha][nova_col] == 1:
                    parede_linha = linha + dl // 2
                    parede_col = col + dc // 2
                    labirinto[parede_linha][parede_col] = 0
                    gerar_caminho(nova_linha, nova_col)

    gerar_caminho(1, 1)

    labirinto[1][0] = 0
    labirinto[linhas - 2][colunas - 1] = 0
    
    return labirinto

def limpar_tela():
    os.system('clear')

def desenhar_labirinto(labirinto, pos_jogador):
    linhas = len(labirinto)
    colunas = len(labirinto[0])
    
    for i in range(linhas):
        linha_texto = ""
        for j in range(colunas):
            if i == pos_jogador[0] and j == pos_jogador[1]:
                linha_texto = linha_texto + " @ "
            elif i == 1 and j == 0:
                linha_texto = linha_texto + " E "
            elif i == linhas -2 and j == colunas - 1:
                linha_texto = linha_texto + " S "
            elif labirinto[i][j] == 1:
                linha_texto = linha_texto + "###"
            else:
                linha_texto = linha_texto + "   "
        
        print(linha_texto)

def mover_jogador(labirinto, pos_jogador, direcao):
    if direcao not in ["w", "s", "a", "d"]:
        return False
    
    linha_atual = pos_jogador[0]
    col_atual = pos_jogador[1]

    if direcao == "w":
        nova_linha = linha_atual - 1
        nova_col = col_atual
    elif direcao == "s":
        nova_linha = linha_atual + 1
        nova_col = col_atual
    elif direcao == "a":
        nova_linha = linha_atual
        nova_col = col_atual -1
    elif direcao == "d": 
        nova_linha = linha_atual
        nova_col = col_atual + 1

    linhas = len(labirinto)
    colunas = len(labirinto[0])

    dentro_do_labirinto = (nova_linha >= 0 and nova_linha < linhas and nova_col >= 0 and nova_col < colunas)

    if dentro_do_labirinto:
        if labirinto[nova_linha][nova_col] != 1:
            pos_jogador[0] = nova_linha
            pos_jogador[1] = nova_col
            return True
        
    return False

def verificar_vitoria(labirinto, pos_jogador):
    linha_saida = len(labirinto) - 2
    col_saida = len(labirinto[0]) - 1

    if pos_jogador[0] == linha_saida and pos_jogador[1] == col_saida:
        return True
    return False

def jogar(nome_jogador):
    labirinto = gerar_labirinto(11, 21)
    pos_jogador = [1, 1]
    movimentos = 0
    tempo_inicio = time.time()

    while True:
        limpar_tela()

        tempo_atual = time.time()
        tempo_passado = int(tempo_atual - tempo_inicio)
        print(f"Jogador: {nome_jogador}  |  Movimentos: {movimentos}  |  Tempo: {tempo_passado}s")
        print("Use w (cima), A (esquerda), S (baixo), D (direita) para se mover.")
        print()

        desenhar_labirinto(labirinto, pos_jogador)
        print()

        if verificar_vitoria(labirinto, pos_jogador):
            print("Você chegou na saída!!!")
            tempo_total = int(time.time() - tempo_inicio)
            return movimentos, tempo_total
        
        comando = input("Movimento: ").strip().lower()

        movimento_valido = mover_jogador(labirinto, pos_jogador, comando)

        if movimento_valido:
            movimentos = movimentos + 1
        else:
            print("Movimento inválido! Pressione Enter para continuar.")
            input()

def calcular_pontuacao(movimentos, tempo):
    pontuacao = 1000 - movimentos - tempo

    if pontuacao < 0:
        pontuacao = 0

    return pontuacao

def salvar_pontuacao(nome, pontuacao, movimentos, tempo):
    arquivo = open("ranking.txt", "a")
    linha = nome + "," + str(pontuacao) + "," + str(movimentos) + "," + str(tempo) + "\n"
    arquivo.write(linha)
    arquivo.close()

def carregar_ranking():
    try:
        arquivo = open("ranking.txt", "r")
        linhas = arquivo.readlines()
        arquivo.close()
    except FileNotFoundError:
        return []
    
    ranking = []

    for linha in linhas:
        linha = linha.strip()
        partes = linha.split(",")

        if len (partes) == 4:
            nome = partes[0]
            pontuacao = int(partes[1])
            movimentos = int(partes[2])
            tempo = int(partes[3])

            jogador = [nome, pontuacao, movimentos, tempo]
            ranking.append(jogador)
    
    for i in range(len(ranking)):
        for j in range(i + 1, len(ranking)):
            if ranking[j][1] > ranking[i][1]:
                temporario =ranking[i]
                ranking[i] = ranking[j]
                ranking[j] = temporario

    return ranking

def exibir_ranking():
    limpar_tela()
    ranking = carregar_ranking()

    print("=" * 45)
    print("RANKING DE JOGADORES")
    print("=" * 45)

    if len(ranking) == 0:
        print("Nenhuma pontuação salva ainda.")
    else:
        print(f"{'Pos':<5} {'Nome':<15} {'Pontuação':<10} {'Movimentos':<12} {'Tempo'}")
        print("-" * 55)

        posicao = 1
        for jogador in ranking:
            nome = jogador[0]
            pontuacao = jogador[1]
            movimentos = jogador[2]
            tempo = jogador[3]

            print(f"{posicao:<5} {nome:<15} {pontuacao:<10} {movimentos:<12} {tempo}s")
            posicao = posicao + 1

        print("=" * 45)

def exibir_menu(nome_jogador):
    limpar_tela()
    print("=" * 40)
    print("          JOGO DE LABIRINTO")
    print("=" * 40)
    print(f"  Jogador: {nome_jogador}")
    print()
    print("  1 - Jogar")
    print("  2 - Ver Ranking")
    print("  3 - Sair")
    print("=" * 40)

def main():
    limpar_tela()
    print("=" * 40)
    print("     Bem-vindo ao Labirinto...")
    print("=" * 40)
    print()
    nome_jogador = input("Qual seu nome?: ").strip()

    if nome_jogador == "":
        nome_jogador = "Anônimo"

    while True:
        exibir_menu(nome_jogador)
        opcao = input("O que deseja fazer?: ").strip()

        if opcao == "1":
            movimentos, tempo = jogar(nome_jogador)
            pontuacao = calcular_pontuacao(movimentos, tempo)
            salvar_pontuacao(nome_jogador, pontuacao, movimentos, tempo)
            print(f"Sua pontuação: {pontuacao}. Pressione Enter para continuar.")
            input()
        elif opcao == "2":
            exibir_ranking()
            input("Pressione Enter para voltar ao menu.")
        elif opcao == "3":
            limpar_tela()
            print("Até mais...")
            break
        else:
            print("Opção inválida... Pressione Enter para continuar")
            input()

main()