from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDScreen:

    MDChip:
        pos_hint: {"center_x": .5, "center_y": .5}
        type: "suggestion"
        line_color: "red"
        md_bg_color: 0, 1, 1, 1

        MDChipText:
            text: "MDChip"
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


Example().run()