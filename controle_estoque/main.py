# Importando o tkinter, para criação das telas "as tk" é só um apelido, ao invés de escrever tkinter.Button, escreve tk.Button
import tkinter as tk
# Do tkinter, importe a messagebox, que é basicamente uma função de popup
from tkinter import messagebox
from tkinter import PhotoImage
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
    janela.geometry("400x400") # Define o tamanho da janela, no caso 400x300

    icone_cadastrar = tk.PhotoImage(file="controle_estoque/icons/icone_add.png")
    icone_remover = tk.PhotoImage(file="controle_estoque/icons/icone_remove.png")
    icone_atualizar = tk.PhotoImage(file="controle_estoque/icons/icone_att.png")
    icone_listar = tk.PhotoImage(file="controle_estoque/icons/icone_list.png")
    icone_sair = tk.PhotoImage(file="controle_estoque/icons/icone_quit.png")

    # Título da janela principal
    titulo = tk.Label(janela, text="Controle de Estoque", font=("Segoe UI", 16, "bold"), bg="#f0f0f0") # Criação de uma etiqueta de texto
    titulo.pack(pady=(30, 20)) # Mostra o item na tela (pack) e dá um espaço vertical de 10px

    frame_botoes = tk.Frame(janela, bg="#f0f0f0")
    frame_botoes.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def criar_botao(texto, comando, icone = None, cor="#191970"):
        btn = tk.Button(
            frame_botoes,
            text=texto,
            command=comando,
            bg=cor,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            height=20,
            width=300,
            compound="left"
        )
        if icone:
            btn.config(image=icone)
            btn.image = icone
        return btn
    
    botoes = [
        ("Cadastrar Produto", lambda: cadastrar_produtos_gui(janela), icone_cadastrar),
        ("Listar Produtos", lambda: listar_produtos_gui(janela), icone_listar),
        ("Atualizar Produto", lambda: atualizar_produtos_gui(janela), icone_atualizar),
        ("Remover Produto", lambda: remover_produtos_gui(janela), icone_remover),

    ]
    for texto, comando, icone in botoes:
        criar_botao(texto, comando, icone).pack(pady=10)

    btn_sair = tk.Button(
        frame_botoes,
        text="Sair",
        command=janela.quit,
        bg="#4F4F4F",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        height=20,
        width=300,
        compound="left",
        image=icone_sair
    )
    
    btn_sair.pack(pady=10)

    janela.mainloop() # Esse comando mantém a janela aberta, esperando que o usuário clique em algum botão. Sem isso, a janela abriria e fecharia em 0.00001 segundos

# Se o nome dessa aplicação for "main.py" e ela for executada diretamente, a função criar_tabela{} (função importada do módulo database) é chamada para garantir que a tabela exista antes de abrir a janela
if __name__ == "__main__":
    try:
        criar_tabela()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao criar o banco de dados: {e}")
    abrir_janela()