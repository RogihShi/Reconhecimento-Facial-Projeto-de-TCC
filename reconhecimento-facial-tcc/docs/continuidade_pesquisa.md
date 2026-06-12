# Continuidade da pesquisa

Este documento registra possíveis caminhos para ampliar a pesquisa em trabalhos futuros.

## 1. Ampliar a base experimental

A primeira melhoria recomendada é aumentar o número de participantes e a quantidade de imagens por pessoa. Isso permitiria uma análise estatística mais forte e reduziria o risco de conclusões limitadas a uma base pequena.

Sugestões:

- incluir mais participantes;
- variar idade, gênero, tom de pele e características faciais;
- coletar mais imagens por cenário;
- incluir diferentes câmeras e resoluções;
- repetir a coleta em dias diferentes.

## 2. Expandir os cenários ambientais

Além de ideal, baixa luz e contraluz, novos cenários podem ser incluídos:

- oclusão parcial;
- uso de óculos;
- uso de máscara facial;
- diferentes distâncias da câmera;
- variação de pose;
- movimento durante a captura;
- baixa resolução e compressão de imagem.

## 3. Avaliação biométrica formal

Para transformar o experimento em uma avaliação biométrica mais completa, recomenda-se calcular:

- FAR;
- FRR;
- EER;
- curvas ROC;
- curvas DET;
- CMC/rank-k em identificação 1:N.

Isso exige um protocolo com comparações genuínas e impostoras, além de variação sistemática de limiares.

## 4. Avaliação formal de PAD

A avaliação exploratória do PAD ativo pode ser expandida para um protocolo formal com:

- APCER;
- BPCER;
- conjunto bona fide padronizado;
- ataques com foto impressa;
- ataques com vídeo em tela;
- ataques com vídeo preparado;
- testes com diferentes telas e iluminações.

## 5. Sensores e hardware

Trabalhos futuros podem comparar câmera RGB com sensores adicionais:

- infravermelho;
- NIR;
- sensor de profundidade;
- ToF;
- luz estruturada;
- câmeras com HDR.

## 6. Modelos e pipelines

Novos pipelines podem ser testados:

- MTCNN + FaceNet;
- RetinaFace + ArcFace;
- MediaPipe Face Mesh + embeddings;
- modelos comerciais de liveness;
- modelos de detecção de deepfake.

## 7. Governança e LGPD

A continuidade da pesquisa também pode incluir:

- termo de consentimento mais formal;
- anonimização/pseudonimização dos dados;
- controle de acesso às imagens;
- política de retenção e exclusão de dados;
- Relatório de Impacto à Proteção de Dados Pessoais em cenários de maior risco.
