"""
Pacote "filtros"
-----------------
Cada filtro disponível no programa é implementado como uma classe própria,
que herda de FiltroBase e implementa o método aplicar(imagem_pil).

Este arquivo expõe um dicionário FILTROS_DISPONIVEIS que o menu principal
usa para listar as opções e instanciar o filtro escolhido pelo usuário.
"""

from .escala_cinza import FiltroEscalaCinza
from .preto_branco import FiltroPretoBranco
from .cartoon import FiltroCartoon
from .negativo import FiltroNegativo
from .contorno import FiltroContorno
from .blur import FiltroBlur

# Dicionário: opção do menu -> (nome amigável, classe do filtro, sufixo do arquivo de saída)
FILTROS_DISPONIVEIS = {
    "1": ("Escala de Cinza", FiltroEscalaCinza, "cinza"),
    "2": ("Preto e Branco", FiltroPretoBranco, "pb"),
    "3": ("Cartoon", FiltroCartoon, "cartoon"),
    "4": ("Foto Negativa", FiltroNegativo, "negativo"),
    "5": ("Contorno", FiltroContorno, "contorno"),
    "6": ("Blurred", FiltroBlur, "blur"),
}
