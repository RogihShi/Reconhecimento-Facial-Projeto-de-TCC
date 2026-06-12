# Roteiro de coleta de imagens

Este roteiro orienta a coleta local das imagens utilizadas nos experimentos de reconhecimento facial. As imagens coletadas não devem ser publicadas no GitHub, pois representam dados biométricos sensíveis.

## 1. Preparação do ambiente

Antes da captura, organize um ambiente controlado, com câmera fixa e distância semelhante entre participante e câmera.

Recomendações:

- usar câmera RGB com resolução mínima de 1080p/30fps;
- posicionar a câmera em tripé ou superfície fixa;
- manter distância aproximada entre 0,6 m e 1,2 m;
- evitar movimentação brusca durante a captura;
- manter o enquadramento do rosto centralizado;
- registrar as condições utilizadas em cada cenário.

## 2. Participantes e consentimento

A coleta deve ser feita apenas com autorização dos participantes. Como imagens faciais são dados biométricos sensíveis, recomenda-se registrar o consentimento para uso acadêmico e manter os arquivos apenas em ambiente local.

## 3. Estrutura local das imagens

As imagens devem ser organizadas assim:

```text
data/
├── imagens_conhecidas/
└── imagens_teste/
    ├── Ideal/
    ├── Baixa_luz/
    └── Contra_luz/
```

## 4. Cadastro das pessoas conhecidas

Na pasta `data/imagens_conhecidas/`, coloque ao menos uma imagem de cadastro por pessoa.

Exemplo:

```text
data/imagens_conhecidas/
├── higor.jpg
├── pessoa1.jpg
└── pessoa2.jpg
```

## 5. Cenários de teste

### 5.1 Cenário ideal

Condição com iluminação frontal, rosto visível e textura facial nítida.

Exemplo de nomes:

```text
data/imagens_teste/Ideal/
├── higor_ideal_01.jpg
├── higor_ideal_02.jpg
└── pessoa1_ideal_01.jpg
```

### 5.2 Baixa luz

Condição com pouca iluminação, simulando perda de detalhes e aumento de ruído.

Exemplo de nomes:

```text
data/imagens_teste/Baixa_luz/
├── higor_baixa_luz_01.jpg
├── higor_baixa_luz_02.jpg
└── pessoa1_baixa_luz_01.jpg
```

### 5.3 Contraluz

Condição com fonte de luz atrás do participante, gerando subexposição da face.

Exemplo de nomes:

```text
data/imagens_teste/Contra_luz/
├── higor_contraluz_01.jpg
├── higor_contraluz_02.jpg
└── pessoa1_contraluz_01.jpg
```

## 6. Padronização dos nomes

O nome esperado da pessoa deve aparecer no início do arquivo, antes do primeiro sublinhado.

Exemplos:

```text
higor_ideal_01.jpg -> higor
pessoa1_contraluz_02.jpg -> pessoa1
```

## 7. Observação sobre imagens ilustrativas

Imagens geradas por IA podem ser usadas no TCC ou em apresentações apenas para representar visualmente os cenários. Elas não devem ser misturadas com as imagens reais de teste, a menos que o objetivo seja outro experimento específico.

## 8. Checklist de coleta

- [ ] Câmera fixa.
- [ ] Rosto centralizado.
- [ ] Imagem de cadastro para cada pessoa.
- [ ] Imagens separadas por cenário.
- [ ] Nome dos arquivos padronizado.
- [ ] Imagens reais mantidas fora do GitHub.
- [ ] Consentimento dos participantes registrado.
