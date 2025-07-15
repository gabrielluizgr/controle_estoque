import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import remover_produto_id
from database import busca_produto_id

def remover_produtos(): # Criação de uma função para remover produtos
    try: # Tratamento de exceções
        id_produto = int(input("Informe o ID do produto que deseja remover: "))
    except ValueError: # Se o que foi informado pelo usuário não foi um número, a função encerra
        print("ID inválido. Use apenas números")
        return # Retorno None
    conexao = None # Iniciando para usar no finally
    try:
        conexao = sqlite3.connect("estoque.db") # Conexão com o banco
        cursor = conexao.cursor() # Abertura do cursor

        cursor.execute("SELECT * FROM produtos WHERE id = ?" , (id_produto,)) # Selecionando o produto que tem o id informado pelo usuário
        produto = cursor.fetchone() # Armazenando na tupla

        if produto:
            id, nome, marca, quantidade, preco = produto # Desempacotando...
            print(f"\nProduto encontrado\n") # Mostrando ao usuário o produto coletado...
            print(f"Nome: {nome}")
            print(f"Marca: {marca}")
            print(f"Quantidade: {quantidade}")
            print(f"Preço: {preco:.2f}")

            confirmacao = input("Tem certeza que deseja remover esse produto? (s/n) ").strip().lower() # Confirmação
            if confirmacao == 's':
                cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,)) # Usando o cursor para deletar da tabela produtos o produto com o id correspondente
                conexao.commit() # Salvando a alteração no banco
                print("Produto removido com sucesso.")
            else:
                print("Remoção cancelada.")
        else:
            print("Produto não encontrado.")
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        if conexao:
            conexao.close() # Fechando conexão
            print("\nVoltando ao menu principal...\n")

def remover_produtos_gui(janela_principal): # Criação de uma nova função que será chamada quando o usuário clicar no botão Remover Produto
    janela_deletar = tk.Toplevel() # Cria uma nova janela filha 
    janela_deletar.title("Remover Produto") # Título da janela
    janela_deletar.geometry("300x200") # Tamanho da janela

    # Campo para inserção do id
    tk.Label(janela_deletar, text="ID do Produto a ser Removido:").pack(pady=10) 
    entry_id = tk.Entry(janela_deletar) # Campo onde o usuário irá digitar o número do ID
    entry_id.pack()

    def deletar(): # Define a função interna deletar, que será chamada quando o botão for clicado
        try:
            id_produto = int(entry_id.get()) # Converte a entrada do id para inteiro
            produto = busca_produto_id(id_produto)

            if not produto:
                messagebox.showwarning("Aviso", "Produto não encontrado.")
                return
            confirmar = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o produto '{produto[1]}'?'") # Abre uma caixa de confirmação (Yes/No) perguntando se o usuário realmente quer a exclusão. produto[1] é o índice da tupla onde fica o nome do produto. Se clicar em Não, a função encerra
            if not confirmar:
                return
            linhas_afetadas = remover_produto_id(id_produto)
            if linhas_afetadas == 0:
                messagebox.showwarning("Aviso", "Produto não encontrado.")
            else:
                messagebox.showinfo("Sucesso!", "Produto excluído com sucesso.")
                janela_deletar.destroy()

        except ValueError: # Tratamento de erros
            messagebox.showerror("Erro", "Insira um ID válido.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))    
    # Área dos botões
    frame_botoes = tk.Frame(janela_deletar)
    frame_botoes.pack(pady=20)
    # Criação de um frame(caixa interna), para organizar os dois botões horizontalmente, com espaço vertical entre os campos e os botões
    btn_deletar = tk.Button(frame_botoes, text="Deletar", command=deletar, bg="red", fg="white")
    btn_deletar.grid(row=0, column=0, padx=10)
    # Criação de um botão chamado deletar, quando clicado, chama a função criada anteriormente, usa grid para alinhamento e a cor de fundo é vermelha para dar destaque
    btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=janela_deletar.destroy, bg="gray", fg="white")
    btn_cancelar.grid(row=0, column=1, padx=10)
    # Criação de outro botão chamado cancelar, quando clicado, chama a função destroy (fecha a janela)