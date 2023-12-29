import cv2
import face_recognition
from datetime import datetime
import os
from tempfile import NamedTemporaryFile
import sqlite3
from PIL import Image, ImageTk
from pathlib import Path

class WebcamCapture:
    def __init__(self):
        # Conectar-se ao banco de dados SQLite
        script_directory = Path(__file__).resolve().parent
        db_path = script_directory / '..' / 'data' / 'database.db'
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

        # Consulta para buscar imagens da tabela
        self.c.execute("SELECT imagem, nome FROM usuarios")  # Substitua 'usuarios' pelo nome da sua tabela e 'imagem' pelo nome da coluna de imagem
        data = self.c.fetchall()

        # Cria um diretório temporário para armazenar as imagens
        self.temp_directory = 'temp_images'
        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)

        # Salvar imagens temporariamente no diretório temporário
        self.known_face_encodings = []
        self.known_face_names = []

        for image_blob, image_name in data:
            temp_image_path = os.path.join(self.temp_directory, image_name)
            with open(temp_image_path, 'wb') as f:
                f.write(image_blob)
            image = face_recognition.load_image_file(temp_image_path)
            encoding = face_recognition.face_encodings(image)[0]  # Assumindo que há apenas um rosto em cada imagem
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(image_name)

        # Inicializa a captura de vídeo
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Largura desejada
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Altura desejada

        # Variáveis adicionais para o reconhecimento facial
        self.frame_count = 0
        self.detection_interval = 5
        self.face_locations = []
        self.match_displayed = False
        self.face_detected_prev = False
        self.names_on_video = {}

    def capture_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        self.frame_count += 1

        if self.frame_count % self.detection_interval == 0:
            # Realiza o reconhecimento facial na imagem do frame
            self.face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, self.face_locations)

            # Limpa os nomes que não foram detectados
            self.names_on_video = {name: (left, top - 10) for name, (left, top) in self.names_on_video.items() if any(
                face_recognition.compare_faces(self.known_face_encodings, face_encoding) for face_encoding in face_encodings
            )}

            # Verifica se o rosto está sendo detectado na iteração atual
            face_detected = any(face_recognition.compare_faces(self.known_face_encodings, face_encodings) for face_encodings in face_encodings)

            # Exibe a mensagem de detecção no terminal se o rosto foi detectado nesta iteração
            if face_detected and not self.face_detected_prev:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{current_time}: Rosto correspondente detectado")
                for (top, right, bottom, left), face_encodings in zip(self.face_locations, face_encodings):
                    # Compara a codificação do rosto com as codificações conhecidas
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encodings)

                    for i, match in enumerate(matches):
                        if match:
                            name = self.known_face_names[i]
                            print(f"Nome: {name}")

            self.face_detected_prev = face_detected

            for (top, right, bottom, left), face_encodings in zip(self.face_locations, face_encodings):
                # Compara a codificação do rosto com as codificações conhecidas
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encodings)

                for i, match in enumerate(matches):
                    if match:
                        name = self.known_face_names[i]
                        # Adiciona o nome do rosto ao dicionário
                        self.names_on_video[name] = (left, top - 10)

        # Exibe o frame com retângulos ao redor dos rostos detectados
        for (top, right, bottom, left) in self.face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Exibe os nomes dos rostos detectados no vídeo
        for name, (left, top) in self.names_on_video.items():
            cv2.putText(frame, name, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Converte o frame para um formato suportado pelo ImageTk.PhotoImage
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img)

        return img_tk

    def release_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()