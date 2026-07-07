
from PIL import Image as PILImage, ImageFilter
from .filtro_base import FiltroBase


class FiltroContorno(FiltroBase):
    nome = "Contorno"

    def aplicar(self, imagem_pil: PILImage.Image) -> PILImage.Image:
        rgb = imagem_pil.convert("RGB")
        return rgb.filter(ImageFilter.CONTOUR)
