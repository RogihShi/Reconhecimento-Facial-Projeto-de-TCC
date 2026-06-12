# -*- coding: utf-8 -*-
"""Protótipo de reconhecimento facial com PAD ativo por desafio-resposta.

Este script usa webcam, face_recognition/dlib e landmarks faciais para solicitar
desafios visuais simples, como piscar, abrir a boca e virar a cabeça.

A avaliação deste script é exploratória e não substitui validação biométrica
formal com APCER/BPCER.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import cv2
import face_recognition
import numpy as np

from utils import DATA_DIR, extrair_nome_pessoa, listar_imagens

CAMINHO_IMAGENS = DATA_DIR / "imagens_conhecidas"

LIMITE_EAR = 0.22
LIMITE_MAR = 0.25
LIMITE_TEMPO = 250


def calcular_ear(olho):
    a = math.dist(olho[1], olho[5])
    b = math.dist(olho[2], olho[4])
    c = math.dist(olho[0], olho[3])
    if c == 0:
        return 0.0
    return (a + b) / (2.0 * c)


def calcular_mar(landmarks):
    if "top_lip" not in landmarks or "bottom_lip" not in landmarks:
        return 0.0
    altura_interna_boca = math.dist(landmarks["top_lip"][9], landmarks["bottom_lip"][9])
    largura_boca = math.dist(landmarks["top_lip"][0], landmarks["top_lip"][6])
    if largura_boca == 0:
        return 0.0
    return altura_interna_boca / largura_boca


def calcular_rotacao_3d(landmarks):
    nariz = landmarks["nose_bridge"][-1]
    maxilar_esq = landmarks["chin"][0]
    maxilar_dir = landmarks["chin"][-1]
    dist_esq = math.dist(nariz, maxilar_esq)
    dist_dir = math.dist(nariz, maxilar_dir)
    if dist_dir == 0:
        return 1.0
    return dist_esq / dist_dir


def rosto_frontal(razao):
    return 0.85 <= razao <= 1.15


def rosto_virado_direita(razao):
    return razao < 0.65


def rosto_virado_esquerda(razao):
    return razao > 1.5


def carregar_base():
    codificacoes_conhecidas = []
    nomes_conhecidos = []

    if not CAMINHO_IMAGENS.exists():
        raise FileNotFoundError(f"A pasta '{CAMINHO_IMAGENS}' não foi encontrada.")

    print("Carregando imagens conhecidas...")
    for caminho in listar_imagens(CAMINHO_IMAGENS):
        try:
            imagem = face_recognition.load_image_file(str(caminho))
            codificacoes = face_recognition.face_encodings(imagem)
            if codificacoes:
                codificacoes_conhecidas.append(codificacoes[0])
                nomes_conhecidos.append(extrair_nome_pessoa(caminho.name))
                print(f"[OK] {caminho.name}")
            else:
                print(f"[AVISO] Nenhum rosto detectado em {caminho.name}")
        except Exception as exc:
            print(f"[AVISO] Erro ao carregar {caminho.name}: {exc}")

    if not codificacoes_conhecidas:
        raise RuntimeError("Nenhuma imagem válida foi carregada em data/imagens_conhecidas.")

    return codificacoes_conhecidas, nomes_conhecidos


def main():
    try:
        codificacoes_conhecidas, nomes_conhecidos = carregar_base()
    except Exception as exc:
        print(f"Erro: {exc}")
        return

    estado_atual = "AGUARDANDO_FRONTAL"
    desafios_pendentes = []
    indice_desafio_atual = 0
    olhos_fechados = False
    boca_estava_fechada = False
    frames_no_estado = 0
    frames_sem_rosto = 0
    nome_reconhecido = None

    cap = cv2.VideoCapture(0)
    print("\nIniciando sistema de biometria antifraude. Pressione 'q' para sair.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        altura_frame, largura_frame = frame.shape[:2]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pequeno = cv2.resize(frame_rgb, (0, 0), None, 0.25, 0.25)

        locais_rostos = face_recognition.face_locations(frame_pequeno)
        landmarks_lista = face_recognition.face_landmarks(frame_pequeno, locais_rostos)

        if not locais_rostos:
            frames_sem_rosto += 1
            if frames_sem_rosto > 10:
                estado_atual = "AGUARDANDO_FRONTAL"
                desafios_pendentes = []
                indice_desafio_atual = 0
                frames_no_estado = 0
                olhos_fechados = False
                boca_estava_fechada = False
                nome_reconhecido = None
        else:
            frames_sem_rosto = 0

        for local_rosto, landmarks in zip(locais_rostos, landmarks_lista):
            y1_orig, x2_orig, y2_orig, x1_orig = [coord * 4 for coord in local_rosto]

            padding_lateral = 30
            padding_topo = 50
            padding_base = 30

            x1 = max(0, x1_orig - padding_lateral)
            y1 = max(0, y1_orig - padding_topo)
            x2 = min(largura_frame, x2_orig + padding_lateral)
            y2 = min(altura_frame, y2_orig + padding_base)

            cor = (0, 0, 255)
            texto_exibicao = "ANALISANDO\nROSTO..."

            if nome_reconhecido is None:
                try:
                    codificacao_rosto = face_recognition.face_encodings(frame_pequeno, [local_rosto])[0]
                    matches = face_recognition.compare_faces(
                        codificacoes_conhecidas, codificacao_rosto, tolerance=0.5
                    )
                    distancia_facial = face_recognition.face_distance(
                        codificacoes_conhecidas, codificacao_rosto
                    )
                    if True in matches:
                        indice = int(np.argmin(distancia_facial))
                        if matches[indice]:
                            nome_reconhecido = nomes_conhecidos[indice].upper()
                except Exception:
                    pass

            if nome_reconhecido is not None:
                nome = nome_reconhecido
                frames_no_estado += 1

                razao_rosto = calcular_rotacao_3d(landmarks)
                ear_medio = 1.0
                if "left_eye" in landmarks and "right_eye" in landmarks:
                    ear_medio = (calcular_ear(landmarks["left_eye"]) + calcular_ear(landmarks["right_eye"])) / 2.0
                mar_atual = calcular_mar(landmarks)

                if estado_atual == "AGUARDANDO_FRONTAL":
                    texto_exibicao = f"{nome}\nOLHE RETO PARA\nA CAMERA"
                    cor = (255, 255, 0)

                    if rosto_frontal(razao_rosto):
                        todas_instrucoes = ["PISCAR", "VIRAR_DIREITA", "VIRAR_ESQUERDA", "ABRIR_BOCA"]
                        desafios_pendentes = [random.choice(todas_instrucoes)]
                        while len(desafios_pendentes) < 5:
                            nova_instrucao = random.choice(todas_instrucoes)
                            if nova_instrucao != desafios_pendentes[-1]:
                                desafios_pendentes.append(nova_instrucao)

                        estado_atual = "EXECUTANDO_DESAFIOS"
                        indice_desafio_atual = 0
                        frames_no_estado = 0

                elif estado_atual == "EXECUTANDO_DESAFIOS":
                    if frames_no_estado > LIMITE_TEMPO:
                        estado_atual = "FRAUDE"
                    else:
                        desafio_ativo = desafios_pendentes[indice_desafio_atual]
                        passou_desafio = False

                        if desafio_ativo == "PISCAR":
                            texto_exibicao = f"{nome}\nPISQUE [{indice_desafio_atual + 1}/5]"
                            if ear_medio < LIMITE_EAR:
                                olhos_fechados = True
                            elif ear_medio >= LIMITE_EAR and olhos_fechados:
                                passou_desafio = True
                                olhos_fechados = False

                        elif desafio_ativo == "VIRAR_DIREITA":
                            texto_exibicao = f"{nome}\nVIRE PARA A\nDIREITA [{indice_desafio_atual + 1}/5]"
                            if rosto_virado_direita(razao_rosto):
                                passou_desafio = True

                        elif desafio_ativo == "VIRAR_ESQUERDA":
                            texto_exibicao = f"{nome}\nVIRE PARA A\nESQUERDA [{indice_desafio_atual + 1}/5]"
                            if rosto_virado_esquerda(razao_rosto):
                                passou_desafio = True

                        elif desafio_ativo == "ABRIR_BOCA":
                            texto_exibicao = f"{nome}\nABRA A BOCA [{indice_desafio_atual + 1}/5]"
                            if mar_atual < 0.10:
                                boca_estava_fechada = True
                            elif mar_atual > LIMITE_MAR and boca_estava_fechada:
                                passou_desafio = True
                                boca_estava_fechada = False

                        cor = (0, 165, 255)

                        if passou_desafio:
                            indice_desafio_atual += 1
                            frames_no_estado = 0
                            if indice_desafio_atual >= len(desafios_pendentes):
                                estado_atual = "VALIDADO"

                elif estado_atual == "VALIDADO":
                    texto_exibicao = f"ACESSO LIBERADO:\n{nome}"
                    cor = (0, 255, 0)

                elif estado_atual == "FRAUDE":
                    texto_exibicao = "FRAUDE BLOQUEADA\n(FOTO/VIDEO)"
                    cor = (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
            linhas_texto = texto_exibicao.split("\n")
            altura_linha = 25
            altura_total_fundo = (len(linhas_texto) * altura_linha) + 10
            largura_fundo_minima = max(x2, x1 + 250)
            cv2.rectangle(frame, (x1, y2), (largura_fundo_minima, y2 + altura_total_fundo), cor, cv2.FILLED)
            cor_fonte = (0, 0, 0) if cor == (255, 255, 0) else (255, 255, 255)

            for i, linha in enumerate(linhas_texto):
                pos_y = y2 + 22 + (i * altura_linha)
                cv2.putText(frame, linha, (x1 + 5, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, cor_fonte, 2)

        cv2.imshow("Biometria Antifraude", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
