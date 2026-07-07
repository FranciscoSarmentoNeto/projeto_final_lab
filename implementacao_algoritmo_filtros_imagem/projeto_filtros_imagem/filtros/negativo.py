
from PIL import Image as PILImage, ImageOps
from .filtro_base import FiltroBase


class FiltroNegativo(FiltroBase):
    nome = "Foto Negativa"

    def aplicar(self, imagem_pil: PILImage.Image) -> PILImage.Image:
        rgb = imagem_pil.convert("RGB")
        return ImageOps.invert(rgb)
