# main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from processamento_imagens import extrair_informacoes_chapas, extrair_numero_bundle, renomear_imagem

def selecionar_imagem_chapas():
    """
    Abre um diálogo para o usuário selecionar a imagem das chapas.
    """
    arquivo = filedialog.askopenfilename(title="Selecionar Imagem das Chapas", filetypes=[("Imagem JPG", "*.jpg"), ("Imagem PNG", "*.png")])
    if arquivo:
        entry_imagem_chapas.delete(0, tk.END)
        entry_imagem_chapas.insert(0, arquivo)

def selecionar_imagem_bundle():
    """
    Abre um diálogo para o usuário selecionar a imagem do bundle.
    """
    arquivo = filedialog.askopenfilename(title="Selecionar imagem do Bundle")
    if arquivo:
        entry_imagem_bundle.delete(0, tk.END)
        entry_imagem_bundle.insert(0, arquivo)

def selecionar_pasta_destino():
    """
    Abre um diálogo para o usuário selecionar a pasta de destino.
    """
    pasta = filedialog.askdirectory(title="Selecionar Pasta de Destino")
    if pasta:
        entry_pasta_destino.delete(0, tk.END)
        entry_pasta_destino.insert(0, pasta)

def processar_imagens():
    """
    Realiza o processo de extração e renomeação de imagens com base nos arquivos selecionados.
    """
    imagem_chapas = entry_imagem_chapas.get()
    imagem_bundle = entry_imagem_bundle.get()
    pasta_destino = entry_pasta_destino.get()

    # Verificar se todos os campos estão preenchidos
    if not imagem_chapas or not imagem_bundle or not pasta_destino:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

        # Iniciar a barra de progresso
    progress_var.set(0)
    progress_bar.start()


    # Extrair o número do lote da imagem das chapas
    numero_lote = extrair_informacoes_chapas(imagem_chapas)
    if not numero_lote:
        progress_bar.stop()
        messagebox.showerror("Erro", "Não foi possível extrair o número do lote da imagem das chapas.")
        return

    # Extrair o número do bundle com base no número do lote
    numero_bundle = extrair_numero_bundle(imagem_bundle, numero_lote)
    if not numero_bundle:
        progress_bar.stop()
        messagebox.showerror("Erro", "Não foi possível encontrar o número do bundle associado ao lote.")
        return

    # Renomear a imagem das chapas
    novo_caminho = renomear_imagem(imagem_chapas, numero_bundle, pasta_destino)
    progress_bar.stop()
    messagebox.showinfo("Sucesso", f"A imagem foi renomeada e movida para: {novo_caminho}")

# Interface gráfica
root = tk.Tk()
root.title("Processador de Imagens")

# Layout
tk.Label(root, text="Imagem das Chapas").grid(row=0, column=0, padx=10, pady=5)
entry_imagem_chapas = tk.Entry(root, width=40)
entry_imagem_chapas.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=selecionar_imagem_chapas).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Imagem do Bundle").grid(row=1, column=0, padx=10, pady=5)
entry_imagem_bundle = tk.Entry(root, width=40)
entry_imagem_bundle.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=selecionar_imagem_bundle).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Pasta de Destino").grid(row=2, column=0, padx=10, pady=5)
entry_pasta_destino = tk.Entry(root, width=40)
entry_pasta_destino.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=selecionar_pasta_destino).grid(row=2, column=2, padx=10, pady=5)

# Barra de progresso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300, mode='indeterminate')
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

tk.Button(root, text="Processar Imagens", command=processar_imagens).grid(row=4, column=0, columnspan=3, pady=10)

# Ajustar a largura das colunas para evitar sobreposição
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(2, weight=1)


root.mainloop()
