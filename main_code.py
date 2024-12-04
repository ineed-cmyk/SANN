from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
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
        pos_hint: {"center_x": .5, "center_y": .5}
        
        MDTextField:
    
            MDTextFieldHintText:
                text: "Enter"
    
            MDTextFieldHelperText:
                text: "Helper text"
                mode: "persistent"
    
            MDTextFieldTrailingIcon:
                icon: "information"
                
        MDTextField:
            
            MDTextFieldHintText:
                text: "Enter"
    
            MDTextFieldHelperText:
                text: "Helper text"
                mode: "persistent"
    
            MDTextFieldTrailingIcon:
                icon: "information"
                    
                

    MDButton:
        style: "outlined"
        pos_hint: {"center_x": .3, "center_y": .26}

        MDButtonText:
            text: "Back"
            
    MDButton:
        style: "filled"
        pos_hint: {"center_x": .42, "center_y": .26}

        MDButtonText:
            text: "Enter"

'''


class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)


Example().run()