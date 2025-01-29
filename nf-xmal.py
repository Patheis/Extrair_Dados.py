import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import os
from datetime import datetime

# Função para selecionar o arquivo XML
def selecionar_arquivo():
    """Função para selecionar o arquivo XML."""
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
    if caminho_arquivo:
        nome_arquivo.set(os.path.basename(caminho_arquivo))
        caminho_arquivo_selecionado.set(caminho_arquivo)

# Função para extrair os dados do XML
def extrair_dados():
    """Função para extrair dados específicos do XML e exibir no terminal."""
    caminho = caminho_arquivo_selecionado.get()
    if not caminho:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado!")
        return

    try:
        # Carregar e analisar o arquivo XML
        tree = ET.parse(caminho)
        root = tree.getroot()

        # Definir o namespace a ser utilizado na busca
        namespaces = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # Extração dos dados com base nas tags fornecidas
        dados = {
            "Nome do Fornecedor": obter_dado_xml(root, namespaces, "emit", "xNome"),
            "Data de Emissão": obter_data_xml(root, namespaces, "ide", "dhEmi"),
            "Valor da Nota": obter_valor_da_nota(root, namespaces)
        }

        # Exibe os dados extraídos no terminal
        print("Dados Extraídos:")
        for chave, valor in dados.items():
            print(f"{chave}: {valor}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo: {e}")

# Função para extrair dados de uma tag do XML
def obter_dado_xml(root, namespaces, parent_tag, tag):
    """Função para extrair o dado de uma tag específica do XML dentro de um parent_tag."""
    # Buscando a tag com o namespace correto
    elemento = root.find(f".//nfe:{parent_tag}/nfe:{tag}", namespaces=namespaces)  
    if elemento is not None:
        return elemento.text.strip()  # Retorna o texto dentro da tag
    else:
        return '0'  # Retorna '0' se a tag não for encontrada

# Função para extrair o valor da nota (vNF)
def obter_valor_da_nota(root, namespaces):
    """Função para extrair o valor da nota (vNF)"""
    # A busca da tag vNF dentro de total/ICMSTot
    elemento = root.find(".//nfe:total/nfe:ICMSTot/nfe:vNF", namespaces=namespaces)
    if elemento is not None:
        return elemento.text.strip()  # Retorna o valor da nota
    else:
        return '0'  # Retorna '0' se não encontrar a tag

# Função para extrair e formatar a data da tag dhEmi
def obter_data_xml(root, namespaces, parent_tag, tag):
    """Função para extrair e formatar a data de emissão (dhEmi)."""
    elemento = root.find(f".//nfe:{parent_tag}/nfe:{tag}", namespaces=namespaces)  # Encontra a tag dhEmi
    if elemento is not None:
        # Exemplo: 2024-11-25T22:09:47-03:00, então extraímos a parte da data
        data_entrada = elemento.text.split("T")[0]
        # Converte para o formato brasileiro: dd/mm/yyyy
        try:
            data_formatada = datetime.strptime(data_entrada, "%Y-%m-%d").strftime("%d/%m/%Y")
            return data_formatada
        except ValueError:
            return 'Data inválida'  # Caso a data não seja válida
    else:
        return '0'  # Retorna '0' se a tag não for encontrada

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Extrair Dados do XML")
janela.geometry("500x400")
janela.configure(bg="#3f3f3f")

caminho_arquivo_selecionado = tk.StringVar()
nome_arquivo = tk.StringVar()

# Frame para a seleção de arquivos
frame_selecao = tk.Frame(janela, bg="#d3d3d3", width=300, height=100)
frame_selecao.place(relx=0.5, rely=0.2, anchor="center")

# Botão para selecionar o arquivo XML
botao_selecionar = tk.Button(
    frame_selecao,
    text="IMPORTAR XML",
    command=selecionar_arquivo,
    bg="#d3d3d3",
    fg="gray",
    relief="flat",
    font=("Arial", 10)
)
botao_selecionar.place(relx=0.5, rely=0.5, anchor="center")

# Label para exibir o nome do arquivo carregado
label_nome_arquivo = tk.Label(janela, textvariable=nome_arquivo, bg="#3f3f3f", fg="white", font=("Arial", 10))
label_nome_arquivo.pack(pady=120)

# Frame para os botões de ação
frame_botoes = tk.Frame(janela, bg="#d3d3d3", width=300, height=100)
frame_botoes.place(relx=0.5, rely=0.6, anchor="center")

# Botão para extrair os dados do arquivo XML
botao_extrair = tk.Button(
    frame_botoes,
    text="EXTRAIR DADOS",
    command=extrair_dados,
    bg="#0a3d62",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    width=20
)
botao_extrair.place(relx=0.5, rely=0.5, anchor="center")

janela.mainloop()
