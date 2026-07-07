

from PIL import Image as PILImage, ImageFilter, ImageOps, ImageChops
from .filtro_base import FiltroBase


class FiltroCartoon(FiltroBase):
    nome = "Cartoon"

    def aplicar(self, imagem_pil: PILImage.Image) -> PILImage.Image:
        rgb = imagem_pil.convert("RGB")

        # 1) Suaviza a imagem e reduz a quantidade de cores (efeito "chapado")
        suavizada = rgb.filter(ImageFilter.MedianFilter(size=7))
        cores_reduzidas = ImageOps.posterize(suavizada, bits=4)

        # 2) Detecta as bordas a partir da versão em escala de cinza
        cinza = rgb.convert("L")
        bordas = cinza.filter(ImageFilter.FIND_EDGES)
        bordas = ImageOps.invert(bordas)
        # Binariza as bordas: traços ficam pretos, resto fica branco
        bordas = bordas.point(lambda pixel: 255 if pixel > 100 else 0)
        bordas_rgb = bordas.convert("RGB")

        # 3) Combina cores + bordas (multiplicação escurece onde há traço)
        cartoon = ImageChops.multiply(cores_reduzidas, bordas_rgb)
        return cartoon
