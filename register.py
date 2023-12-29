import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

class RegisterPage(tk.Frame):
    def __init__(self, parent, show_page_callback, main_page_instance, db_path, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.show_page_callback = show_page_callback
        self.main_page_instance = main_page_instance
        self.db_path = db_path

        # Inicializar a conexão com o banco de dados SQLite
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

        # Widgets
        self.label_nome = tk.Label(self, text="Nome:")
        self.label_nome.pack()

        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        self.label_numero = tk.Label(self, text="Número:")
        self.label_numero.pack()

        self.entry_numero = tk.Entry(self)
        self.entry_numero.pack()

        self.label_cpf = tk.Label(self, text="CPF:")
        self.label_cpf.pack()

        self.entry_cpf = tk.Entry(self)
        self.entry_cpf.pack()

        self.label_imagem = tk.Label(self, text="Imagem:")
        self.label_imagem.pack()

        self.entry_caminho_imagem = tk.Entry(self)
        self.entry_caminho_imagem.pack()

        self.botao_selecionar_imagem = tk.Button(self, text="Selecionar Imagem", command=self.selecionar_imagem)
        self.botao_selecionar_imagem.pack()

        self.botao_cadastrar = tk.Button(self, text="Cadastrar", command=self.cadastrar_usuario)
        self.botao_cadastrar.pack()

        # Exemplo de botão que volta para a página principal
        button_back_to_main = tk.Button(self, text="Voltar para a Página Principal", command=self.back_to_main)
        button_back_to_main.pack(pady=10)

    def selecionar_imagem(self):
        caminho_imagem = filedialog.askopenfilename(title="Selecionar Imagem", filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg")])
        self.entry_caminho_imagem.delete(0, tk.END)
        self.entry_caminho_imagem.insert(0, caminho_imagem)

    def cadastrar_usuario(self):
        nome = self.entry_nome.get()
        numero = self.entry_numero.get()
        cpf = self.entry_cpf.get()
        caminho_imagem = self.entry_caminho_imagem.get()

        # Lógica para converter a imagem em bytes (se necessário) e salvar no banco de dados
        if caminho_imagem:
            with open(caminho_imagem, 'rb') as f:
                imagem_blob = f.read()
        else:
            # Lógica para lidar com o caso em que nenhuma imagem é fornecida
            imagem_blob = None

        # Inserir dados no banco de dados
        self.c.execute("INSERT INTO usuarios (nome, numero, cpf, imagem) VALUES (?, ?, ?, ?)", (nome, numero, cpf, imagem_blob))
        self.conn.commit()

        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")

        # Após cadastrar o usuário, voltar para a página principal
        self.show_page_callback(self.main_page_instance)

    def back_to_main(self):
        self.show_page_callback(self.main_page_instance)

    def show_page(self, page):
        self.pack_forget()
        page.pack()
