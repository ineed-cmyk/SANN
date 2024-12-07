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
            padding: dp(16)  
            spacing: dp(12)  

            MDBoxLayout:
                orientation: "horizontal"
                adaptive_height: True
                spacing: dp(20)  # Adjust spacing between the text field and button

                MDTextField:
                    id: inputfield
                    mode: "outlined"
                    size_hint_x: None  # Ensure width is used
                    width: dp(300)

                MDButton:
                    width: dp(200)
                    on_release: app.on_start()
                    MDButtonText:
                        text: "Start"
'''

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        Window.size = [dp(350), dp(600)]
        return Builder.load_string(MAIN_KV)

    def on_start(self):
        # Retrieve user input
        user_input = self.root.ids.inputfield.text.strip()
        user_input_list = []
        user_input_list.append(user_input)
        # Add the input to the list if it's not empty
        for uservalues in user_input_list:

            self.root.ids.main_scroll.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text=uservalues,
                    ),
                )
            )
            # Clear the input field after adding the item
            self.root.ids.inputfield.text = ""

Example().run()
