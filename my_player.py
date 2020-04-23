from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel,\
    QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
import sys
from data import images


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOW Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon(images))
        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        self.init_ui()

        self.show()
    
    def init_ui(self):
        #create mediaplayer object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        #create videowidget
        videowidget = QVideoWidget()
        #create openbuton
        openButn = QPushButton('Open Video')
        openButn.clicked.connect(self.openfile)
        #create buton for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.playvideo)
        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.setposition)
        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
        #set widet to hboxlayout
        hboxLayout.addWidget(openButn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        self.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)
        #mediaplayer signal
        self.mediaPlayer.stateChanged.connect(self.mediastatechanged)
        self.mediaPlayer.positionChanged.connect(self.positionchanged)
        self.mediaPlayer.durationChanged.connect(self.durationchanged)

    def openfile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
    
    def playvideo(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastatechanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )
    
    def positionchanged(self, position):
        self.slider.setValue(position)
    
    def durationchanged(self, duration):
        self.slider.setRange(0, duration)

    def setposition(self, position):
        self.mediaPlayer.setPosition(position)

    def handererrors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error" + self.mediaPlayer.errorString())



app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
