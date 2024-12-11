import pytesseract
from PIL import Image, ImageEnhance
import re
import cv2 
import numpy as np

# Configure o caminho para o executável do Tesseract (ajuste conforme seu sistema)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\CaioAlbuquerqueQuali\OneDrive - Qualita Granitos e Marmores LTDA\Área de Trabalho\teste_ocr\tesseract\tesseract.exe"

def testar_reconhecimento(caminho_imagem):
    """
    Testa o reconhecimento de texto em uma imagem e verifica o padrão do número do lote.
    
    Args:
        caminho_imagem (str): Caminho para a imagem a ser analisada.
    
    Returns:
        str: Resultado do reconhecimento de texto.
        list: Lista de padrões encontrados.
    """
    try:
        # Abre a imagem
        imagem = Image.open(caminho_imagem)
        
        # 1. Pré-processamento: Converter para escala de cinza
        img_gray = imagem.convert('L')  # Conversão para escala de cinza

        # 2. Aumento de contraste e brilho
        enhancer = ImageEnhance.Contrast(img_gray)
        img_contrast = enhancer.enhance(2)  # Aumentar o contraste (ajuste conforme necessário)

        img_np = np.array(img_contrast)  # Converte a imagem PIL para um array NumPy  
        _, img_binary = cv2.threshold(img_np, 128, 255, cv2.THRESH_BINARY)

        # 6. Configuração de OCR: Definir idioma e opções
        custom_config = r'--oem 1 --psm 12 -c tessedit_char_whitelist=0123456789/'

        # Realiza o OCR
        texto_extraido = pytesseract.image_to_string(img_binary, lang='por', config=custom_config)
        print(f"Texto extraído:\n{texto_extraido}")
        
        # Busca pelo padrão 00XXXX/YY usando regex
        padrao = r"00\d{4}/\d{3}"
        correspondencias = re.findall(padrao, texto_extraido)
        
        if correspondencias:
            print(f"Padrões encontrados: {correspondencias}")
        else:
            print("Nenhum padrão correspondente encontrado.")
        
        return texto_extraido, correspondencias
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None, []

# Teste com sua imagem
caminho_imagem = r"C:\Users\CaioAlbuquerqueQuali\OneDrive - Qualita Granitos e Marmores LTDA\Área de Trabalho\teste_ocr\img\img1.jpg" # Substitua pelo caminho real da imagem
texto, resultados = testar_reconhecimento(caminho_imagem)

if resultados:
    print("Reconhecimento bem-sucedido!")
else:
    print("O OCR não conseguiu identificar o padrão corretamente.")
