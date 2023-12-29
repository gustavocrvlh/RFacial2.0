import tkinter as tk
from modules.webcam_capture import WebcamCapture

class WebcamPage(tk.Frame):
    def __init__(self, parent, show_page, main_page_instance, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.main_page_instance = main_page_instance

        # Inicializar a captura da webcam
        self.webcam = WebcamCapture()

        # Widget para exibir o feed de vídeo
        self.label_video = tk.Label(self)
        self.label_video.pack()

        # Iniciar a captura de frames
        self.capturar_frame()

        # Exemplo de botão que volta para a página principal
        button_back_to_main = tk.Button(self, text="Voltar para a Página Principal", command=self.back_to_main)
        button_back_to_main.pack(pady=10)

    def capturar_frame(self):
        img_tk = self.webcam.capture_frame()

        if img_tk is not None:
            self.label_video.config(image=img_tk)
            self.label_video.image = img_tk

        # Chama a função novamente após um intervalo (em milissegundos)
        self.label_video.after(10, self.capturar_frame)

    def release_camera(self):
        self.webcam.release_camera()

    def back_to_main(self):
        self.show_page(self.main_page_instance)

    def show_page(self, page):
        self.pack_forget()
        page.pack()