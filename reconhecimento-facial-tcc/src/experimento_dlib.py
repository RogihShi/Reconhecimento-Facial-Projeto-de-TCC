# -*- coding: utf-8 -*-
"""Experimento comparativo com dlib/face_recognition.

Critério principal: avaliação closed-set rank-1.
Todas as imagens de teste devem pertencer a pessoas previamente cadastradas.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import List, Tuple

import face_recognition
import numpy as np

from utils import (
    DATA_DIR,
    RESULTS_DIR,
    extrair_nome_pessoa,
    listar_imagens,
    salvar_resultados_csv,
    salvar_resultados_json,
)

PASTA_IMAGENS_CONHECIDAS = DATA_DIR / "imagens_conhecidas"
PASTA_RAIZ_TESTES = DATA_DIR / "imagens_teste"
MODELO_DETECCAO_DLIB = "hog"  # use "cnn" se houver suporte e recursos computacionais

CENARIOS_DE_TESTE = {
    "Cenário Ideal": PASTA_RAIZ_TESTES / "Ideal",
    "Baixa Luz": PASTA_RAIZ_TESTES / "Baixa_luz",
    "Contraluz": PASTA_RAIZ_TESTES / "Contra_luz",
}


def carregar_base_dlib(pasta: Path) -> Tuple[List[np.ndarray], List[str]]:
    codificacoes_conhecidas: List[np.ndarray] = []
    nomes_conhecidos: List[str] = []

    if not pasta.exists():
        raise FileNotFoundError(f"A pasta '{pasta}' não foi encontrada.")

    print("Carregando base de dados com dlib/face_recognition...")

    for caminho in listar_imagens(pasta):
        nome_pessoa = extrair_nome_pessoa(caminho.name)
        try:
            imagem = face_recognition.load_image_file(str(caminho))
            locais = face_recognition.face_locations(imagem, model=MODELO_DETECCAO_DLIB)
            encodings = face_recognition.face_encodings(imagem, locais)

            if not encodings:
                print(f"AVISO: Nenhum rosto detectado em '{caminho.name}' no cadastro. Imagem ignorada.")
                continue

            codificacoes_conhecidas.append(encodings[0])
            nomes_conhecidos.append(nome_pessoa)
        except Exception as exc:
            print(f"AVISO: Não foi possível processar '{caminho.name}' no cadastro. Erro: {exc}")

    if not codificacoes_conhecidas:
        raise RuntimeError("Nenhuma codificação válida foi carregada da base.")

    print(f"Total de embeddings carregados: {len(codificacoes_conhecidas)}")
    print(f"Pessoas da base: {sorted(set(nomes_conhecidos))}")
    return codificacoes_conhecidas, nomes_conhecidos


def prever_identidade_dlib(
    codificacao_teste: np.ndarray,
    codificacoes_conhecidas: List[np.ndarray],
    nomes_conhecidos: List[str],
) -> Tuple[str, float]:
    distancias = face_recognition.face_distance(codificacoes_conhecidas, codificacao_teste)
    indice_melhor = int(np.argmin(distancias))
    return nomes_conhecidos[indice_melhor], float(distancias[indice_melhor])


def executar_cenario_dlib(
    nome_cenario: str,
    caminho_cenario: Path,
    codificacoes_conhecidas: List[np.ndarray],
    nomes_conhecidos: List[str],
) -> dict:
    print("\n=========================================")
    print(f"Processando: {nome_cenario}")
    print(f"Pasta: {caminho_cenario}")
    print("=========================================")

    arquivos = listar_imagens(caminho_cenario)
    if not arquivos:
        print(f"Nenhuma imagem válida encontrada em '{caminho_cenario}'.")
        return {}

    total_testes = 0
    total_acertos = 0
    falhas_deteccao = 0
    erros_identidade = 0
    tempo_inicio = time.time()

    for caminho_teste in arquivos:
        nome_esperado = extrair_nome_pessoa(caminho_teste.name)
        total_testes += 1

        try:
            frame = face_recognition.load_image_file(str(caminho_teste))
            locais_rostos = face_recognition.face_locations(frame, model=MODELO_DETECCAO_DLIB)
            codificacoes = face_recognition.face_encodings(frame, locais_rostos)
        except Exception as exc:
            print(f"  [FALHA] {caminho_teste.name}: erro ao processar. {exc}")
            falhas_deteccao += 1
            continue

        if not codificacoes:
            falhas_deteccao += 1
            print(f"  [ERRO] {caminho_teste.name}: esperado '{nome_esperado}', mas nenhum rosto foi detectado.")
            continue

        nome_previsto, distancia = prever_identidade_dlib(
            codificacoes[0], codificacoes_conhecidas, nomes_conhecidos
        )

        if nome_previsto == nome_esperado:
            total_acertos += 1
            print(f"  [ACERTO] {caminho_teste.name}: '{nome_previsto}' (distância: {distancia:.4f})")
        else:
            erros_identidade += 1
            print(
                f"  [ERRO] {caminho_teste.name}: esperado '{nome_esperado}', "
                f"encontrado '{nome_previsto}' (distância: {distancia:.4f})"
            )

    tempo_total = time.time() - tempo_inicio
    acuracia = (total_acertos / total_testes * 100) if total_testes else 0.0
    taxa_deteccao = ((total_testes - falhas_deteccao) / total_testes * 100) if total_testes else 0.0

    print(f"\nResultado - {nome_cenario}")
    print(f"Acurácia rank-1: {acuracia:.2f}% ({total_acertos}/{total_testes})")
    print(f"Taxa de detecção: {taxa_deteccao:.2f}%")
    print(f"Falhas de detecção: {falhas_deteccao}")
    print(f"Erros de identidade: {erros_identidade}")
    print(f"Tempo: {tempo_total:.2f}s")

    return {
        "acuracia": acuracia,
        "taxa_deteccao": taxa_deteccao,
        "falhas_deteccao": falhas_deteccao,
        "erros_identidade": erros_identidade,
        "total_testes": total_testes,
        "total_acertos": total_acertos,
        "tempo_total": tempo_total,
    }


def main() -> None:
    try:
        codificacoes_conhecidas, nomes_conhecidos = carregar_base_dlib(PASTA_IMAGENS_CONHECIDAS)
    except Exception as exc:
        print(f"Erro ao carregar a base: {exc}")
        return

    resultados_finais = {}

    print("\n--- INICIANDO TESTES DLIB / FACE_RECOGNITION ---")
    print("Critério: closed-set rank-1, sem classe 'desconhecido'.")

    for nome_cenario, caminho_cenario in CENARIOS_DE_TESTE.items():
        resultado = executar_cenario_dlib(
            nome_cenario,
            caminho_cenario,
            codificacoes_conhecidas,
            nomes_conhecidos,
        )
        if resultado:
            resultados_finais[nome_cenario] = resultado

    if resultados_finais:
        salvar_resultados_csv(RESULTS_DIR / "resultados_dlib.csv", resultados_finais)
        salvar_resultados_json(RESULTS_DIR / "resultados_dlib.json", resultados_finais)
        print("\nResultados salvos em results/resultados_dlib.csv e results/resultados_dlib.json")


if __name__ == "__main__":
    main()
