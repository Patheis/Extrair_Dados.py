import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
import os
import re

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho_arquivo:
        nome_arquivo.set(os.path.basename(caminho_arquivo))
        caminho_arquivo_selecionado.set(caminho_arquivo)

def extrair_informacoes():
    caminho = caminho_arquivo_selecionado.get()
    if not caminho:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado!")
        return

    try:
        # Usando PyPDF2 para abrir e ler o PDF
        leitor = PdfReader(caminho)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text()  # Extração do texto de todas as páginas

        # Verifica se o texto foi extraído corretamente
        if not texto:
            messagebox.showerror("Erro", "Não foi possível extrair texto do PDF!")
            return

        # Inicializando o dicionário de dados
        dados = {
            "CNPJ": obter_dado_regex(texto, r"CNPJ[:\s]*([\d]{2}\.[\d]{3}\.[\d]{3}/[\d]{4}-[\d]{2})"),
            "VALOR TOTAL DA NOTA": obter_dado_regex(texto, r"VALOR TOTAL DA NOTA[\s\S]*?R\$\s*([\d\.,]+)"),
            "ISS": obter_dado_regex(texto, r"ISS[\s\S]*?R\$\s*([\d\.,]+)"),
            "PIS": obter_dado_regex(texto, r"PIS[\s\S]*?R\$\s*([\d\.,]+)"),
            "COFINS": obter_dado_regex(texto, r"COFINS[\s\S]*?R\$\s*([\d\.,]+)"),
            "NUMERO DA NOTA": obter_dado_regex(texto, r"Nota nº:\s*(\d+)"),
            "Data e Hora de Emissão": obter_dado_regex(texto, r"Data e Hora de Emissão:\s*(\d{2}/\d{2}/\d{4})"),
            "BANCO": obter_dado_regex(texto, r"Banco:\s*(\w+.*)"),
            "VENCIMENTO DA NOTA": obter_dado_regex(texto, r"Vencimento:\s*(\d{2}/\d{2}/\d{4})")
        }

        # Salvando os dados extraídos em um arquivo .txt
        with open("dados_nota_fiscal.txt", "w") as arquivo:
            for chave, valor in dados.items():
                arquivo.write(f"{chave}: {valor}\n")

        messagebox.showinfo("Sucesso", "Informações extraídas e salvas em 'dados_nota_fiscal.txt'!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo: {e}")

def obter_dado_regex(texto, padrao):
    """Utiliza expressões regulares para encontrar os dados no texto. Retorna '0' ou 'NULL' se não encontrar."""
    resultado = re.search(padrao, texto)
    if resultado:
        return resultado.group(1)  # Retorna o valor encontrado
    else:
        return '0'  # Retorna '0' se não encontrar

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Importador de Nota Fiscal")
janela.geometry("400x300")
janela.configure(bg="#3f3f3f")

caminho_arquivo_selecionado = tk.StringVar()
nome_arquivo = tk.StringVar()

# Frame principal
frame = tk.Frame(janela, bg="#d3d3d3", width=300, height=100)
frame.place(relx=0.5, rely=0.3, anchor="center")

# Botão para selecionar arquivo
botao_selecionar = tk.Button(
    frame,
    text="IMPORTAR NOTA-FISCAL",
    command=selecionar_arquivo,
    bg="#d3d3d3",
    fg="gray",
    relief="flat",
    font=("Arial", 10)
)
botao_selecionar.place(relx=0.5, rely=0.5, anchor="center")

# Label para exibir o nome do arquivo selecionado
label_arquivo = tk.Label(janela, textvariable=nome_arquivo, bg="#3f3f3f", fg="white", font=("Arial", 10))
label_arquivo.pack(pady=150)

# Botão para trazer informações
botao_processar = tk.Button(
    janela,
    text="TRAZER INFORMAÇÕES",
    command=extrair_informacoes,
    bg="#0a3d62",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    width=20
)
botao_processar.pack(pady=120)

janela.mainloop()
