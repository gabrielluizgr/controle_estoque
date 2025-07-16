import tkinter as tk
from tkinter import messagebox
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

def listar_produtos_gui(janela_principal): # Criação de uma nova função que será chamada quando o usuário clicar no botão Listar Produtos
    janela_listagem = tk.Toplevel() # Criação de uma nova janela filha (secundária). Usamos Toplevel() ao invés de Tk(), porque essa janela depende da principal (não é uma aplicação, é só uma nova tela)
    janela_listagem.title("Lista de Produtos") # Define o título da janela
    janela_listagem.geometry("700x500") # Define o tamanho da janela

    frame = tk.Frame(janela_listagem) # Cria um frame, que é uma caixa contêiner dentro da janela. Serve como um espaço para agrupar elementos (como a lista e a barra de rolagem)
    frame.pack(fill=tk.BOTH, expand=True) # Coloca o frame na tela. "fill=tk.BOTH" sinaliza que ele vai ocupar o espaço tanto horizontal, quanto vertical. "expand=True" permite que o frame cresça junto com a janela, se ela for redimensionada
    scrollbar = tk.Scrollbar(frame) # Cria uma barra de rolagem vertical dentro do frame. Isso é importante caso tenhamos muitos produtos para exibir.
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Coloca a barra de rolagem na tela. "side=tk.RIGHT" sinaliza que ela aparecerá do lado direito da janela. "fill=tk.Y" faz com que ela se estique no eixo Y, ou seja, verticalmente
    lista = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=80) # Cria um componente Listbox, que é como uma caixa de listagem de itens. "yscrollcomand=scrollbar.set" conecta o scroll com a lista (para ele funcionar). "width=80" define a largura da lista (em caracteres, não pixels)
    lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Coloca a Listbox no lado esquerdo do frame e faz com que ele preencha todo o espaço disponível
    lista.config(selectmode=tk.NONE)
    lista.bind("<Button-1>", lambda e: "break")
    scrollbar.config(command=lista.yview) # Conecta o comando da barra de rolagem à Listbox, para que ela saiba o que fazer quando o usuário rolar a barra (nesse caso, mover a visualização da lista)

    # Chama a função separada do banco
    sucesso, resultado = lista_dos_produtos()
    if sucesso:
        produtos = resultado
        if produtos:
            for id, nome, marca, descricao, quantidade, preco in produtos:
                marca = marca.strip() if marca else "Sem marca"
                descricao = descricao.strip() if descricao else "Sem descrição"
                preco_formatado = f"{preco:.2f}".replace('.', ',')
                texto = f"ID: {id} | Nome: {nome} | Marca: {marca or 'Sem marca'} | Descrição: {descricao} | Quantidade: {quantidade} | Preço: R$ {preco_formatado}"
                lista.insert(tk.END, texto)
        else:
            lista.insert(tk.END, "Nenhum produto cadastrado.")
    else:
        messagebox.showerror("Erro", f"Erro ao acessar o banco: {resultado}")
    
    # Botão pra fechar janela
    frame_botoes = tk.Frame(janela_listagem)
    frame_botoes.pack(pady=10)
    btn_fechar = tk.Button(frame_botoes, text="Fechar", command=janela_listagem.destroy, bg="red", fg="white")
    btn_fechar.pack()