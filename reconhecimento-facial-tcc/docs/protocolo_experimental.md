# Protocolo experimental de replicação

Este documento descreve como replicar os experimentos de reconhecimento facial e como interpretar os resultados gerados pelos scripts.

## 1. Preparar o ambiente

Clone o repositório e instale as dependências:

```bash
git clone LINK_DO_REPOSITORIO
cd reconhecimento-facial-tcc
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Organizar a base local

Siga o roteiro de coleta em `docs/roteiro_coleta.md` e organize as imagens em:

```text
data/imagens_conhecidas/
data/imagens_teste/Ideal/
data/imagens_teste/Baixa_luz/
data/imagens_teste/Contra_luz/
```

## 3. Executar o pipeline dlib/face_recognition

```bash
python src/experimento_dlib.py
```

O script irá:

1. carregar os rostos cadastrados;
2. percorrer as imagens de teste;
3. detectar o rosto;
4. extrair o embedding;
5. classificar pelo cadastro mais próximo;
6. calcular métricas por cenário.

## 4. Executar o pipeline ArcFace + RetinaFace

```bash
python src/experimento_arcface_retinaface.py
```

O script irá:

1. carregar as imagens cadastradas;
2. extrair embeddings com ArcFace;
3. usar RetinaFace para detecção;
4. comparar as imagens de teste por distância cosseno;
5. salvar os resultados em `results/`.

## 5. Executar o protótipo de PAD ativo

```bash
python src/reconhecedor_facial.py
```

O sistema abrirá a webcam e solicitará comandos visuais, como piscar, abrir a boca e virar a cabeça. O reconhecimento só é liberado após a execução correta dos desafios.

## 6. Métricas utilizadas

### Acurácia rank-1

Percentual de imagens em que a identidade correta foi escolhida como primeira opção no regime fechado.

### Taxa de detecção facial

Percentual de imagens em que o sistema conseguiu localizar um rosto.

### Falhas de detecção

Número de imagens em que nenhum rosto foi detectado.

### Erros de identidade

Número de imagens em que o rosto foi detectado, mas a identidade prevista foi diferente da esperada.

### Tempo de execução

Tempo total necessário para processar cada cenário.

## 7. Protocolo exploratório de PAD

Para avaliar o PAD ativo de forma exploratória, recomenda-se registrar tentativas em três grupos:

1. fotografia estática;
2. vídeo comum reproduzido em tela;
3. vídeo preparado, no qual o atacante conhece os tipos de desafios possíveis, mas não a ordem exata.

Registre para cada tentativa:

- tipo de ataque;
- número da tentativa;
- se foi bloqueado;
- se houve aceitação indevida;
- observações sobre iluminação, tela e distância.

## 8. Limite da avaliação

Este protocolo não substitui validação biométrica formal. Para uma avaliação completa de PAD, seria necessário incluir amostras bona fide padronizadas e calcular métricas como APCER e BPCER.
