# Programa de Filtros de Imagem

Projeto da 3ª Avaliação — Laboratório de Programação.

Programa em Python, orientado a objetos, que aplica filtros (Escala de
Cinza, Preto e Branco, Cartoon, Foto Negativa, Contorno e Blurred) em
imagens `.jpg`/`.png` locais ou baixadas de uma URL pública.

## Estrutura do projeto

```
implementacao_algoritmos_filtros_imagem/
├── main.py                  # Classe Principal: menu interativo do programa
├── requirements.txt
├── models/
│   ├── imagem.py             # Classe Imagem
│   └── download.py           # Classe Download
├── filtros/
│   ├── filtro_base.py         # Classe abstrata FiltroBase
│   ├── escala_cinza.py        # FiltroEscalaCinza
│   ├── preto_branco.py        # FiltroPretoBranco
│   ├── cartoon.py             # FiltroCartoon
│   ├── negativo.py            # FiltroNegativo
│   ├── contorno.py            # FiltroContorno
│   └── blur.py                # FiltroBlur
├── imagens_filtradas/
└── repositorio_de_fotos
```

## Como funciona (orientação a objetos)

- **`Imagem`** (`models/imagem.py`): representa o arquivo de imagem. Valida
  a extensão, carrega o arquivo em memória (via Pillow) e salva o
  resultado de um filtro no disco.
- **`Download`** (`models/download.py`): detecta se o caminho informado é
  uma URL e, se for, baixa a imagem e a salva localmente.
- **`FiltroBase`** (`filtros/filtro_base.py`): classe abstrata que define o
  método `aplicar(imagem_pil)`. Cada filtro concreto (`FiltroEscalaCinza`,
  `FiltroPretoBranco`, `FiltroCartoon`, `FiltroNegativo`, `FiltroContorno`,
  `FiltroBlur`) implementa essa mesma interface — por isso o programa
  principal consegue tratá-los de forma genérica (polimorfismo).
- **`Principal`** (`main.py`): integra tudo e exibe o menu com as 4 opções
  pedidas no enunciado.


## Instalação

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

## Exemplo de uso

```
1. Informar o caminho da imagem
   -> ./fotos/gato.jpg
   -> ou: https://exemplo.com/imagens/gato.png

2. Escolher o filtro a ser aplicado
   -> 1. Escala de Cinza
   -> 2. Preto e Branco
   -> 3. Cartoon
   -> 4. Foto Negativa
   -> 5. Contorno
   -> 6. Blurred

   Gera, por exemplo: gato_cinza.jpg (salvo automaticamente na pasta
   "imagens_filtradas/", que é criada pelo programa se ainda não existir)

3. Listar fotos disponíveis em "repositorio_de_fotos/"
4. Listar imagens já filtradas em "imagens_filtradas/"
5. Sair
```

## Pasta de saída das imagens filtradas

Toda imagem gerada por um filtro é salva automaticamente na pasta
`imagens_filtradas/` (o programa cria essa pasta sozinho, caso ela ainda
não exista). Para mudar o nome/local dessa pasta, basta alterar a
constante `PASTA_IMAGENS_FILTRADAS` no início do arquivo `main.py`.

## Pasta com as fotos disponíveis

A opção 3 do menu (**Listar fotos disponíveis**) lista apenas os arquivos
`.jpg`/`.png` que estiverem dentro da pasta `repositorio_de_fotos/`. Essa
pasta **não** é criada automaticamente ao iniciar o programa — vocês devem
criá-la e colocar as fotos de teste dentro dela (ou deixar o programa
criá-la sozinho ao baixar a primeira imagem de uma URL, veja abaixo).
Para mudar o nome dessa pasta, altere a constante
`PASTA_REPOSITORIO_FOTOS` em `main.py`.

Sempre que o usuário informar uma **URL** na opção 1 do menu, a imagem
baixada é salva automaticamente dentro de `repositorio_de_fotos/`
(a pasta é criada nesse momento, se ainda não existir).

## Experiência do usuário (limpar tela e pausas)

- A tela de apresentação da equipe aparece **uma única vez**, ao iniciar o
  programa.
- Antes de cada tela (menu principal, informar caminho, escolher filtro,
  listar fotos), o terminal é limpo (`limpar_tela()`), para não acumular
  informação antiga na tela.
- Depois de qualquer ação (sucesso, erro ou opção inválida), o programa
  pausa com "Pressione Enter para continuar..." antes de voltar ao menu,
  garantindo que o usuário sempre consiga ler a mensagem antes da tela
  ser limpa novamente.

## Tratamento de erros

O programa trata (com mensagens claras, sem travar):
- extensão de arquivo inválida;
- arquivo/caminho inexistente;
- arquivo corrompido ou que não é uma imagem válida;
- falhas de rede/URL inválida no download;
- opções inválidas no menu.

## Como estender (adicionar um novo filtro)

1. Criar um novo arquivo em `filtros/`, por exemplo `sepia.py`, com uma
   classe que herda de `FiltroBase` e implementa `aplicar(imagem_pil)`.
2. Registrar essa classe no dicionário `FILTROS_DISPONIVEIS` em
   `filtros/__init__.py`.

Nenhuma outra parte do código precisa mudar — é o benefício de usar
orientação a objetos e polimorfismo aqui.
