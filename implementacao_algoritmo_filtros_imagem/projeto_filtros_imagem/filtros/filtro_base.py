

from abc import ABC, abstractmethod
from PIL import Image as PILImage


class FiltroBase(ABC):
    nome = "Filtro Base"

    @abstractmethod
    def aplicar(self, imagem_pil: PILImage.Image) -> PILImage.Image:
        """Recebe uma imagem PIL e retorna uma NOVA imagem PIL já filtrada."""
        raise NotImplementedError
