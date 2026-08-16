from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import os

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class ExpenseCard(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 70
        self.padding = 10
        self.canvas.before:
            # Ye har card ko ek halka grey background dega
            from kivy.graphics import Color, Rectangle
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(Label(text=text, color=(1, 1, 1, 1)))

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class SpendWiseApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header (Clear & Privacy)
        header = BoxLayout(size_hint_y=0.08, spacing=5)
        header.add_widget(Button(text="Clear All", background_color=(0.8, 0, 0, 1)))
        header.add_widget(Button(text="Privacy", background_color=(0.3, 0.3, 0.3, 1)))
        root.add_widget(header)
        
        # Inputs
        root.add_widget(self.amount := TextInput(hint_text="Amount", multiline=False, size_hint_y=0.07))
        root.add_widget(self.cat := TextInput(hint_text="Category", multiline=False, size_hint_y=0.07))
        
        save = Button(text="POST EXPENSE", size_hint_y=0.08, background_color=(0, 0.6, 0.3, 1))
        save.bind(on_press=self.add_data)
        root.add_widget(save)
        
        # Feed Area
        self.feed = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.feed.bind(minimum_height=self.feed.setter('height'))
        scroll = ScrollView(size_hint=(1, 0.6))
        scroll.add_widget(self.feed)
        root.add_widget(scroll)
        
        self.show_data()
        return root

    def add_data(self, instance):
        if self.amount.text:
            with open("data.txt", "a") as f:
                f.write(f"{self.cat.text} : ₹{self.amount.text}\n")
            self.amount.text = ""
            self.show_data()

    def show_data(self):
        self.feed.clear_widgets()
        if os.path.exists("data.txt"):
            with open("data.txt", "r") as f:
                for line in reversed(f.readlines()):
                    self.feed.add_widget(ExpenseCard(line.strip()))

if __name__ == '__main__':
    SpendWiseApp().run()