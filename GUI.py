from kivy.lang import Builder

from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty
KV = '''


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
                

    
MDScreenManager:

    MDScreen:
        name: "front_page"
        md_bg_color: "cadetblue"
        
        MDButton:
            pos_hint: {"center_x": .5,"center_y": .5}
            on_release:
                root.current = "first_input_page"

            MDButtonText:
                text: "Start"
                
                
    MDScreen:
        name: "first_input_page"
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
            on_release:
                root.current = "front_page"
            MDButtonText:
                text: "Back"
                   
        MDButton:
            style: "filled"
            pos_hint: {"center_x": .42, "center_y": .26}
            on_press: 
                app.save_values()
                root.current = "second_input_page"
            MDButtonText:
                text: "Enter"

    MDScreen:
        name: "second_input_page"
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
                    MDTextField:
                        id: secondinputfield
                        mode: "outlined"
                        size_hint_x: None  # Ensure width is used
                        width: dp(100)
    
                    MDButton:
                        size_hint_x: None
                        width: dp(200)
                        on_release: app.add_item_widget()
                        MDButtonText:
                            text: "Start"
        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(16)
            spacing: dp(20)
            pos_hint: {"center_x": 0.5, "y": 0}
    
            MDButton:            
                size_hint_x: None
                on_release:
                    root.current = "first_input_page"
                width: dp(150)
                MDButtonText:
                    text: "Go Back"

    
            MDButton:
                
                size_hint_x: None
                width: dp(150)
                MDButtonText:
                    text: "Enter"
'''

class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_input_list = []
        self.user_input_list2 = []
    def build(self):
        self.theme_cls.primary_palette = "Antiquewhite"
        return Builder.load_string(KV)
    def save_values(self):
        duration = self.root.ids.duration_slider.value
        max_people = self.root.ids.people_slider.value

        print(f"Duration: {duration} days")
        print(f"Max People: {max_people}")

        self.duration = duration
        self.max_people = max_people

    def add_item_widget(self):

        user_input = self.root.ids.inputfield.text.strip()
        user_input_No = self.root.ids.secondinputfield.text.strip()
        if user_input and user_input_No:
            self.user_input_list2.append([user_input,user_input_No])
            self.user_input_list.append(user_input)

            self.root.ids.main_scroll.add_widget(SwipeToDeleteItem(text=f"{user_input} X {user_input_No}"))

            self.root.ids.inputfield.text = ""
            self.root.ids.secondinputfield.text = ""

    def delete_item(self, list_item):
        """Remove the specified list item."""
        if list_item.text in self.user_input_list:
            self.user_input_list.remove(list_item.text)
        self.root.ids.main_scroll.remove_widget(list_item)

        print(self.user_input_list2)





Example().run()
