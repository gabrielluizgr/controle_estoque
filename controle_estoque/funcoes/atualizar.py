import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import busca_produto_id, atualizar_produto_id

def atualizar_produtos(): # Criação de uma função para atualizar produtos
    try:
        id_produto = int(input("Informe o ID do produto que deseja atualizar: ")) # Solicitando ao usuário o id do produto que deseja atualizar...
    except ValueError:
        print("ID inválido. Use apenas números")
        return
    
    conexao = None # Iniciando a variável para utilizar no finally
    # Conectando ao banco...
    try:
        conexao = sqlite3.connect("estoque.db")
        cursor = conexao.cursor()

        #Verificando se o produto existe...
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()

        if produto: 
            # Se o produto existir, realiza o desempacotamento...
            id, nome, marca, sabor, quantidade, preco = produto

            print(f"\nProduto atual: {nome}, Marca: {marca}, Sabor: {sabor}, Quantidade: {quantidade}, Preço: R$ {preco:.2f}") # Mostrando ao usuário o produto desempacotado que será atualizado...
            print(f"\nDeixe em branco caso não queira alterações.\n")

            novo_nome = input(f"Novo nome [{nome}]: ").strip() or nome # Colocando em novas variáveis as atualizações. Se nada for informado como novo nome, o antigo continua
            nova_marca = input(f"Nova marca [{marca}]: ").strip() or marca # Nova marca, se nada for informado, a antiga continua
            novo_sabor = input(f"Novo sabor [{sabor}]: ").strip() or sabor # Novo sabor, se nada for informado, o antigo continua

            while True: # Para a quantidade, validamos se foi digitada, se foi digitada, validamos se é inteiro ou não
                nova_quantidade_str = input(f"Nova quantidade [{quantidade}]: ").strip() # Nova quantidade
                if not nova_quantidade_str:
                    nova_quantidade = quantidade 
                    break
                try:
                    nova_quantidade = int(nova_quantidade_str)
                    break
                except ValueError:
                    print("Quantidade inválida. Por favor, digite um número inteiro.")
            # Para o preço, valida se digitou, se digitou, valida ser float
            while True:
                novo_preco_str = input(f"Novo preço [{preco}]: ").strip()
                if not novo_preco_str: # Se novo_preco_str for None, novo_preco volta a ser preco
                    novo_preco = preco
                    break
                try:
                    novo_preco = float(novo_preco_str) 
                    break
                except ValueError: 
                    print("Preço inválido. Por favor, digite um número decimal válido, usando ponto.")
            
            print("\nResumo da atualização:") # Resumo do que está sendo atualizado e confirmação
            print(f"Nome: {nome} ➜ {novo_nome}")
            print(f"Marca: {marca} ➜ {nova_marca}")
            print(f"Sabor: {sabor} ➜ {novo_sabor}")
            print(f"Quantidade: {quantidade} ➜ {nova_quantidade}")
            print(f"Preço: R$ {preco:.2f} ➜ R$ {novo_preco:.2f}")
            confirmar = input("Você realmente quer atualizar esse produto? (s/n) ").strip().lower()
            if confirmar != 's': # Se confirmar for diferente de s (sim), a atualização é cancelada
                print("Atualização cancelada")
                return
            
            #Atualizando o banco...
            cursor.execute("""
                UPDATE produtos
                SET nome = ?, marca = ?, quantidade = ?, preco = ?
                WHERE id = ?
            """, (novo_nome, nova_marca, novo_sabor, nova_quantidade, novo_preco, id_produto)) # Atualizando o nome, marca, quantidade, preco, do produto onde seu id é x

            conexao.commit() # Salvando as mudanças
            print("\nProduto atualizado com sucesso\n") # Mostrando o sucesso
        else:
            print("Produto não encontrado") # Se produto for None, produto não foi encontrado

    except sqlite3.Error as e: # Tratamento da exceção
        print(f"Erro ao acessar o banco de dados {e}")
    finally: # Finally o encerramento da conexão
        if conexao:
            conexao.close()

