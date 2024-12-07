from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
)

MAIN_KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    

    MDScrollView:
        do_scroll_x: False

        MDBoxLayout:
            id: main_scroll
            orientation: "vertical"
            adaptive_height: True
            padding: dp(16)  # Add padding around the entire content
            spacing: dp(12)  # Add spacing between widgets

            MDBoxLayout:
                orientation: "horizontal"
                adaptive_height: True
                spacing: dp(8)  # Adjust spacing between the text field and button

                MDTextField:
                    id: inputfield
                    mode: "outlined"
                    size_hint_x: 0.75
                    hint_text: "Enter text"

                MDButton:
                    text: "Add"
                    size_hint_x: 0.25
                    on_release: app.on_start()
'''

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        Window.size = [dp(350), dp(600)]
        return Builder.load_string(MAIN_KV)

    def on_start(self):
        # Retrieve user input
        user_input = self.root.ids.inputfield.text.strip()

        # Add the input to the list if it's not empty
        if user_input:
            self.root.ids.main_scroll.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text=user_input,
                    ),
                )
            )
            # Clear the input field after adding the item
            self.root.ids.inputfield.text = ""

Example().run()
