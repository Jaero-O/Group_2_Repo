from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import os

# You can later connect these with your ML model / severity functions
def classify_leaf(image_path):
    # TODO: Replace with real model prediction
    return "Anthracnose Detected", "Severity: 23%"

class DP1AppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        # Title
        self.add_widget(Label(text="🌿 DP1 Leaf Disease Classification", font_size='20sp', size_hint_y=None, height=50))

        # Display Image
        self.image_display = Image(source="", size_hint=(1, 0.5))
        self.add_widget(self.image_display)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        btn_layout.add_widget(Button(text="📷 Scan / Load Leaf", on_press=self.load_leaf))
        btn_layout.add_widget(Button(text="🔍 Classify", on_press=self.classify))
        btn_layout.add_widget(Button(text="💾 Save Result", on_press=self.save_result))
        self.add_widget(btn_layout)

        # Result area
        self.result_label = Label(text="No image loaded.", halign="center", valign="middle")
        self.add_widget(self.result_label)

        # Optional: log or notes
        self.notes = TextInput(hint_text="Notes or Observations...", size_hint_y=None, height=100)
        self.add_widget(self.notes)

        self.loaded_image_path = None

    def load_leaf(self, instance):
        chooser = FileChooserIconView(path=os.getcwd(), filters=["*.jpg", "*.png", "*.jpeg"])
        popup = Popup(title="Select a Leaf Image", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=lambda chooser, selection, touch: self.set_image(selection, popup))
        popup.open()

    def set_image(self, selection, popup):
        if selection:
            self.loaded_image_path = selection[0]
            self.image_display.source = self.loaded_image_path
            self.result_label.text = "Image Loaded."
            popup.dismiss()

    def classify(self, instance):
        if not self.loaded_image_path:
            self.show_popup("Error", "Please load an image first.")
            return
        label, severity = classify_leaf(self.loaded_image_path)
        self.result_label.text = f"[b]{label}[/b]\n{severity}"
        self.result_label.markup = True

    def save_result(self, instance):
        if not self.loaded_image_path:
            self.show_popup("Error", "No image loaded.")
            return
        text = self.result_label.text
        with open("results_log.txt", "a") as f:
            f.write(f"{self.loaded_image_path} | {text}\n")
        self.show_popup("Saved", "Result has been saved successfully!")

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200)).open()

class DP1App(App):
    def build(self):
        Window.size = (800, 600)
        return DP1AppLayout()

if __name__ == '__main__':
    DP1App().run()
