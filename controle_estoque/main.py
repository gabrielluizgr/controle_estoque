# Importando o tkinter, para criação das telas "as tk" é só um apelido, ao invés de escrever tkinter.Button, escreve tk.Button
import tkinter as tk
# Do tkinter, importe a messagebox, que é basicamente uma função de popup
from tkinter import messagebox
# Importando a criação da tabela do módulo database
from database import criar_tabela 
# Importando para o programa a biblioteca padrão do Python que lida com banco de dados SQLite
import sqlite3
# Importando as funções de cadastro, listagem, atualização e remoção de produtos
from funcoes.cadastrar import cadastrar_produtos_gui
from funcoes.listar import listar_produtos_gui
from funcoes.atualizar import atualizar_produtos_gui
from funcoes.remover import remover_produtos_gui

def abrir_janela(): # Função para criação da janela principal do sistema
    janela = tk.Tk() # Cria a janela principal da aplicação
    janela.title("Controle de Estoque") # Coloca um título na janela principal
    janela.geometry("400x300") # Define o tamanho da janela, no caso 400x300

    # Título da janela principal
    titulo = tk.Label(janela, text="Controle de Estoque", font=("Arial", 16, "bold")) # Criação de uma etiqueta de texto
    titulo.pack(pady=10) # Mostra o item na tela (pack) e dá um espaço vertical de 10px

    # Botões do menu
    # Cria um botão com o texto informado, width=30 é sua largura e o command é o que vai acontecer depois. A mesma coisa vale para todos os outros botões
    btn_cadastrar = tk.Button(janela, text="Cadastrar Produto", width=30, command=lambda: cadastrar_produtos_gui(janela)) 
    btn_listar = tk.Button(janela, text="Listar Produtos", width=30, command=lambda: listar_produtos_gui(janela))
    btn_atualizar = tk.Button(janela,text="Atualizar Produto", width=30, command=lambda: atualizar_produtos_gui(janela))
    btn_remover = tk.Button(janela, text="Remover Produto", width=30, command=lambda: remover_produtos_gui(janela))
    btn_sair = tk.Button(janela, text="Sair", width=30, command=janela.quit)
    # Colocando os botões para aparecerem na tela (pack), com um espaçamento vertical de 5px
    btn_cadastrar.pack(pady=5) 
    btn_listar.pack(pady=5)
    btn_atualizar.pack(pady=5)
    btn_remover.pack(pady=5)
    btn_sair.pack(pady=20)

    janela.mainloop() # Esse comando mantém a janela aberta, esperando que o usuário clique em algum botão. Sem isso, a janela abriria e fecharia em 0.00001 segundos

# Se o nome dessa aplicação for "main.py" e ela for executada diretamente, a função criar_tabela{} (função importada do módulo database) é chamada para garantir que a tabela exista antes de abrir a janela
if __name__ == "__main__":
    try:
        criar_tabela()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao criar o banco de dados: {e}")
    abrir_janela()