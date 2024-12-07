
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemLeadingIcon,
)


MAIN_KV = '''
MDScreen:
    md_bg_color: app.theme_cls.backgroundColor

    MDScrollView:
        do_scroll_x: False

        MDBoxLayout:
            id: main_scroll
            orientation: "vertical"
            adaptive_height: True

            MDBoxLayout:
                adaptive_height: True

            MDTextField:
                mode: "outlined"
                size_hint_x: None
                width: "240dp"
                pos_hint: {"center_x": .20, "center_y": .26}
            MDButton:
                style: "outlined"
                pos_hint: {"center_x": .60, "center_y": .26}
                MDButtonText:
                    text: "Back"






'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(MAIN_KV)

    def on_start(self):

        info = ["ff","553554"]
        for info_item in info:
            self.root.ids.main_scroll.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text=info_item,
                    ),
                    pos_hint={"center_x": .5, "center_y": .5},
                )
            )

        Window.size = [dp(350), dp(600)]


Example().run()