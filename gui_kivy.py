import os
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from PIL import Image
import joblib

# Set window background color - gradient-like background
Window.clearcolor = (0.68, 0.85, 0.90, 1)  # Light cyan/blue

# Load the pre-trained SVM model
model_path = "svm_model.pkl"
if os.path.exists(model_path):
    svm_model = joblib.load(model_path)
    print("Model SVM berhasil dimuat.")
else:
    print(f"Model tidak ditemukan di {model_path}")
    exit(1)


class CardWidget(BoxLayout):
    def __init__(self, bg_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class HandwritingApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 20
        
        # Prediction history
        self.prediction_history = []
        self.total_predictions = 0
        
        # Main content area
        main_content = self.create_main_content()
        self.add_widget(main_content)
        
        # Placeholder for the image data
        self.image_data = None

    def create_main_content(self):
        main = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=15)
        
        # Header
        header = self.create_header()
        main.add_widget(header)
        
        # Content grid
        content = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=15)
        
        # Top row - Image preview and prediction result
        top_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.5), spacing=15)
        
        # Image preview card
        image_card = self.create_image_card()
        top_row.add_widget(image_card)
        
        # Prediction result card
        result_card = self.create_result_card()
        top_row.add_widget(result_card)
        
        content.add_widget(top_row)
        
        # Middle row - Statistics cards
        stats_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.25), spacing=15)
        
        # Statistics card - only accuracy
        self.accuracy_label = self.create_stat_card('Akurasi Model', '95.2%', (0.3, 0.7, 0.5, 1))
        
        stats_row.add_widget(BoxLayout(size_hint=(0.33, 1)))  # Spacer
        stats_row.add_widget(self.accuracy_label)
        stats_row.add_widget(BoxLayout(size_hint=(0.33, 1)))  # Spacer
        
        content.add_widget(stats_row)
        
        # Bottom row - Action buttons
        action_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.25), spacing=15, padding=[0, 10])
        
        action_card = CardWidget(bg_color=(0.2, 0.6, 0.7, 1))
        action_card.orientation = 'vertical'
        action_card.padding = 20
        action_card.spacing = 10
        
        action_title = Label(
            text='[b]Mulai Prediksi[/b]',
            markup=True,
            font_size='18sp',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.3),
            halign='left',
            valign='middle'
        )
        action_title.bind(size=action_title.setter('text_size'))
        action_card.add_widget(action_title)
        
        action_subtitle = Label(
            text='Pilih gambar tulisan tangan untuk dikenali',
            font_size='13sp',
            color=(0.9, 0.9, 0.9, 1),
            size_hint=(1, 0.3),
            halign='left',
            valign='middle'
        )
        action_subtitle.bind(size=action_subtitle.setter('text_size'))
        action_card.add_widget(action_subtitle)
        
        button_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=10)
        
        load_btn = Button(
            text='Pilih Gambar',
            font_size='14sp',
            bold=True,
            background_normal='',
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.7, 1),
            size_hint=(0.5, 1)
        )
        load_btn.bind(on_press=self.open_filechooser)
        
        predict_btn = Button(
            text='Prediksi Sekarang',
            font_size='14sp',
            bold=True,
            background_normal='',
            background_color=(0.1, 0.4, 0.5, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.5, 1)
        )
        predict_btn.bind(on_press=self.predict_digit)
        
        button_box.add_widget(load_btn)
        button_box.add_widget(predict_btn)
        action_card.add_widget(button_box)
        
        action_row.add_widget(action_card)
        content.add_widget(action_row)
        
        main.add_widget(content)
        return main

    def create_header(self):
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        
        # Logo and title section
        logo_title_box = BoxLayout(orientation='horizontal', size_hint=(0.6, 1), spacing=15)
        
        # Logo
        logo_path = 'logo UNPATTI.png'
        if os.path.exists(logo_path):
            logo_widget = KivyImage(source=logo_path, size_hint=(0.15, 1), allow_stretch=True, keep_ratio=True)
            logo_title_box.add_widget(logo_widget)
        
        # Welcome and Dashboard text
        welcome_box = BoxLayout(orientation='vertical', size_hint=(0.85, 1))
        welcome_label = Label(
            text='[color=3399cc]Selamat datang![/color]',
            markup=True,
            font_size='14sp',
            halign='left',
            valign='bottom',
            size_hint=(1, 0.4)
        )
        welcome_label.bind(size=welcome_label.setter('text_size'))
        
        dashboard_label = Label(
            text='[b]Dashboard Pengenalan Tulisan Tangan[/b]',
            markup=True,
            font_size='26sp',
            color=(0.2, 0.2, 0.2, 1),
            halign='left',
            valign='top',
            size_hint=(1, 0.6)
        )
        dashboard_label.bind(size=dashboard_label.setter('text_size'))
        
        welcome_box.add_widget(welcome_label)
        welcome_box.add_widget(dashboard_label)
        logo_title_box.add_widget(welcome_box)
        
        header.add_widget(logo_title_box)
        
        # Spacer
        header.add_widget(BoxLayout(size_hint=(0.4, 1)))
        
        return header

    def create_image_card(self):
        card = CardWidget(bg_color=(1, 1, 1, 1))
        card.orientation = 'vertical'
        card.padding = 15
        card.spacing = 10
        card.size_hint = (0.5, 1)
        
        title = Label(
            text='[b]Preview Gambar[/b]',
            markup=True,
            font_size='16sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(1, 0.1),
            halign='left',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        card.add_widget(title)
        
        # Image container
        image_container = BoxLayout(size_hint=(1, 0.9), padding=10)
        self.image_widget = KivyImage(size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
        image_container.add_widget(self.image_widget)
        card.add_widget(image_container)
        
        return card

    def create_result_card(self):
        card = CardWidget(bg_color=(1, 1, 1, 1))
        card.orientation = 'vertical'
        card.padding = 15
        card.spacing = 10
        card.size_hint = (0.5, 1)
        
        title = Label(
            text='[b]Hasil Prediksi[/b]',
            markup=True,
            font_size='16sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(1, 0.1),
            halign='left',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        card.add_widget(title)
        
        # Result display
        result_box = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=20)
        
        self.result_label = Label(
            text='[size=80][b]-[/b][/size]',
            markup=True,
            font_size='80sp',
            color=(0.2, 0.6, 0.7, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.6)
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        
        self.result_text = Label(
            text='Belum ada prediksi',
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1),
            halign='center',
            valign='top',
            size_hint=(1, 0.4)
        )
        self.result_text.bind(size=self.result_text.setter('text_size'))
        
        result_box.add_widget(self.result_label)
        result_box.add_widget(self.result_text)
        card.add_widget(result_box)
        
        return card

    def create_stat_card(self, title, value, color):
        card = CardWidget(bg_color=color)
        card.orientation = 'vertical'
        card.padding = 15
        card.spacing = 5
        
        title_label = Label(
            text=title,
            font_size='12sp',
            color=(1, 1, 1, 0.8),
            size_hint=(1, 0.3),
            halign='left',
            valign='bottom'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        value_label = Label(
            text=f'[b]{value}[/b]',
            markup=True,
            font_size='24sp',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.7),
            halign='left',
            valign='top'
        )
        value_label.bind(size=value_label.setter('text_size'))
        
        card.add_widget(title_label)
        card.add_widget(value_label)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card

    def open_filechooser(self, instance):
        # Open a filechooser popup to select an image
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg', '*.bmp'])
        popup = Popup(title='Pilih Gambar', content=filechooser, size_hint=(0.9, 0.9))

        # Bind on_submit to a method that properly handles arguments
        filechooser.bind(on_submit=self.load_image_from_path)
        filechooser.popup = popup  # Store the popup to dismiss later
        popup.open()

    def load_image_from_path(self, filechooser, selection, *args):
        if selection:
            image_path = selection[0]
            if os.path.exists(image_path):
                try:
                    # Load and preprocess the image
                    img = Image.open(image_path).convert('L')  # Convert to grayscale
                    img_resized = img.resize((28, 28))  # Resize for model input
                    self.image_data = np.array(img_resized).flatten() / 255.0  # Normalize

                    # Update the image widget to display the selected image
                    self.image_widget.source = image_path
                    self.image_widget.reload()  # Reload to reflect changes
                    
                    # Update result text
                    self.result_text.text = 'Gambar berhasil dimuat. Klik Prediksi!'
                    self.result_text.color = (0.2, 0.6, 0.7, 1)
                    
                    print(f"Gambar {image_path} berhasil dimuat.")
                    
                    if hasattr(filechooser, 'popup'):
                        filechooser.popup.dismiss()  # Close the popup
                except Exception as e:
                    print(f"Gagal memuat gambar: {e}")
                    self.result_text.text = 'Gagal memuat gambar'
                    self.result_text.color = (0.9, 0.3, 0.3, 1)
            else:
                print(f"Gambar tidak ditemukan di {image_path}")

    def predict_digit(self, instance):
        if self.image_data is None:
            self.result_text.text = 'Belum ada gambar yang dipilih'
            self.result_text.color = (0.9, 0.3, 0.3, 1)
            print("Tidak ada gambar yang dimuat untuk diprediksi.")
            return

        try:
            prediction = svm_model.predict([self.image_data])
            predicted_digit = prediction[0]
            
            # Update result display
            self.result_label.text = f'[size=80][b]{predicted_digit}[/b][/size]'
            self.result_label.color = (0.2, 0.7, 0.4, 1)
            self.result_text.text = f'Prediksi: Angka {predicted_digit}'
            self.result_text.color = (0.2, 0.7, 0.4, 1)
            
            # Update statistics
            self.total_predictions += 1
            self.prediction_history.append(predicted_digit)
            
            print(f"Hasil prediksi: {predicted_digit}")
        except Exception as e:
            print(f"Terjadi kesalahan selama prediksi: {e}")
            self.result_text.text = 'Terjadi kesalahan saat prediksi'
            self.result_text.color = (0.9, 0.3, 0.3, 1)


class MainApp(App):
    def build(self):
        self.title = 'Pengenalan Tulisan Tangan Menggunakan SVM'
        return HandwritingApp()


if __name__ == '__main__':
    MainApp().run()
