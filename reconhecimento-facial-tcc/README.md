# Reconhecimento Facial: Análise Experimental de Robustez e Limites de Confiabilidade de Segurança

Este repositório reúne o código-fonte, a estrutura de pastas e os documentos de apoio do Trabalho de Conclusão de Curso de **Higor Silva Sudario**, desenvolvido no curso de Ciência da Computação da PUC Goiás.

O projeto avalia a robustez de dois pipelines de reconhecimento facial em três cenários de iluminação: **ideal**, **baixa luz** e **contraluz**. Também apresenta uma implementação exploratória de **Presentation Attack Detection (PAD)** ativo por desafio-resposta visual, com o objetivo de mitigar tentativas de fraude por foto e vídeo.

## Objetivo do projeto

Comparar o desempenho dos pipelines **dlib/face_recognition** e **ArcFace + RetinaFace** sob condições ambientais distintas, utilizando métricas como:

- acurácia rank-1;
- taxa de detecção facial;
- falhas de detecção;
- erros de identidade;
- tempo de execução;
- taxa exploratória de aceitação indevida em ataques por foto e vídeo.

## Estrutura do repositório

```text
reconhecimento-facial-tcc/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── CITATION.cff
│
├── src/
│   ├── reconhecedor_facial.py
│   ├── experimento_dlib.py
│   ├── experimento_arcface_retinaface.py
│   └── utils.py
│
├── data/
│   ├── imagens_conhecidas/
│   └── imagens_teste/
│       ├── Ideal/
│       ├── Baixa_luz/
│       └── Contra_luz/
│
├── results/
│   └── graficos/
│
├── docs/
│   ├── roteiro_coleta.md
│   ├── protocolo_experimental.md
│   ├── continuidade_pesquisa.md
│   ├── seguranca_privacidade.md
│   ├── publicacao_github.md
│   └── texto_para_tcc.md
│
└── assets/
    └── figuras_ilustrativas/
```

## Observação importante sobre os dados

As imagens reais utilizadas nos experimentos **não devem ser publicadas neste repositório**, pois envolvem dados biométricos sensíveis. A pasta `data/` contém apenas a estrutura esperada para replicação local.

Para replicar o experimento, cada pesquisador deve criar sua própria base de imagens localmente, seguindo o roteiro disponível em [`docs/roteiro_coleta.md`](docs/roteiro_coleta.md).

## Tecnologias utilizadas

- Python
- OpenCV
- NumPy
- face_recognition / dlib
- DeepFace
- ArcFace
- RetinaFace
- SciPy
- Pandas

## Preparação do ambiente

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Observação: a instalação de `dlib` e `face_recognition` pode exigir compiladores, CMake e dependências adicionais do sistema operacional.

## Como organizar as imagens

Crie as imagens localmente na seguinte estrutura:

```text
data/
├── imagens_conhecidas/
│   ├── higor.jpg
│   ├── pessoa1.jpg
│   └── pessoa2.jpg
└── imagens_teste/
    ├── Ideal/
    │   ├── higor_ideal_01.jpg
    │   └── pessoa1_ideal_01.jpg
    ├── Baixa_luz/
    │   ├── higor_baixa_luz_01.jpg
    │   └── pessoa1_baixa_luz_01.jpg
    └── Contra_luz/
        ├── higor_contraluz_01.jpg
        └── pessoa1_contraluz_01.jpg
```

A função de avaliação extrai o nome esperado a partir do início do arquivo. Por exemplo:

```text
higor_contraluz_01.jpg -> higor
pessoa1_baixa_luz_02.jpg -> pessoa1
```

## Execução dos experimentos

### Pipeline dlib/face_recognition

```bash
python src/experimento_dlib.py
```

### Pipeline ArcFace + RetinaFace

```bash
python src/experimento_arcface_retinaface.py
```

### Protótipo com PAD ativo

```bash
python src/reconhecedor_facial.py
```

## Resultados

Os scripts salvam automaticamente os resultados na pasta `results/`, em formato CSV e JSON, quando possível.

## Documentos de apoio

- [`docs/roteiro_coleta.md`](docs/roteiro_coleta.md): roteiro para coleta de imagens nos três cenários.
- [`docs/protocolo_experimental.md`](docs/protocolo_experimental.md): instruções para replicar os testes e interpretar métricas.
- [`docs/continuidade_pesquisa.md`](docs/continuidade_pesquisa.md): sugestões para continuidade da pesquisa.
- [`docs/seguranca_privacidade.md`](docs/seguranca_privacidade.md): cuidados com privacidade e dados biométricos.
- [`docs/publicacao_github.md`](docs/publicacao_github.md): comandos para publicar o projeto no GitHub.
- [`docs/texto_para_tcc.md`](docs/texto_para_tcc.md): texto sugerido para citar o repositório no TCC.

## Limitações

Este projeto possui caráter acadêmico e experimental. A avaliação do PAD ativo foi exploratória e não substitui uma validação biométrica formal com métricas APCER/BPCER. Os resultados também não devem ser generalizados estatisticamente devido ao tamanho reduzido da base experimental.

## Autor

**Higor Silva Sudario**  
Ciência da Computação — PUC Goiás  
Orientador: Prof. Me. Rafael Leal Martins
