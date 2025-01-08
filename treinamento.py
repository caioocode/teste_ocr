import os
import pytesseract
from tkinter import Tk, filedialog, messagebox, Button
from PIL import Image
import ocr_training

# Configure o caminho para o executável do Tesseract (ajuste conforme seu sistema)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\CaioAlbuquerqueQuali\OneDrive - Qualita Granitos e Marmores LTDA\Área de Trabalho\teste_ocr\tesseract\tesseract.exe"

import os
import subprocess

def preparar_imagens_e_transcricoes(diretorio_imagens, diretorio_transcricoes):
    """
    Prepara o diretório de imagens e transcrições para o treinamento do Tesseract.

    Args:
        diretorio_imagens (str): Caminho para o diretório de imagens.
        diretorio_transcricoes (str): Caminho para o diretório de transcrições.
    """
    if not os.path.exists(diretorio_imagens):
        print(f"Erro: O diretório {diretorio_imagens} não existe!")
        return False
    if not os.path.exists(diretorio_transcricoes):
        print(f"Erro: O diretório {diretorio_transcricoes} não existe!")
        return False
    return True

def treinar_modelo(diretorio_imagens, diretorio_transcricoes, diretorio_modelo_saida, idioma="por"):
    """
    Treina o modelo Tesseract com as imagens e transcrições fornecidas.

    Args:
        diretorio_imagens (str): Caminho para o diretório de imagens.
        diretorio_transcricoes (str): Caminho para o diretório de transcrições.
        diretorio_modelo_saida (str): Caminho para salvar o modelo treinado.
        idioma (str): Idioma do treinamento (padrão "por").
    """
    if not preparar_imagens_e_transcricoes(diretorio_imagens, diretorio_transcricoes):
        return
    
    # Passo 1: Criação do arquivo de treinamento .box (usando o Tesseract)
    print("Gerando arquivos .box a partir das imagens...")
    for imagem in os.listdir(diretorio_imagens):
        if imagem.endswith(".jpg") or imagem.endswith(".png"):
            imagem_path = os.path.join(diretorio_imagens, imagem)
            nome_base = os.path.splitext(imagem)[0]
            transcricao_path = os.path.join(diretorio_transcricoes, f"{nome_base}.txt")
            
            # Usar o Tesseract para gerar o arquivo .box
            comando_tesseract = [
                "tesseract", imagem_path, nome_base, "-c", "tessedit_create_boxfiles=1", f"-l {idioma}"
            ]
            subprocess.run(comando_tesseract)
    
    # Passo 2: Treinamento do modelo (treinando o modelo LSTM)
    print("Iniciando o treinamento do modelo...")
    comando_tesseract_train = [
        "tesseract", "--train", diretorio_imagens, diretorio_transcricoes, "-l", idioma, 
        f"--model-output={diretorio_modelo_saida}"
    ]
    subprocess.run(comando_tesseract_train)
    print("Treinamento concluído. Modelo salvo em:", diretorio_modelo_saida)

if __name__ == "__main__":
    # Caminhos dos diretórios
    diretorio_imagens = "caminho/para/imagens_de_treino"
    diretorio_transcricoes = "caminho/para/transcricoes"
    diretorio_modelo_saida = "caminho/para/modelo_saida"
    
    # Treinamento
    treinar_modelo(diretorio_imagens, diretorio_transcricoes, diretorio_modelo_saida)
