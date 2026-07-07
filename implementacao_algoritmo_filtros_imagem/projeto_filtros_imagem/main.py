"""
Programa Principal
-------------------
Integra as classes Imagem, Download e os Filtros, exibindo um menu
interativo no terminal com as opções:

1. Informar o caminho da imagem (local ou URL)
2. Escolher o filtro a ser aplicado
3. Listar arquivos de imagens do diretório corrente
4. Sair

Para executar:
    python main.py
"""

import os
import logging
from datetime import datetime
from PIL import UnidentifiedImageError

from models.imagem import Imagem, ExtensaoInvalidaError
from models.download import Download, DownloadError
from filtros import FILTROS_DISPONIVEIS

EXTENSOES_IMAGEM = (".jpg", ".jpeg", ".png")
PASTA_IMAGENS_FILTRADAS = "imagens_filtradas"
PASTA_REPOSITORIO_FOTOS = "repositorio_de_fotos"
ARQUIVO_LOG_ERROS = "erros.log"



def limpar_tela():
    """Limpa a tela do terminal, dependendo do sistema operacional."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar(mensagem="Pressione Enter para continuar..."):
    """Pausa a execução até que o usuário pressione Enter."""
    input(mensagem)


class Principal:
    def __init__(self):
        self.imagem_atual: Imagem | None = None
        # Garante que a pasta de saída exista antes de qualquer filtro ser aplicado
        os.makedirs(PASTA_IMAGENS_FILTRADAS, exist_ok=True)

    def informar_caminho_imagem(self):
        limpar_tela()
        print("=" * 55)
        print("        INFORMAR O CAMINHO DA IMAGEM")
        print("=" * 55)
        entrada = input(
            "Informe o caminho local da imagem ou a URL pública "
            "(.jpg/.png): "
        ).strip()

        if not entrada:
            print("\nNenhum caminho informado. Nada foi alterado.\n")
            pausar()
            return

        try:
            if Download.eh_url(entrada):
                print("\nDetectada URL. Baixando imagem...")
                os.makedirs(PASTA_REPOSITORIO_FOTOS, exist_ok=True)
                download = Download(diretorio_destino=PASTA_REPOSITORIO_FOTOS)
                caminho_local = download.baixar(entrada)
                print(f"Imagem baixada e salva em: {caminho_local}")
            else:
                caminho_local = entrada

            imagem = Imagem(caminho_local)
            imagem.carregar()  # valida se o arquivo realmente abre como imagem
            self.imagem_atual = imagem
            print(f"\nImagem carregada com sucesso: {imagem.nome}\n")

        except ExtensaoInvalidaError as erro:
            self._registrar_erro(
                "leitura da imagem", erro,
                "o arquivo informado não tem extensão .jpg, .jpeg ou .png.",
            )
        except FileNotFoundError as erro:
            self._registrar_erro(
                "leitura da imagem", erro,
                "o caminho informado não existe no computador. Verifique se "
                "digitou o caminho corretamente.",
            )
        except UnidentifiedImageError as erro:
            self._registrar_erro(
                "leitura da imagem", erro,
                "o arquivo existe, mas não é uma imagem válida (pode estar "
                "corrompido ou não ser realmente um .jpg/.png).",
            )
        except DownloadError as erro:
            self._registrar_erro(
                "download da imagem", erro,
                "a URL pode estar incorreta, fora do ar, sem conexão com a "
                "internet, ou não apontar para uma imagem .jpg/.png.",
            )
        except Exception as erro:  # rede de segurança para qualquer imprevisto
            self._registrar_erro(
                "leitura/download da imagem", erro,
                "erro inesperado; verifique o caminho/URL informado.",
            )

        pausar()

    def escolher_filtro(self):
        limpar_tela()
        print("=" * 55)
        print("        ESCOLHER O FILTRO A SER APLICADO")
        print("=" * 55)

        if self.imagem_atual is None:
            print("Nenhuma imagem foi carregada ainda. Use a opção 1 primeiro.\n")
            pausar()
            return

        print(f"Imagem atual: {self.imagem_atual.nome}\n")
        print("Filtros disponíveis:")
        for chave, (nome_filtro, _classe, _sufixo) in FILTROS_DISPONIVEIS.items():
            print(f"  {chave}. {nome_filtro}")

        escolha = input("\nEscolha o número do filtro desejado: ").strip()

        if escolha not in FILTROS_DISPONIVEIS:
            print(
                f"\nOpção de filtro inválida: '{escolha}'. "
                f"Escolha um número entre 1 e {len(FILTROS_DISPONIVEIS)}.\n"
            )
            pausar()
            return

        nome_filtro, classe_filtro, sufixo = FILTROS_DISPONIVEIS[escolha]

        try:
            imagem_original = self.imagem_atual.carregar()
            filtro = classe_filtro()
            imagem_filtrada = filtro.aplicar(imagem_original)
            caminho_saida = self.imagem_atual.salvar(
                imagem_filtrada, sufixo, diretorio_destino=PASTA_IMAGENS_FILTRADAS
            )
            print(f"\nFiltro '{nome_filtro}' aplicado com sucesso!")
            print(f"   Imagem resultante salva em: {caminho_saida}\n")
        except Exception as erro:
            self._registrar_erro(
                f"aplicação do filtro '{nome_filtro}'", erro,
                "a imagem pode ter sido movida/apagada, ou não há permissão "
                f"de escrita na pasta '{PASTA_IMAGENS_FILTRADAS}'.",
            )

        pausar()

    def listar_imagens_diretorio(self):
        limpar_tela()
        print("=" * 55)
        print("        FOTOS DISPONÍVEIS")
        print("=" * 55)

        if not os.path.isdir(PASTA_REPOSITORIO_FOTOS):
            print(
                f"A pasta '{PASTA_REPOSITORIO_FOTOS}/' não foi encontrada. "
                "Crie-a e coloque as fotos disponíveis dentro dela.\n"
            )
            pausar()
            return

        try:
            arquivos = sorted(os.listdir(PASTA_REPOSITORIO_FOTOS))
        except OSError as erro:
            self._registrar_erro(
                "listagem de imagens", erro,
                f"não foi possível ler a pasta '{PASTA_REPOSITORIO_FOTOS}' "
                "(verifique permissões de acesso).",
            )
            pausar()
            return

        imagens = [a for a in arquivos if a.lower().endswith(EXTENSOES_IMAGEM)]

        if not imagens:
            print(
                f"Nenhum arquivo de imagem (.jpg/.png) encontrado em "
                f"'{PASTA_REPOSITORIO_FOTOS}/'.\n"
            )
            pausar()
            return

        print(f"Imagens encontradas em '{PASTA_REPOSITORIO_FOTOS}/':\n")
        for indice, nome_arquivo in enumerate(imagens, start=1):
            print(f"  {indice}. {nome_arquivo}")
        print()
        pausar()

    def listar_imagens_filtradas(self):
        """
        Percorre a pasta PASTA_IMAGENS_FILTRADAS e informa ao usuário quais
        arquivos de imagem estão lá dentro — ou seja, quais fotos já foram
        processadas por algum filtro pelo terminal.
        """
        limpar_tela()
        print("=" * 55)
        print("        IMAGENS JÁ FILTRADAS")
        print("=" * 55)

        if not os.path.isdir(PASTA_IMAGENS_FILTRADAS):
            print(
                f"A pasta '{PASTA_IMAGENS_FILTRADAS}/' ainda não existe. "
                "Nenhum filtro foi aplicado ainda.\n"
            )
            pausar()
            return

        try:
            arquivos = sorted(os.listdir(PASTA_IMAGENS_FILTRADAS))
        except OSError as erro:
            self._registrar_erro(
                "listagem de imagens filtradas", erro,
                f"não foi possível ler a pasta '{PASTA_IMAGENS_FILTRADAS}' "
                "(verifique permissões de acesso).",
            )
            pausar()
            return

        imagens = [a for a in arquivos if a.lower().endswith(EXTENSOES_IMAGEM)]

        if not imagens:
            print(
                f"Nenhuma imagem filtrada encontrada em "
                f"'{PASTA_IMAGENS_FILTRADAS}/' ainda. Use a opção 2 do menu "
                "para aplicar um filtro em alguma imagem.\n"
            )
            pausar()
            return

        print(f"Imagens já filtradas em '{PASTA_IMAGENS_FILTRADAS}/':\n")
        for indice, nome_arquivo in enumerate(imagens, start=1):
            print(f"  {indice}. {nome_arquivo}")
        print(f"\nTotal: {len(imagens)} imagem(ns) filtrada(s).\n")
        pausar()

    def apresentacao(self):
        largura_total = 60
        espaco_interno = largura_total - 6
        linha_universidade = "UNIVERSIDADE FEDERAL DO PIAUÍ - UFPI"
        linha_centro = "CENTRO DE CIÊNCIAS DA NATUREZA - CCN"
        linha_departamento = "DEPARTAMENTO DE COMPUTAÇÃO"
        linha_curso = "CURSO DE BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO"
        linha_disciplina = "DISCIPLINA DE LABORATÓRIO DE PROGRAMAÇÃO - 2026.1"
        linha_prof = "PROFESSOR DOUTOR ARMANDO SOARES SOUSA"

        print("\n")
        print('=' * largura_total)
        print('||' + ' ' * (largura_total - 4) + '||')
        print('|| ' + linha_universidade.ljust(espaco_interno) + ' ||')
        print('|| ' + linha_centro.ljust(espaco_interno) + ' ||')
        print('|| ' + linha_departamento.ljust(espaco_interno) + ' ||')
        print('|| ' + linha_curso.ljust(espaco_interno) + ' ||')
        print('|| ' + linha_disciplina.ljust(espaco_interno) + ' ||')
        print('|| ' + linha_prof.ljust(espaco_interno) + ' ||')
        print('||' + ' ' * (largura_total - 4) + '||')
        print('=' * largura_total)
        print("\n")

        linha_integrantes = "GRUPO 07 - INTEGRANTES: \n"
        print(linha_integrantes)
        integrantes = [
            "1. FRANCISCO SARMENTO NETO",
            "2. HUDSON IAGO CASTRO RÊGO",
            "3. MARIA EDUARDA DE OLIVEIRA SOUSA SILVA",
            "4. SHERLYSON MEMÓRIA DE SOUSA",
            "5. NOME COMPLETO DO LUIS",
        ]
        for integrante in integrantes:
            print(integrante)
            print("-" * 50)
        print("\n")

    def exibir_menu(self):
        print("=" * 70)
        print("        IMPLEMENTAÇÃO DE ALGORITMOS DE FILTROS DE IMAGEM")
        print("=" * 70)
        if self.imagem_atual:
            print(f"Imagem atual: {self.imagem_atual.nome}")
        else:
            print("Imagem atual: (nenhuma)")
        print("-" * 55)
        print("1. Informar o caminho da imagem")
        print("2. Escolher o filtro a ser aplicado")
        print(f"3. Listar fotos disponíveis em '{PASTA_REPOSITORIO_FOTOS}/'")
        print(f"4. Listar imagens já filtradas em '{PASTA_IMAGENS_FILTRADAS}/'")
        print("5. Sair")
        print("-" * 55)

    def executar(self):
        # A tela de apresentação é exibida apenas uma vez, antes do menu iniciar
        limpar_tela()
        self.apresentacao()
        pausar()

        while True:
            limpar_tela()
            self.exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.informar_caminho_imagem()
            elif opcao == "2":
                self.escolher_filtro()
            elif opcao == "3":
                self.listar_imagens_diretorio()
            elif opcao == "4":
                self.listar_imagens_filtradas()
            elif opcao == "5":
                limpar_tela()
                print("Encerrando o programa. Até logo!")
                break
            else:
                print(f"\nOpção inválida: '{opcao}'. Escolha um número de 1 a 5.\n")
                pausar()


if __name__ == "__main__":
    programa = Principal()
    programa.executar()
