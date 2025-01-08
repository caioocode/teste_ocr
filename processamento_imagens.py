import pytesseract
from PIL import Image, ImageEnhance
import re
import cv2 
import numpy as np
import os

# Configure o caminho para o executável do Tesseract (ajuste conforme seu sistema)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\CaioAlbuquerqueQuali\OneDrive - Qualita Granitos e Marmores LTDA\Área de Trabalho\teste_ocr\tesseract\tesseract.exe"

def extrair_informacoes_chapas(imagem_chapas):
    """
    Extrai o número do lote de uma imagem.

    Args:
        imagem_chapas (str): Caminho para a imagem contendo as chapas.

    Returns:
        str: Número do lote (str).
    """
    texto = pytesseract.image_to_string(Image.open(imagem_chapas), lang="por")

    # Extrair o número do lote (padrão: 007621)
    padrao_lote = r"\b\d{6}\b"
    numero_lote = re.search(padrao_lote, texto)

    if numero_lote:
        return numero_lote.group()
    return None

def extrair_numero_bundle(imagem_bundle, lote):
    """
    Extrai o número do bundle (044xxx) associado ao lote da imagem.

    Args:
        imagem_bundle (str): Caminho para a imagem contendo os bundles.
        lote (str): Número do lote para buscar na imagem.

    Returns:
        str: Número do bundle correspondente (044xxx).
    """
    texto = pytesseract.image_to_string(Image.open(imagem_bundle), lang="eng")

    # Procurar o número do bundle associado ao lote
    padrao_bundle = fr"(044\d{{3}})\s\|\s{lote}"
    match = re.search(padrao_bundle, texto)

    if match:
        return match.group(1)
    return None

def renomear_imagem(imagem_chapas, bundle, pasta_destino):
    """
    Renomeia a imagem com base no número do bundle.

    Args:
        imagem_chapas (str): Caminho para a imagem contendo as chapas.
        bundle (str): Número do bundle (044xxx).
        pasta_destino (str): Caminho da pasta para salvar as imagens renomeadas.
    """
    novo_nome = f"{bundle}.jpg"
    caminho_novo = os.path.join(pasta_destino, novo_nome)

    # Salvar a imagem com o novo nome
    os.rename(imagem_chapas, caminho_novo)
    return caminho_novo
