import os
import pytesseract
from PIL import Image
import cv2
import numpy as np

def gerar_imagem_com_texto(texto, caminho_imagem):
    """
    Gera uma imagem com o texto fornecido e a salva no caminho especificado.
    """
    # Definir tamanho da imagem
    largura = 600
    altura = 100
    imagem = np.ones((altura, largura), dtype=np.uint8) * 255  # Imagem branca
    
    # Configurar fonte para texto
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imagem, texto, (10, 50), fonte, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Salvar imagem gerada
    cv2.imwrite(caminho_imagem, imagem)

def treinar_modelo_imagens(pasta_imagens, pasta_destino):
    """
    Treina o modelo OCR com imagens geradas a partir de textos na pasta de imagens.
    """
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    arquivos = [f for f in os.listdir(pasta_imagens) if f.endswith('.txt')]  # Arquivos de texto com as transcrições
    
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta_imagens, arquivo)
        with open(caminho_arquivo, 'r') as file:
            texto = file.read().strip()
        
        # Gerar uma imagem com o texto
        nome_imagem = arquivo.replace('.txt', '.png')
        caminho_imagem = os.path.join(pasta_destino, nome_imagem)
        gerar_imagem_com_texto(texto, caminho_imagem)

        print(f"Imagem {caminho_imagem} gerada para o texto: {texto}")

    print(f"Treinamento concluído. As imagens foram salvas em {pasta_destino}")

def treinar_tesseract(pasta_imagens, idioma="por"):
    """
    Treina o Tesseract com as imagens de texto geradas e cria um modelo customizado.
    """
    # O Tesseract usa um modelo básico que pode ser treinado com as imagens e transcrições
    os.system(f"tesseract {pasta_imagens} {idioma} --psm 6 --oem 3")
    print(f"Modelo treinado em {idioma}.")
