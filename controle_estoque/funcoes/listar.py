import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import lista_dos_produtos

def listar_produtos(): # Criação de uma função para listar os produtos do banco
    print("===== Lista de Produtos Cadastrados ======")
    conexao = None # Inicializa a variável para usar no finally
    try: # Tratamento de exceção
        conexao = sqlite3.connect("estoque.db") # Abre o arquivo "estoque.db"
        cursor = conexao.cursor() # "cursor" pode ser imaginado como uma caneta, que escreve ou lê coisas dentro do banco de dados

        cursor.execute("SELECT * FROM produtos")  # "cursor.execute" basicamente realiza uma ação no nosso banco de dados (cria tabela, insere, lê, remove, atualiza...). No caso, está selecionando
        produtos = cursor.fetchall() # "fetchall" retorna uma lista de tuplas, contendo todos os atributos da tabela, cada um em uma tupla

        if len(produtos) == 0: # Se o tamanho das tuplas retornadas for zero, quer dizer que não há produtos registrados no banco de dados
            print("Nenhum produto encontrado.")
        else: 
            for produto in produtos: # Se houverem produtos no banco, uma estrutura de repetição FOR percorre cada tupla dentro da lista produtos
                id, nome, marca, quantidade, preco = produto # Desempacotação da tupla -- Separa os dados para que fiquem em variáveis com nome legível
                print(f"ID: {id}")
                print(f"Nome: {nome}")
                print(f"Marca: {marca if marca else '-'}") # Se a marca não existir é substituída por "-"
                print(f"Quantidade: {quantidade}")
                print(f"Preço: R$ {preco:.2f}")
                print("-" * 30)
    except sqlite3.Error as e: # Essa exceção captura os erros relacionados ao sqlite3
        print(f"Erro ao acessar o banco de dados: {e}")
    finally: # Se a variável conexão não for None, a conexão é encerrada
        if conexao:
            conexao.close() # Fecha a conexão    

def listar_produtos_gui(janela_principal):  
    janela_listagem = tk.Toplevel()
    janela_listagem.title("Lista de Produtos")
    janela_listagem.geometry("950x650")
    janela_listagem.configure(bg="#f0f0f0")

    tk.Label(
        janela_listagem,
        text="Produtos Cadastrados",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(pady=(20, 10))

    # Frame de pesquisa
    frame_pesquisa = tk.Frame(janela_listagem, bg="#f0f0f0")
    frame_pesquisa.pack(fill=tk.X, padx=20, pady=(0,10))

    tk.Label(frame_pesquisa, text="Pesquisar:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    entrada_pesquisa = tk.Entry(frame_pesquisa, width=40)
    entrada_pesquisa.pack(side=tk.LEFT, padx=5)

    btn_pesquisar = tk.Button(
        frame_pesquisa, text="Pesquisar",
        command=lambda: carregar_dados(entrada_pesquisa.get().strip()),
        bg="blue", fg="white",
        font=("Segoe UI", 10, "bold"),
        width=12
    )
    btn_pesquisar.pack(side=tk.LEFT, padx=5)

    # Frame da tabela
    frame = tk.Frame(janela_listagem, bg="#f0f0f0")
    frame.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

    colunas = ("ID", "Nome", "Marca", "Descrição", "Quantidade", "Preço")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=20)

    for col in colunas:
        tree.heading(col, text=col, command=lambda c=col: ordenar(tree, c, False))
        tree.column(col, width=120, anchor=tk.CENTER)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def carregar_dados(filtro=""):
        """Carrega produtos do banco, com filtro opcional"""
        for item in tree.get_children():
            tree.delete(item)

        sucesso, resultado = lista_dos_produtos()
        if sucesso:
            produtos = resultado
            if produtos:
                for id, nome, marca, descricao, quantidade, preco in produtos:
                    if filtro.lower() in nome.lower() or filtro.lower() in marca.lower():
                        marca = marca.strip() if marca else "Sem marca"
                        descricao = descricao.strip() if descricao else "Sem descrição"
                        preco_formatado = f"R$ {preco:.2f}".replace('.', ',')
                        tree.insert("", tk.END, values=(id, nome, marca, descricao, quantidade, preco_formatado))
            else:
                messagebox.showinfo("Info", "Nenhum produto cadastrado.")
        else:
            messagebox.showerror("Erro", f"Erro ao acessar o banco: {resultado}")

    # Frame de botões inferior
    frame_botoes = tk.Frame(janela_listagem, bg="#f0f0f0")
    frame_botoes.pack(pady=10)

    btn_atualizar = tk.Button(
        frame_botoes, text="Atualizar Página",
        command=lambda: carregar_dados(),
        bg="green", fg="white",
        font=("Segoe UI", 10, "bold"),
        width=15
    )
    btn_atualizar.pack(side=tk.LEFT, padx=10)

    btn_fechar = tk.Button(
        frame_botoes, text="Fechar",
        command=janela_listagem.destroy,
        bg="red", fg="white",
        font=("Segoe UI", 10, "bold"),
        width=12
    )
    btn_fechar.pack(side=tk.LEFT, padx=10)

    # Carregar dados iniciais
    carregar_dados()



def ordenar(tree, coluna, reverso):
    """Função para ordenar colunas ao clicar no cabeçalho"""
    dados = [(tree.set(item, coluna), item) for item in tree.get_children("")]

    try:
        dados.sort(key=lambda x: float(x[0].replace("R$ ", "").replace(",", ".")), reverse=reverso)
    except ValueError:
        dados.sort(key=lambda x: x[0], reverse=reverso)

    for index, (val, item) in enumerate(dados):
        tree.move(item, "", index)

    tree.heading(coluna, command=lambda: ordenar(tree, coluna, not reverso))
