from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Images import images
import sys
import BackEnd

class DownloadThread(QThread):
    def __init__(self, video_url, case):
        super(QThread, self).__init__()
        self.update = BackEnd.run
        
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.Directory)
        self.file_dialog.setOption(QFileDialog.ShowDirsOnly)
        if self.file_dialog.exec_():
            print("Iniciando elección de directorio")
            self.directory = self.file_dialog.selectedFiles()[0]
            print("Selección de URL")
            self.video_url = video_url
            print("Evaluando el case")
            self.case = case

    def run(self):
        if self.case == 1:
            print(f"Caso 1, descargando video en {self.directory}, la url es {self.video_url}")
            BackEnd.get_video(self.video_url, self.update, self.directory)

        elif self.case == 2:
            print(f"Caso 2, descargando video en {self.directory}, la url es {self.video_url}")
            BackEnd.get_audio(self.video_url, self.update, self.directory)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Su descarga se ha realizado con éxito")
        msg.setWindowTitle("Youtube Download")
        msg.exec_()

class MainApp(QMainWindow):


    def __init__(self, parent=None, *args):
        super(MainApp, self).__init__(parent=parent)

        self.setFixedSize(640,434)    # Establece el tamaño minimo de la ventana
        self.setWindowTitle("Youtube Download") # Agrega un titulo a la ventana
        self.setWindowIcon(QIcon(":images/Logo_Linea_02.png"))
        width = self.frameGeometry().width      # Obtener el largo de la ventana pricipal
        height = self.frameGeometry().height    # Obtener la altura de la ventana pricipal
        centerH = int(width())/2
        centerV = int(height())/2
        self.centerH = int(width())/2
        self.centerV = int(height())/2
        self.setMouseTracking(True)

        label = QLabel(self)
        label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(":images/Fondo.jpeg").scaled(int(width()), int(height()), Qt.KeepAspectRatio,Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)    # Expandir el label al tamaño de la ventana principal        

        self.estilos = """
            QLineEdit {
                font: bold 14px;
                color: #fff;
                border: None;
                background: transparent;
            }
            QLabel {
                font: bold 14px;
                color: #fff;
                border: None;
                background: transparent;
            }
        """
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.2)
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(15)

        label.blurLabel = QLabel(label)
        label.blurLabel.setPixmap(pixmap)
        label.blurLabel.setGeometry(int(centerH-240), int(centerV-140), 480, 280)
        label.blurLabel.setStyleSheet("background: gray; border-radius: 20px")
        label.blurLabel.setGraphicsEffect(blur_effect)
        label.opacityLabel = QLabel(label)
        label.opacityLabel.setGeometry(int(centerH-240), int(centerV-140), 480, 280)
        label.opacityLabel.setStyleSheet("background: black; border-radius: 20px;")
        label.opacityLabel.setGraphicsEffect(opacity_effect)

        self.input_btn = QLineEdit(self)
        self.input_btn.setTextMargins(10, 0, 10, 0)
        self.input_btn.setFrame(False) 
        self.input_btn.setClearButtonEnabled(False)
        self.input_btn.clearFocus()
        self.input_btn.setGeometry(int(centerH-150), int(centerV-60), 300, 40)
        self.input_btn.setStyleSheet(self.estilos)

        self.btn_02 = QPushButton(self)
        self.btn_02.setGeometry(int(centerH+40), int(centerV + 60), 60, 60)
        self.btn_02.setIcon(QIcon(":images/Iconos-02.png"))
        self.btn_02.setIconSize(QSize(60,60))
        self.btn_02.setStyleSheet("text-align: center; background: transparent; border-radius: none;")
        self.btn_02.clicked.connect(self.start_download_video)

        self.btn_01 = QPushButton(self)
        self.btn_01.setGeometry(int(centerH-100), int(centerV + 60), 60, 60)
        self.btn_01.setIcon(QIcon(":images/Iconos-01.png"))
        self.btn_01.setIconSize(QSize(60,60))
        self.btn_01.setStyleSheet("text-align: center; background: transparent; border-radius: none;")
        self.btn_01.clicked.connect(self.start_download_audio)

        self.line_01 = QLabel(self)
        self.line_01.setGeometry(int(centerH-140), int(centerV - 30), 280, 2)
        self.line_01.setStyleSheet("background: #ffffff")

        font = QFont()
        font.setFamily('At Aero TRIAL Black')   # Se establece la fuente
        self.txt = QLabel(self)
        self.txt.setText("Ingrese una URL")
        self.txt.setGeometry(int(centerH-140), int(centerV - 60), 120, 40)
        self.txt.setFont(font)
        self.txt.setStyleSheet(self.estilos)

        self.input_btn.textChanged.connect(self.on_text_changed)

        self.show()

    def on_text_changed(self):
        if len(self.input_btn.text()) == 0:
            # Create an animation object
            self.animation = QPropertyAnimation(self.txt, b"pos")
            # Set the duration of the animation to 500 milliseconds
            self.animation.setDuration(100)
            # Set the start value of the animation to the current position of the label
            self.start_value = QPoint(self.txt.x(), self.txt.y())
            self.animation.setStartValue(self.start_value)
            # Set the end value of the animation to 5 pixels above the current position of the label
            if self.start_value.y() == int(self.centerV - 80):
                self.end_value = QPoint(self.txt.x(), self.txt.y()+20)
                self.animation.setEndValue(self.end_value)
            else:
                self.end_value = QPoint(self.txt.x(), self.txt.y())
                self.animation.setEndValue(self.end_value)
            # Start the animation
            self.animation.start()
        else:
            # Create an animation object
            self.animation = QPropertyAnimation(self.txt, b"pos")
            # Set the duration of the animation to 500 milliseconds
            self.animation.setDuration(100)
            # Set the start value of the animation to the current position of the label
            self.start_value = QPoint(self.txt.x(), self.txt.y())
            self.animation.setStartValue(self.start_value)
            if self.start_value.y() == int(self.centerV - 60):
                self.end_value = QPoint(self.txt.x(), self.txt.y()-20)
                self.animation.setEndValue(self.end_value)
            else:
                self.end_value = QPoint(self.txt.x(), self.txt.y())
                self.animation.setEndValue(self.end_value)
            # Start the animation
            self.animation.start()

    def start_download_video(self):
        video_url = self.input_btn.text()
        self.download_thread = DownloadThread(video_url, 1)
        self.download_thread.start()

    def start_download_audio(self):
        video_url = self.input_btn.text()
        self.download_thread = DownloadThread(video_url, 2)
        self.download_thread.start()

def run_frontend():
    app = QApplication([])  # Inicia la aplicacion
    window = MainApp()      # Se establece una ventana principal para arrancar
    window.show()           # Muestgra la ventana principal ( por default estan ocultas )
    app.exec_()             # Ejecutamos nuestra app

if __name__ == '__main__':
    run_frontend()