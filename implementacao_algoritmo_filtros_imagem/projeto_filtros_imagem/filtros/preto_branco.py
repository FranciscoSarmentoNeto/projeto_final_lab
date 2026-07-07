
from PIL import Image as PILImage
from .filtro_base import FiltroBase

# Qualquer pixel com luminância acima deste valor vira branco; abaixo, preto.
LIMIAR_BINARIZACAO = 128


class FiltroPretoBranco(FiltroBase):
    nome = "Preto e Branco"

    def aplicar(self, imagem_pil: PILImage.Image) -> PILImage.Image:
        cinza = imagem_pil.convert("L")
        binarizada = cinza.point(lambda pixel: 255 if pixel > LIMIAR_BINARIZACAO else 0)
        return binarizada.convert("L")
