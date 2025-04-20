import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QRadioButton, QSlider, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from image_processing import apply_fourier_filter
from PIL import Image

class FourierFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Filtering with Fourier Transform")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # UI layout
        self.layout = QHBoxLayout() 
        self.central_widget.setLayout(self.layout)

        self.controls_panel = QWidget()
        self.controls_layout = QVBoxLayout()
        self.controls_panel.setLayout(self.controls_layout)

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        self.controls_layout.addWidget(self.load_button)

        self.low_pass_radio = QRadioButton("Low-pass Filter")
        self.high_pass_radio = QRadioButton("High-pass Filter")
        self.low_pass_radio.setChecked(True)
        self.low_pass_radio.toggled.connect(self.update_preview)  
        self.high_pass_radio.toggled.connect(self.update_preview)
        self.controls_layout.addWidget(self.low_pass_radio)
        self.controls_layout.addWidget(self.high_pass_radio)

        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setMinimum(10)
        self.radius_slider.setMaximum(100)
        self.radius_slider.setValue(30)
        self.radius_slider.valueChanged.connect(self.schedule_preview_update)  
        self.controls_layout.addWidget(self.radius_slider)

        self.apply_button = QPushButton("Apply Filter")
        self.apply_button.clicked.connect(self.apply_filter)
        self.controls_layout.addWidget(self.apply_button)

        self.layout.addWidget(self.controls_panel)

        self.image_panel = QWidget()
        self.image_layout = QVBoxLayout()
        self.image_panel.setLayout(self.image_layout)

        self.original_image_label = QLabel("Original Image")
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.original_image_label)

        self.preview_image_label = QLabel("Preview (Filtered Image)")
        self.preview_image_label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.preview_image_label)

        self.layout.addWidget(self.image_panel)

        self.preview_timer = QTimer()
        self.preview_timer.setInterval(200)  
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.update_preview)

    def load_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.jpg *.png *.jpeg)", options=options)
        if self.image_path:
            self.display_image(self.image_path)
            self.update_preview()  

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.original_image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def schedule_preview_update(self):
        self.preview_timer.start()

    def update_preview(self):
        if not self.image_path:
            return

        thumbnail_size = (200, 200)  
        image = Image.open(self.image_path)
        image.thumbnail(thumbnail_size)

        filter_type = "low" if self.low_pass_radio.isChecked() else "high"
        radius = self.radius_slider.value()
        filtered_image = apply_fourier_filter(self.image_path, filter_type, radius)
        filtered_image.thumbnail(thumbnail_size)

        
        filtered_image.save("temp_preview.jpg")  
        preview_pixmap = QPixmap("temp_preview.jpg")
        self.preview_image_label.setPixmap(preview_pixmap)

    def apply_filter(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Please load an image first!")
            return

        filter_type = "low" if self.low_pass_radio.isChecked() else "high"
        radius = self.radius_slider.value()
        filtered_image = apply_fourier_filter(self.image_path, filter_type, radius)

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Filtered Image", "", "Images (*.jpg *.png *.jpeg)")
        if save_path:
            filtered_image.save(save_path)
            QMessageBox.information(self, "Success", "Filtered image saved successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FourierFilterApp()
    window.show()
    sys.exit(app.exec_())
