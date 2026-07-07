"""
Classe Imagem
-------------
Representa um arquivo de imagem (.jpg ou .png) manipulado pelo programa.

Responsabilidades:
- Guardar o caminho e o nome do arquivo.
- Validar se a extensão é suportada (.jpg, .jpeg, .png).
- Carregar a imagem em memória usando a biblioteca Pillow (PIL).
- Salvar uma nova imagem (por exemplo, após aplicar um filtro).
"""

import os
from PIL import Image as PILImage, UnidentifiedImageError

# Extensões de imagem aceitas pelo programa
EXTENSOES_VALIDAS = (".jpg", ".jpeg", ".png")


class ExtensaoInvalidaError(Exception):
    """Lançada quando o arquivo informado não é .jpg/.jpeg/.png."""
    pass


class Imagem:
    def __init__(self, caminho: str):
        """
        caminho: caminho local do arquivo de imagem (já deve existir no disco).
        """
        self.caminho = caminho
        self.nome = os.path.basename(caminho)
        self.extensao = os.path.splitext(caminho)[1].lower()
        self._objeto_pil = None  # imagem carregada em memória (lazy loading)

        self._validar_extensao()

    def _validar_extensao(self):
        if self.extensao not in EXTENSOES_VALIDAS:
            raise ExtensaoInvalidaError(
                f"Extensão '{self.extensao}' não suportada. "
                f"Use um arquivo {', '.join(EXTENSOES_VALIDAS)}."
            )

    def carregar(self) -> PILImage.Image:
        """
        Carrega a imagem do disco para a memória (objeto PIL.Image).
        Lança FileNotFoundError ou UnidentifiedImageError em caso de problema.
        """
        if not os.path.isfile(self.caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho}")

        try:
            self._objeto_pil = PILImage.open(self.caminho)
            # força a leitura completa dos dados para detectar arquivos corrompidos
            self._objeto_pil.load()
        except UnidentifiedImageError:
            raise UnidentifiedImageError(
                f"O arquivo '{self.caminho}' não é uma imagem válida ou está corrompido."
            )

        return self._objeto_pil

    def salvar(self, imagem_pil: PILImage.Image, sufixo: str, diretorio_destino: str = ".") -> str:
        """
        Salva uma imagem (normalmente já filtrada) no diretório informado.
        O nome do arquivo de saída é: <nome_original>_<sufixo><extensao_original>

        Retorna o caminho completo do arquivo salvo.
        """
        nome_base = os.path.splitext(self.nome)[0]
        nome_saida = f"{nome_base}_{sufixo}{self.extensao}"
        caminho_saida = os.path.join(diretorio_destino, nome_saida)

        # Imagens em modo "RGBA" não podem ser salvas em JPG (sem canal alfa)
        if self.extensao in (".jpg", ".jpeg") and imagem_pil.mode in ("RGBA", "P"):
            imagem_pil = imagem_pil.convert("RGB")

        imagem_pil.save(caminho_saida)
        return caminho_saida

    def __str__(self):
        return f"Imagem(nome={self.nome}, extensao={self.extensao}, caminho={self.caminho})"
