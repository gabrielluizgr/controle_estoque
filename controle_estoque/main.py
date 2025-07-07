import tkinter as tk # Importando o tkinter, para criação das telas "as tk" é só um apelido, ao invés de escrever tkinter.Button, escreve tk.Button
from tkinter import messagebox # Do tkinter, importe a messagebox, que é basicamente um popup
from database import criar_tabela # Importar módulo da criação do banco de dados
import sqlite3 # Importando banco de dados
from funcoes.cadastrar import cadastrar_produtos_gui
from funcoes.listar import listar_produtos_gui
from funcoes.atualizar import atualizar_produtos_gui
from funcoes.remover import remover_produtos_gui

def abrir_janela(): # Função para criação da janela principal dos sistema
    janela = tk.Tk() # Cria a janela principal da aplicação. É tipo o formulário principal do programa
    janela.title("Controle de Estoque") # Coloca um título na janela
    janela.geometry("400x300") # Define o tamanho da janela, no caso 400x300

    # Título
    titulo = tk.Label(janela, text="Controle de Estoque", font=("Arial", 16, "bold")) # Criação de uma etiqueta de texto, com o nome do sistema
    titulo.pack(pady=10) # "Empacota" o item na tela e dá um espaço vertical de 10 pixels

    # Botões do menu
    btn_cadastrar = tk.Button(janela, text="Cadastrar Produto", width=30, command=lambda: cadastrar_produtos_gui(janela)) # Cria um botão com o texto cadastrar produto, width é sua largura e o command é o que vai acontecer depois, atualmente, o que acontece é uma caixinha informando que ainda será implementado. A mesma coisa vale para todos os botões
    btn_listar = tk.Button(janela, text="Listar Produtos", width=30, command=lambda: listar_produtos_gui(janela))
    btn_atualizar = tk.Button(janela,text="Atualizar Produto", width=30, command=lambda: atualizar_produtos_gui(janela))
    btn_remover = tk.Button(janela, text="Remover Produto", width=30, command=lambda: remover_produtos_gui(janela))
    btn_sair = tk.Button(janela, text="Sair", width=30, command=janela.quit)

    btn_cadastrar.pack(pady=5) # Colocando os botões na tela. Pack é o que posiciona o botão na janela, Pady dá um espaço vertical entre os botões
    btn_listar.pack(pady=5)
    btn_atualizar.pack(pady=5)
    btn_remover.pack(pady=5)
    btn_sair.pack(pady=20)

    janela.mainloop() # Esse comando mantém a janela aberta, esperando que o usuário clique em algum botão. Sem isso, a janela abriria e fecharia em 0.00001 segundos

if __name__ == "__main__":
    try:
        criar_tabela()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao criar o banco de dados: {e}")
    abrir_janela()