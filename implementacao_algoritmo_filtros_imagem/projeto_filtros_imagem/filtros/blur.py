"""Filtro: Blurred (desfoque gaussiano)."""

from PIL import Image as PILImage, ImageFilter
from .filtro_base import FiltroBase

RAIO_DESFOQUE = 6  # quanto maior, mais borrada fica a imagem


class FiltroBlur(FiltroBase):
    nome = "Blurred"

    def aplicar(self, imagem_pil: PILImage.Image) -> PILImage.Image:
        rgb = imagem_pil.convert("RGB")
        return rgb.filter(ImageFilter.GaussianBlur(radius=RAIO_DESFOQUE))
