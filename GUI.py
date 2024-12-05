from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen

KV = '''
Window_Manager:
    first_window:
    second_window:
<first_window>:
    name: "first"
    MDScreen:
        md_bg_color: self.theme_cls.backgroundColor
        MDLabel:
            text: "Enter Duration(Days)"
            pos_hint: {"center_x": .75, "center_y": .69}
        MDLabel:
            text: "Enter Max People"
            pos_hint: {"center_x": .75, "center_y": .47}
    
        MDBoxLayout:
            orientation: "vertical"
            spacing: "80dp"
            adaptive_height: True
            size_hint_x: .5
            pos_hint: {"center_x": .5, "center_y": .6}
    
            MDSlider:
                id: duration_slider
    
                step: 1
                max: 30
                min:1
                value: 1
    
                MDSliderHandle:
    
                MDSliderValueLabel:
        MDBoxLayout:
            orientation: "vertical"
            spacing: "80dp"
            adaptive_height: True
            size_hint_x: .5
            pos_hint: {"center_x": .5, "center_y": .4}
    
            MDSlider:
                id: people_slider
    
                step: 1
                max: 15
                min:1
                value: 1
    
                MDSliderHandle:
    
                MDSliderValueLabel:
    
    




    MDButton:
        style: "outlined"
        pos_hint: {"center_x": .3, "center_y": .26}
        on_release: app.root.current = "second"

        MDButtonText:
            text: "Back"

    MDButton:
        style: "filled"
        pos_hint: {"center_x": .42, "center_y": .26}
        on_press: app.save_values()
        MDButtonText:
            text: "Enter"


    <second_window>:
    name: "second"
    MDScreen:
        md_bg_color: self.theme_cls.backgroundColor

        MDButton:
            style: "filled"
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: app.root.current = "first"
            MDButtonText:
                text: "Goback"
                
'''

class first_window(MDScreen):
    pass
class second_window(MDScreen):
    pass
class Window_Manager(MDScreenManager):
    pass


class Example(MDApp):


    def save_values(self):
        duration = self.root.ids.duration_slider.value
        max_people = self.root.ids.people_slider.value

        print(f"Duration: {duration} days")
        print(f"Max People: {max_people}")

        self.duration = duration
        self.max_people = max_people

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)



Example().run()