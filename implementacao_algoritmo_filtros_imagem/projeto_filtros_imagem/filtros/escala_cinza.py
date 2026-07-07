"""Filtro: Escala de Cinza."""

from PIL import Image as PILImage
from .filtro_base import FiltroBase


class FiltroEscalaCinza(FiltroBase):
    nome = "Escala de Cinza"

    def aplicar(self, imagem_pil: PILImage.Image) -> PILImage.Image:
        # "L" = modo de 8 bits, um único canal (luminância / escala de cinza)
        return imagem_pil.convert("L")
