import sqlite3 # Traz para o programa a biblioteca padrão do Python que lida com banco de dados SQLite

def atualizar_produto_id(id_produto, nome, marca, quantidade, preco):
    try:
        conexao = sqlite3.connect("estoque.db")
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE produtos
            SET nome = ?, marca = ?, quantidade = ?, preco = ?
            WHERE id = ?
        """, (nome, marca, quantidade, preco, id_produto))
        conexao.commit()
        linhas_afetadas = cursor.rowcount
        conexao.close()
        return linhas_afetadas
    except sqlite3.Error as e:
        print(f"Erro ao atualizar produto: {e}")
        return 0

def remover_produto_id(id_produto):
    try:
        conexao = sqlite3.connect("estoque.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conexao.commit()
        linha_afetada = cursor.rowcount
        conexao.close()
        return linha_afetada
    except sqlite3.Error as e:
        print(f"Erro ao remover produto: {e}")
        return 0

def busca_produto_id(id_produto):
    try:
        conexao = sqlite3.connect("estoque.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()
        conexao.close()
        return produto
    except sqlite3.Error as e:
        print(f"Erro ao buscar produto: {e}")
        return None

def lista_dos_produtos():
    try:
        conexao = sqlite3.connect("estoque.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        conexao.close()
        return True, produtos
    except sqlite3.Error as e:
        return False, str(e)

def cadastro_dos_produtos(nome, marca, quantidade, preco):
    try:
        conexao = sqlite3.connect("estoque.db")
        cursor = conexao.cursor()
        cursor.execute("""
                       INSERT INTO produtos (nome, marca, quantidade, preco)
                       VALUES(?, ?, ?, ?)
                       """, (nome, marca, quantidade, preco))
        conexao.commit()
        conexao.close()
        return True, "Produto cadastrado com sucesso!"
    except sqlite3.Error as e:
        return False, str(e)

def criar_tabela():
    # Tratando exceções
    try:
        # Usando with para abrir a conexão e garantir que ela será fechada no final
        with sqlite3.connect("estoque.db") as conexao: # Cria o arquivo estoque.db, se ele não existir, se já existir, apenas abre
            cursor = conexao.cursor() # "cursor" pode ser imaginado como uma caneta, que escreve ou lê coisas dentro do banco de dados

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos'") # "sqlite_master" é um lugar especial, onde o SQLite guarda informações sobre tudo que existe no banco de dados: tabelas, índices, etc... Basicamente, o que acontece nesse comando é: "Olha aí no banco se existe uma tabela com o nome "produtos"
            tabela_existe = cursor.fetchone() # "fetchone" pega o primeiro resultado da consulta. Se vier algo, a tabela existe. Se vier None, a tabela ainda não existe

            if not tabela_existe: # Verificação condicional, se a o valor que veio antes for None, a tabela não existe, então, criamos ela, e mostramos a mensagem de sucesso. Se a tabela já existir, mostramos uma outra mensagem, informando que nada foi criado
                cursor.execute("""
                    CREATE TABLE produtos (                     
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        marca TEXT,
                        quantidade INTEGER,
                        preco REAL
                    )
             """)
    
        # "cursor.execute" basicamente realiza uma ação no nosso banco de dados (cria tabela, insere, lê, remove, atualiza...). No caso, está criando uma tabela
        # CREATE TABLE produtos: Criando a tabela produtos
        # id INTEGER PRIMARY KEY AUTOINCREMENT: "id" é o identificador único de cada produto, como se fosse o "número de cadastro". "INTEGER" é um tipo de dado, só aceita números inteiros. "PRIMARY KEY" significa que esse atributo é único e não pode repetir. "AUTOINCREMENT" significa que ele é gerado automaticamente, sem você precisar digitar. Ex: O primeiro produto recebe id = 1, o segundo, id = 2, e assim por diante.
    
        # nome TEXT NOT NULL: "nome" é o nome do produto (ex: Whey, Creatina...). "TEXT" é um tipo de dado, só aceita texto (letras, espaços, acentos) e "NOT NULL" significa que é obrigatório preencher -- não é possível deixar em branco.
        # marca TEXT: "marca" é o nome da marca ou do fabricante do produto (ex: Max Titanium, Growth...) e "TEXT" é o tipo do dado, somente texto. Não há "NOT NULL", então, não é obrigatório preencher.
        # quantidade INTEGER: "quantidade" quantos desse item estão no estoque e "INTEGER" tipo do dado, somente números inteiros. Essa coluna vai mudar com o tempo: quando você vender ou repor o estoque.
        # preco REAL: "preco" preço de venda do produto. "REAL" tipo de dado -- só aceita número decimal, como se fosse o "float" do Python.

                print("Banco de dados e tabela criados com sucesso!")
                conexao.commit() # "commit" salva no banco qualquer alteração feita
            else:
                print("Banco de dados já existia. Nenhuma tabela nova criada.")

    except sqlite3.Error as e: # Captura de qualquer erro relacionado ao sqlite3
        print(f"Erro ao trabalhar com o banco de dados: {e}")
    except Exception as e: # Captura outros erros gerais 
        print(f"Ocorreu um erro inesperado: {e}")