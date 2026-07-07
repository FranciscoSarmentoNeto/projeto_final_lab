"""
Classe Download
----------------
Responsável por baixar uma imagem publicada na internet (URL) e
salvá-la localmente no diretório atual, para que depois possa ser
tratada pela classe Imagem.
"""

import os
import requests
from urllib.parse import urlparse


class DownloadError(Exception):
    """Lançada quando não é possível baixar ou salvar a imagem."""
    pass


class Download:
    # Tipos de conteúdo aceitos (jpg/png)
    TIPOS_ACEITOS = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
    }

    def __init__(self, diretorio_destino: str = "."):
        self.diretorio_destino = diretorio_destino

    @staticmethod
    def eh_url(caminho: str) -> bool:
        """Verifica se a string informada é uma URL (http/https)."""
        resultado = urlparse(caminho)
        return resultado.scheme in ("http", "https") and bool(resultado.netloc)

    def baixar(self, url: str) -> str:
        """
        Faz o download da imagem a partir da URL informada e salva
        localmente. Retorna o caminho do arquivo salvo.
        """
        try:
            resposta = requests.get(url, timeout=15, stream=True)
            resposta.raise_for_status()
        except requests.exceptions.RequestException as erro:
            raise DownloadError(f"Falha ao baixar a imagem: {erro}")

        content_type = resposta.headers.get("Content-Type", "").split(";")[0].strip()

        # Tenta descobrir a extensão pelo Content-Type; se não achar,
        # tenta usar a extensão do próprio nome do arquivo na URL.
        extensao = self.TIPOS_ACEITOS.get(content_type)
        if extensao is None:
            nome_na_url = os.path.basename(urlparse(url).path)
            _, ext_url = os.path.splitext(nome_na_url)
            ext_url = ext_url.lower()
            if ext_url in (".jpg", ".jpeg", ".png"):
                extensao = ext_url
            else:
                raise DownloadError(
                    "A URL não aponta para uma imagem .jpg ou .png válida "
                    f"(Content-Type recebido: '{content_type}')."
                )

        nome_arquivo = os.path.basename(urlparse(url).path) or "imagem_baixada"
        nome_arquivo = os.path.splitext(nome_arquivo)[0] + extensao

        caminho_local = os.path.join(self.diretorio_destino, nome_arquivo)

        try:
            with open(caminho_local, "wb") as arquivo:
                for pedaco in resposta.iter_content(chunk_size=8192):
                    arquivo.write(pedaco)
        except OSError as erro:
            raise DownloadError(f"Falha ao salvar a imagem localmente: {erro}")

        return caminho_local
