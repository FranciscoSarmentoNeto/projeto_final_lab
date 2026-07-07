# IMPLEMENTAÇÃO DO TRABALHO FINAL DA DISCIPLINA DE LABORATÓRIO DE PROGRAMAÇÃO

**Projeto da 3ª Avaliação — Laboratório de Programação (2026.1)**
Universidade Federal do Piauí (UFPI) — Centro de Ciências da Natureza (CCN)
Curso de Bacharelado em Ciência da Computação
Professor: Doutor Armando Soares Sousa

## Equipe 06 - Integrantes:
* Francisco Sarmento Neto
* Hudson Iago Castro Rêgo
* Luís Fernando Amorim Figueiredo da Silva
* Maria Eduarda de Oliveira Sousa Silva
* Sherlyson Memória de Sousa

## Trabalho Proposto
- Está presente nesse repositório como "Trabalho_Final_Proposto" anexado.



## Estrutura do Projeto

A árvore de diretórios do repositório reflete a seguinte organização modular:

```text
projeto_final_lab/
├── README.md                                         # Documentação do projeto
├── Trabalho_Final_Proposto.pdf                        # Enunciado oficial do projeto
│
├── imagens_filtradas/                                # Saída global de testes das imagens processadas
│   ├── 9c98fba4828d6739e4c35635f251fb18d81568657a..._blur.jpg
│   ├── 9c98fba4828d6739e4c35635f251fb18d81568657a..._cartoon.jpg
│   ├── 9c98fba4828d6739e4c35635f251fb18d81568657a..._cinza.jpg
│   ├── 9c98fba4828d6739e4c35635f251fb18d81568657a..._contorno.jpg
│   ├── 9c98fba4828d6739e4c35635f251fb18d81568657a..._negativo.jpg
│   └── 9c98fba4828d6739e4c35635f251fb18d81568657a..._pb.jpg
│
├── repositorio_de_fotos/                             # Banco local de imagens originais para teste
│   ├── 9c98fba4828d6739e4c35635f251fb18d81568657a...jpg
│   ├── imagem_1.jpg
│   ├── imagem_2.jpg
│   └── [imagem_3.jpg ... imagem_9.jpg]
│
└── implementacao_algoritmo_filtros_imagem/
    └── projeto_filtros_imagem/                       # Core da aplicação em Python
        ├── main.py                                   # Classe Principal (Menu Interativo e Fluxo)
        ├── requirements.txt                          # Dependências externas do projeto
        ├── .gitignore                                # Arquivo de omissão de logs e caches do Git
        ├── imagens_filtradas/                        # Cache local para salvamento interno de filtros
        │
        ├── models/                                   # Pacote das classes de dados e utilitários
        │   ├── __init__.py
        │   ├── download.py                           # Classe Download (Manipulação de requisições web)
        │   └── imagem.py                             # Classe Imagem (Mapeamento e validação de arquivos)
        │
        └── filtros/                                  # Pacote contendo o polimorfismo dos filtros
            ├── __init__.py                           # Registro interno de filtros ativos
            ├── filtro_base.py                        # Classe abstrata/mãe FiltroBase
            ├── blur.py                               # Implementação do Modo Blurred
            ├── cartoon.py                            # Implementação do Filtro Cartoon
            ├── contorno.py                           # Implementação do Modo Contorno
            ├── escala_cinza.py                       # Implementação do Filtro Escala de Cinza
            ├── negativo.py                           # Implementação do Modo Foto Negativa
            └── preto_branco.py                       # Implementação do Filtro Preto e Branco
```

## Funcionalidades

| | Funcionalidade | Descrição |
|---|---|---|
| 1 | Informar o caminho da imagem | Aceita caminho local **ou** URL pública; detecta automaticamente qual é qual |
| 2 | Escolher o filtro a ser aplicado | 6 filtros disponíveis, aplicados sobre a imagem carregada |
| 3 | Listar fotos disponíveis | Lista os arquivos `.jpg`/`.png` da pasta `repositorio_de_fotos/` |
| 4 | Listar imagens já filtradas | Lista os arquivos `.jpg`/`.png` da pasta `imagens_filtradas/` |
| 5 | Sair | Encerra o programa |


### Filtros disponíveis

| Filtro | Efeito |
|---|---|
| **Escala de Cinza** | Converte a imagem para tons de cinza |
| **Preto e Branco** | Binariza a imagem (cada pixel vira preto ou branco) |
| **Cartoon** | Simula um desenho animado (cores "chapadas" + contorno em traço) |
| **Foto Negativa** | Inverte todas as cores da imagem |
| **Contorno** | Detecta e realça as bordas dos objetos |
| **Blurred** | Aplica desfoque gaussiano |



## Arquitetura implementada:

```
                      ┌───────────────────┐
                      │     Principal     │  (main.py)
                      │  menu interativo  │
                      └─────────┬─────────┘
                                │ usa
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
     ┌─────────────┐     ┌─────────────┐     ┌───────────────┐
     │   Imagem    │     │  Download   │     │  FiltroBase   │  (abstrata)
     │ carrega/    │     │ baixa da    │     │ aplicar(img)  │
     │ salva PIL   │     │ internet    │     └───────┬───────┘
     └─────────────┘     └─────────────┘             │ herdam
                                          ┌───────────┼─────────────┬───────────┬────────────┬───────────┐
                                          ▼           ▼             ▼           ▼            ▼           ▼
                                    EscalaCinza  PretoBranco    Cartoon    Negativo      Contorno      Blur
```


- **`Imagem`** (`models/imagem.py`): representa o arquivo de imagem.
  Valida a extensão (`.jpg`/`.jpeg`/`.png`), carrega o arquivo em memória
  via Pillow e salva o resultado de um filtro em uma pasta de destino.
- **`Download`** (`models/download.py`): detecta se o caminho informado é
  uma URL (`Download.eh_url`) e, se for, baixa a imagem e a salva
  localmente, validando o `Content-Type` da resposta.
- **`FiltroBase`** (`filtros/filtro_base.py`): classe abstrata (`ABC`) que
  define o contrato `aplicar(imagem_pil) -> imagem_pil`. Cada filtro
  concreto implementa essa mesma interface, permitindo que o programa
  principal trate qualquer filtro de forma genérica (**polimorfismo**).
- **`Principal`** (`main.py`): integra todas as classes acima e conduz o
  menu interativo do usuário.



  ## Instalação

Pré-requisito: Python 3.10 ou superior.

```bash
git clone <link-do-repositorio>
cd projeto_filtros_imagem

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
   -> ./repositorio_de_fotos/gato.jpg
   -> ou: https://exemplo.com/imagens/gato.png   (baixada automaticamente)

2. Escolher o filtro a ser aplicado
   -> 1. Escala de Cinza
   -> 2. Preto e Branco
   -> 3. Cartoon
   -> 4. Foto Negativa
   -> 5. Contorno
   -> 6. Blurred

   Gera, por exemplo: gato_cinza.jpg, salvo automaticamente em
   imagens_filtradas/

3. Listar fotos disponíveis em 'repositorio_de_fotos/'
4. Listar imagens já filtradas em 'imagens_filtradas/'
5. Sair
```

## Como estender (adicionar um novo filtro)

1. Criar um novo arquivo em `filtros/`, por exemplo `sepia.py`, com uma
   classe que herda de `FiltroBase` e implementa `aplicar(imagem_pil)`.
2. Registrar essa classe no dicionário `FILTROS_DISPONIVEIS`, em
   `filtros/__init__.py`.


## Dependências

```
Pillow>=10.0.0
requests>=2.31.0
```