def atualizar_produtos_gui(janela_principal):# Criação de uma nova função que será chamada quando o usuário clicar no botão Atualizar Produto

    # Criação da nova janela filha
    janela_atualizar = tk.Toplevel()
    janela_atualizar.title("Atualizar Produto")
    janela_atualizar.geometry("400x500")
    janela_atualizar.configure(bg="#f0f0f0")

    # Título
    tk.Label(janela_atualizar, text="Atualizar Produto", font=("Segoe UI", 16, "bold"), bg="#f0f0f0").pack(pady=(20, 10))

    # Frame central dos campos
    frame_campos = tk.Frame(janela_atualizar, bg="#f0f0f0")
    frame_campos.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def campo(label_text):
        tk.Label(frame_campos, text=label_text, anchor="w", bg="#f0f0f0", font=("Segoe UI", 10, "bold")).pack(fill="x")
        entry = tk.Entry(frame_campos, font=("Segoe UI", 10))
        entry.pack(pady=5, fill="x")
        return entry
    
    # Campo para inserir o ID do produto
    entry_id = campo("ID do Produto *")
    entry_nome = campo("Novo Nome")
    entry_marca = campo("Nova Marca")
    entry_descricao = campo("Nova Descrição")
    entry_quantidade = campo("Nova Quantidade")
    entry_preco = campo("Novo Preço")


    # Criação da função para atualizar o banco
    def atualizar():
        try:
            id_produto = int(entry_id.get()) # ID é obrigatório e deve ser número
            produto_atual = busca_produto_id(id_produto)

            if not produto_atual: # Caso produto não exista, mostra o aviso e encerra a função
                messagebox.showwarning("Aviso", "Produto não encontrado.")
                return
            
            # Desempacotando dados atuais
            _, nome_atual, marca_atual, descricao_atual, quantidade_atual, preco_atual = produto_atual
            # Lê os novos dados ou mantém os antigos
            nome = entry_nome.get().strip() or nome_atual
            marca = entry_marca.get().strip() or marca_atual
            descricao = entry_descricao.get().strip() or descricao_atual

            if not nome: # Se o nome for vazio, mostra o aviso e encerra a função
                messagebox.showwarning("Aviso", "O nome do produto é obrigatório.")
                return
            
            quantidade_str = entry_quantidade.get().strip()

            if quantidade_str: # Verifica se o campo quantidade foi preenchido, se foi, o converte para int
                try:
                    quantidade = int(quantidade_str)
                    if quantidade < 0:
                        messagebox.showerror("Erro", "Quantidade não pode ser negativa.")
                        return
                except ValueError:
                    messagebox.showerror("Erro", "Quantidade deve ser número inteiro.")
            else:
                quantidade = quantidade_atual

            preco_str = entry_preco.get().strip().replace(',', '.')
            if preco_str: # Verifica se o campo preço foi preenchido, se foi, o converte para float
                try:
                    preco = float(preco_str)
                    if preco < 0:
                        messagebox.showerror("Erro", "Preço não pode ser negativo.")
                        return
                except ValueError:
                    messagebox.showerror("Erro", "Digite um preço válido. Use apenas números")
                    return
            else:
                preco = preco_atual # Se não foi preenchido, volta a ser o preço atual
                
            # Atualização do banco
            linhas_afetadas = atualizar_produto_id(id_produto, nome, marca, descricao, quantidade, preco)
            if linhas_afetadas == 0:
                messagebox.showwarning("Aviso", "Produto não encontrado.")
            else:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
                janela_atualizar.destroy()

        except ValueError: # Captura de erros de conversão ou no banco de dados
            messagebox.showerror("Erro", "ID Inválido: Use números inteiros.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    # Botões de atualizar e cancelar
    frame_botoes = tk.Frame(janela_atualizar, bg="#f0f0f0") # Cria um quadro ou contêiner dentro da janela janela_atualizar. Esse frame vai ser usado só para organizar os botões lado a lado
    frame_botoes.pack(pady=20) # Adiciona esse frame à janela e define um espaçamento vertical (padding) de 20px acima e abaixo

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=atualizar, bg="green", fg="white", font=("Segoe UI", 10, "bold"), width=12) # tk.Button cria um botão, "frame_botoes" será um botão filho "text="Atualizar"" define o texto visível dentro do botão, "command=atualizar" define a função que será chamada ao clicar o botão -- no caso a função será a criada antes atualizar(), "bg=green" é o fundo verde, "fg=white" define a cor do texto como branca. 
    btn_atualizar.grid(row=0, column=0, padx=10) # Usa o layout grid para posicionar o botão na linha 0, coluna 0, dentro do frame.padx=10 adiciona um espaçamento horizontal (padding) de 10px nas laterais.
    btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=janela_atualizar.destroy, bg="red", fg="white", font=("Segoe UI", 10, "bold"), width=12)
    btn_cancelar.grid(row=0, column=1, padx=10)