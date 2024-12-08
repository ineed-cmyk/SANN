from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemTrailingIcon,
)
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty


MAIN_KV = '''
<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height

    MDCardSwipeLayerBox:
        padding: "8dp"

        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y": .5}
            on_release: app.delete_item(root)

    MDCardSwipeFrontBox:

        MDListItem:
            id: content
            _no_ripple_effect: True
            MDListItemHeadlineText:
                text:root.text
                

    
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
                    size_hint_x: None
                    width: dp(200)
                    on_release: app.on_start()
                    MDButtonText:
                        text: "Start"
'''
class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()

user_input_list = []
class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        Window.size = [dp(350), dp(600)]
        return Builder.load_string(MAIN_KV)

    def on_start(self):

        user_input = self.root.ids.inputfield.text.strip()
        user_input_list.append(user_input)
        for uservalues in user_input_list:

            self.root.ids.main_scroll.add_widget(SwipeToDeleteItem(text=f"{uservalues}"))



    def delete_item(self, list_item):
        """Remove the specified list item."""
        self.root.ids.main_scroll.remove_widget(list_item)

Example().run()

