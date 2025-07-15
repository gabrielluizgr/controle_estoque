import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import cadastro_dos_produtos

def cadastrar_produtos(): # Criação de uma função para o cadastro de produtos no terminal
    print("===== Cadastro de Produto =====")
    while True:
        # Validação de nome
        nome = input("Nome do produto (Obrigatório): ").strip() # "strip" remove espaços antes e depois da palavra digitada (para evitar nome só com espaços)
        if nome: # Verifica se a string nome não está vazia (ou seja, se o usuário digitou algo)
            break # Se o nome for válido, sai do loop
        print("O nome do produto não pode ficar vazio. Por favor, digite um nome válido.") # Nome do produto, obrigatório pois é NOT NULL
    marca = input("Marca (Opcional): ").strip() # Nome da marca, opcional, pois não há NOT NULL
    while True:
        # Validação de quantidade
        try: # Tratamento de exceção
            quantidade = int(input("Quantidade em estoque: ")) # Quantidade, int, pois seu tipo no banco é INTEGER
            break # Caso a quantidade for um número inteiro, a estrutura para
        except ValueError: # Caso o valor inserido for outro sem ser inteiro, o loop continua
            print("Quantidade inválida. Por favor, digite um número inteiro.")
    while True:
        # Validação do preço
        try: # Tratamento de exceção
            preco = float(input("Preço do produto (Use ponto, ex: 49.90): ")) # Preço, float, pois seu tipo no banco é REAL
            break # Se o preço informado foi um valor válido, o loop encerra
        except ValueError: # Se for um valor diferente de float, o loop continua
            print("Preço inválido. Por favor, digite um número decimal válido, usando ponto.")
        
    conexao = None # Conexao = None antes do try para garantir que a variável existe no escopo
    try:
        conexao = sqlite3.connect("estoque.db") # Abre o arquivo "estoque.db"
        cursor = conexao.cursor() # "cursor" pode ser imaginado como uma caneta, que escreve ou lê coisas dentro do banco de dados

        cursor.execute("""
            INSERT INTO produtos (nome, marca, quantidade, preco)
            VALUES (?, ?, ?, ?)
        """, (nome, marca, quantidade, preco)) # "cursor.execute" basicamente realiza uma ação no nosso banco de dados (cria tabela, insere, lê, remove, atualiza...). No caso, está inserindo
        # VALUES(?, ?, ?, ?) se chama query parametrizada. Isso serve para proteger contra ataques e erros (como SQL Injection). Os ? são substituídos pelos valores entre parênteses, na ordem certa.
    
        conexao.commit() # Salva as alterações no banco
        print(f"\nProduto '{nome}' cadastrado com sucesso!\n") # \n basicamente é quebra de linha

    except sqlite3.Error as e: # Capturando a exceção de qualquer erro relacionado ao sqlite3
        print(f"Erro ao acessar o banco de dados: {e}")
    finally: # Finally serve para finalmente, após tudo, fechar a conexão com o banco
        if conexao:  # Só é chamada a conexao.close se conexao não for None (isso sinaliza que a conexão foi aberta com sucesso)
            conexao.close()

def cadastrar_produtos_gui(janela_principal): # Criação de uma nova função que será chamada quando o usuário clicar no botão Cadastrar Produto

    janela_cadastro = tk.Toplevel() # Cria uma janela filha dentro do programa principal, usamos toplevel() e não tk() porque essa janela é dependente da principal
    janela_cadastro.title("Cadastrar Produto") # Define o título que aparece na barra superior da janela filha
    janela_cadastro.geometry("400x400") # Define o tamanho da janela filha 400x400

    # Nome
    tk.Label(janela_cadastro, text="Nome (Obrigatório):").pack() # Cria um rótulo(texto) com "Nome:" dentro da janela, e o exibe (pack() significa "coloca na tela")
    entry_nome = tk.Entry(janela_cadastro) # Cria um campo de entrada de texto para o nome do produto, e o exibe. A variável entry_nome guarda esse campo, pra depois pegar o valor
    entry_nome.pack(pady=5)

    # Marca
    tk.Label(janela_cadastro, text="Marca (Opcional):").pack() # Padrão repetido
    entry_marca = tk.Entry(janela_cadastro)
    entry_marca.pack(pady=5)

    # Descrição
    tk.Label(janela_cadastro, text="Descrição (Opcional) (Sabor, Tamanho...):").pack() # Padrão repetido
    entry_descricao = tk.Entry(janela_cadastro)
    entry_descricao.pack(pady=5)

    # Quantidade
    tk.Label(janela_cadastro, text="Quantidade (Obrigatório):").pack() # Padrão repetido
    entry_quantidade = tk.Entry(janela_cadastro)
    entry_quantidade.pack(pady=5)

    # Preço
    tk.Label(janela_cadastro, text="Preço (Obrigatório):").pack() # Padrão repetido
    entry_preco = tk.Entry(janela_cadastro)
    entry_preco.pack(pady=5)

    def salvar(): # Criação da função interna que salva os dados no banco
        nome = entry_nome.get().strip() # Pega o valor digitado no campo de nome 
        if not nome: # O "strip()" remove espaços indesejados. Se o nome for None (não foi digitado pelo usuário), cai no showwarning e retorna None
            messagebox.showwarning("Aviso", "O nome do produto é obrigatório.")
            return

        marca = entry_marca.get().strip() or "Sem marca" # Pega o valor digitado no campo de nome, remove os espaços indesejados e caso não for informado, vira "Sem marca"
        descricao = entry_descricao.get().strip() or "Sem descrição" # Pega o valor digitado no campo sabor, remove os espaços indesejados e caso não for informado, vira "Sem sabor"

        try:
            quantidade = int(entry_quantidade.get()) # Pega o valor digitado no campo de quantidade, e o tenta converter para número int 
            if quantidade < 0:
                messagebox.showerror("Erro", "Quantidade não pode ser negativa.")
                return
        except ValueError: # Se o usuário digitar letra onde tem que ser número, a exceção é lançada, e a mensagem abaixo é posta na tela, também cancela o cadastro com o Return
            messagebox.showerror("Erro", "Quantidade deve ser número inteiro.")
            return
        
        try: # Validação do preço. Caso seja digitado ',' ao invés de '.', a ',' é substituída por'.'
            preco = float(entry_preco.get().replace(',', '.'))
            if preco < 0:
                messagebox.showerror("Erro", "Preço não pode ser negativo.")
                return
        except ValueError: # Se não for digitado um número cai nesse except
            messagebox.showerror("Erro", "Preço deve ser um número decimal.")
            return
            
        sucesso, mensagem = cadastro_dos_produtos(nome, marca, descricao, quantidade, preco)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            # Limpa os campos
            entry_nome.delete(0, tk.END)
            entry_marca.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_quantidade.delete(0, tk.END)
            entry_preco.delete(0, tk.END)
            entry_nome.focus()
        else:
            messagebox.showerror("Erro no banco de dados", mensagem)

    frame_botoes = tk.Frame(janela_cadastro)
    frame_botoes.pack(pady=15)

    tk.Button(frame_botoes, text="Salvar", command=salvar, bg="green", fg="white").grid(row=0, column=0, padx=10)
    tk.Button(frame_botoes, text="Cancelar", command=janela_cadastro.destroy, bg="red", fg="white").grid(row=0, column=1, padx=10)

    entry_nome.focus()
