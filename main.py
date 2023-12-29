import tkinter as tk
from modules.webcam_capture import WebcamCapture
from register import RegisterPage
from webcam_page import WebcamPage
from pathlib import Path

class MyApp:
    def __init__(self):
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("RFacial 2.0")

        # Propriedades da janela
        largura_janela = 800
        altura_janela = 600
        posicao_x = (self.root.winfo_screenwidth() - largura_janela) // 2  # Centralizar na tela
        posicao_y = (self.root.winfo_screenheight() - altura_janela) // 2  # Centralizar na tela
        self.root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")
        self.root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

        script_directory = Path(__file__).resolve().parent
        db_path = script_directory / 'data' / 'database.db'

        # Criação de instâncias dos frames
        self.mainPage = tk.Frame(self.root)
        self.webcamPage = WebcamPage(self.root, self.show_page, self.mainPage)
        self.registerPage = RegisterPage(self.root, self.show_page, self.mainPage, db_path)

        self.nextPage = tk.Frame(self.root)

        # Iniciar com a página principal visível
        self.mainPage.pack()

        # Exemplo de botão na página principal que muda para a página da webcam
        button_goto_webcam = tk.Button(self.mainPage, text="Ir para a Página da Webcam",
                                       command=lambda: self.show_page(self.webcamPage))
        button_goto_webcam.pack(pady=10)

        # Exemplo de botão na página principal que muda para a nova página
        button_goto_register = tk.Button(self.mainPage, text="Ir para a Página de Registro",
                                         command=lambda: self.show_page(self.registerPage))
        button_goto_register.pack(pady=10)

        # Iniciar o loop principal
        self.root.mainloop()

    def show_page(self, page):
        self.mainPage.pack_forget()
        self.webcamPage.pack_forget()
        self.registerPage.pack_forget()
        self.nextPage.pack_forget()

        page.pack()

        largura_janela = 800
        altura_janela = 600
        posicao_x = (self.root.winfo_screenwidth() - largura_janela) // 2  # Centralizar na tela
        posicao_y = (self.root.winfo_screenheight() - altura_janela) // 2  # Centralizar na tela
        self.root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

app = MyApp()
