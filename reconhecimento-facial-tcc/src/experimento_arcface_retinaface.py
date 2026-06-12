# -*- coding: utf-8 -*-
"""Experimento comparativo com ArcFace + RetinaFace.

Critério principal: avaliação closed-set rank-1.
Todas as imagens de teste devem pertencer a pessoas previamente cadastradas.
"""

from __future__ import annotations

import time
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine

from utils import (
    DATA_DIR,
    RESULTS_DIR,
    extrair_nome_pessoa,
    listar_imagens,
    salvar_resultados_csv,
    salvar_resultados_json,
)

CAMINHO_IMAGENS_CONHECIDAS = DATA_DIR / "imagens_conhecidas"
PASTA_RAIZ_TESTES = DATA_DIR / "imagens_teste"

MODELO = "ArcFace"
DETECTOR_BACKEND = "retinaface"
USAR_CLAHE = True

CENARIOS_DE_TESTE = {
    "Cenário Ideal": PASTA_RAIZ_TESTES / "Ideal",
    "Baixa Luz": PASTA_RAIZ_TESTES / "Baixa_luz",
    "Contraluz": PASTA_RAIZ_TESTES / "Contra_luz",
}


def aplicar_clahe(img_bgr: np.ndarray) -> np.ndarray:
    """Melhora localmente o contraste em imagens com baixa iluminação."""
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l2 = clahe.apply(l)
    lab2 = cv2.merge((l2, a, b))
    return cv2.cvtColor(lab2, cv2.COLOR_LAB2BGR)


def gerar_variantes_imagem(img_bgr: np.ndarray) -> list[np.ndarray]:
    variantes = [img_bgr]
    if USAR_CLAHE:
        try:
            variantes.append(aplicar_clahe(img_bgr))
        except Exception:
            pass
    return variantes


def representar_imagem_retinaface(img_bgr: np.ndarray):
    """Extrai embedding usando DeepFace com ArcFace e detector RetinaFace."""
    embeddings = []
    for variante in gerar_variantes_imagem(img_bgr):
        try:
            reps = DeepFace.represent(
                img_path=variante,
                model_name=MODELO,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=True,
                align=True,
                normalization="ArcFace",
            )
            if reps and "embedding" in reps[0]:
                embeddings.append(np.array(reps[0]["embedding"], dtype=np.float32))
        except Exception:
            continue

    if not embeddings:
        return None, 0

    emb_medio = np.mean(np.vstack(embeddings), axis=0)
    return emb_medio, len(embeddings)


def carregar_imagem_bgr(caminho: Path):
    return cv2.imread(str(caminho))


def carregar_base_arcface():
    if not CAMINHO_IMAGENS_CONHECIDAS.exists():
        raise FileNotFoundError(f"A pasta '{CAMINHO_IMAGENS_CONHECIDAS}' não foi encontrada.")

    print("Carregando base com ArcFace + RetinaFace...")
    print(f"Detector backend: {DETECTOR_BACKEND}")
    print(f"CLAHE ativado: {USAR_CLAHE}")

    embeddings_por_pessoa = defaultdict(list)
    falhas_cadastro = []

    for caminho in listar_imagens(CAMINHO_IMAGENS_CONHECIDAS):
        img = carregar_imagem_bgr(caminho)
        if img is None:
            falhas_cadastro.append((caminho.name, "imagem inválida"))
            continue

        nome = extrair_nome_pessoa(caminho.name)
        emb, tentativas_ok = representar_imagem_retinaface(img)

        if emb is None:
            falhas_cadastro.append((caminho.name, "nenhum rosto detectado"))
            continue

        embeddings_por_pessoa[nome].append(emb)
        print(f"[CADASTRO OK] {caminho.name} -> identidade='{nome}' | tentativas_ok={tentativas_ok}")

    if falhas_cadastro:
        print("\nFalhas no cadastro:")
        for arquivo, motivo in falhas_cadastro:
            print(f" - {arquivo}: {motivo}")

    if not embeddings_por_pessoa:
        raise RuntimeError("Nenhuma identidade válida foi cadastrada.")

    nomes_conhecidos = []
    centroides_conhecidos = []

    for nome, lista_embs in embeddings_por_pessoa.items():
        centroide = np.mean(np.vstack(lista_embs), axis=0)
        nomes_conhecidos.append(nome)
        centroides_conhecidos.append(centroide)

    print("\nIdentidades cadastradas:")
    for nome, embs in embeddings_por_pessoa.items():
        print(f" - {nome}: {len(embs)} embedding(s)")

    return nomes_conhecidos, centroides_conhecidos


def executar_cenario(nome_cenario, caminho_cenario, nomes_conhecidos, centroides_conhecidos):
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
        img = carregar_imagem_bgr(caminho_teste)
        if img is None:
            print(f"  [FALHA] {caminho_teste.name}: imagem inválida.")
            continue

        total_testes += 1
        nome_esperado = extrair_nome_pessoa(caminho_teste.name)

        emb_teste, tentativas_ok = representar_imagem_retinaface(img)
        if emb_teste is None:
            falhas_deteccao += 1
            print(f"  [ERRO] {caminho_teste.name}: esperado '{nome_esperado}', mas nenhum rosto foi detectado.")
            continue

        distancias = [cosine(c, emb_teste) for c in centroides_conhecidos]
        idx = int(np.argmin(distancias))
        nome_encontrado = nomes_conhecidos[idx]
        menor_dist = float(distancias[idx])

        if nome_encontrado == nome_esperado:
            total_acertos += 1
            print(
                f"  [ACERTO] {caminho_teste.name}: '{nome_encontrado}' "
                f"(distância cosseno: {menor_dist:.4f}, tentativas_ok={tentativas_ok})"
            )
        else:
            erros_identidade += 1
            print(
                f"  [ERRO] {caminho_teste.name}: esperado '{nome_esperado}', "
                f"encontrado '{nome_encontrado}' "
                f"(distância cosseno: {menor_dist:.4f}, tentativas_ok={tentativas_ok})"
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


def main():
    try:
        nomes_conhecidos, centroides_conhecidos = carregar_base_arcface()
    except Exception as exc:
        print(f"Erro ao carregar a base: {exc}")
        return

    resultados_finais = {}

    print("\n--- INICIANDO TESTES ARCFACE + RETINAFACE ---")
    print("Critério: closed-set rank-1, sem classe 'desconhecido'.")

    for nome_cenario, caminho_cenario in CENARIOS_DE_TESTE.items():
        resultado = executar_cenario(
            nome_cenario,
            caminho_cenario,
            nomes_conhecidos,
            centroides_conhecidos,
        )
        if resultado:
            resultados_finais[nome_cenario] = resultado

    if resultados_finais:
        salvar_resultados_csv(RESULTS_DIR / "resultados_arcface_retinaface.csv", resultados_finais)
        salvar_resultados_json(RESULTS_DIR / "resultados_arcface_retinaface.json", resultados_finais)
        print("\nResultados salvos em results/resultados_arcface_retinaface.csv e results/resultados_arcface_retinaface.json")


if __name__ == "__main__":
    main()
