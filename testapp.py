from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
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
        name: "start_screen"
        md_bg_color: (0.082, 0.043, 0, 0.180)
        MDIcon:
            icon: "exit-run"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            theme_text_color: "Secondary"

        #Text
        MDLabel:
            text: "CritKit"
            halign: "center"
            pos_hint: {"center_y": 0.6}
            theme_text_color: "Secondary"
        #Tagline
        MDLabel:
            text: "Assess how prepared you are for any disaster."
            halign: "center"
            pos_hint: {"center_y": 0.53}
            theme_text_color: "Primary"
        #Start button
        MDButton:
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            size_hint: (0.5, 0.08)
            md_bg_color: 1, 0.5, 0, 1 
            on_release:
                app.root.transition.direction = "left"
                app.root.current = "first_input_page"
            MDButtonText:
                text: "Get Started" 

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
                        on_text:
                            app.filter_items(self.text)
                        multiline: False
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
    ###Searching functions for drop down menu 
    def show_menu(self):
        try:
            if self.menu:
                self.menu.dismiss()
        except:
            pass
        self.menu = MDDropdownMenu(
            caller=self.root.ids.inputfield,  # The widget that triggers the dropdown
            items=self.menu_items,
            width_mult=8,
            position="bottom",
            )
        self.menu.open()

    def filter_items(self, search_text):
        """Filter the menu items based on the search text."""
        # List of items to be used in the dropdown
        all_items = ["Apple", "Banana", "Orange", "Grape", "Pineapple", "Strawberry", "Blueberry"]

    # Filter items based on the search text
        filtered_items = [
            {
            "text": item,
            "on_release": lambda x=item: self.set_text(x),
            }
            for item in all_items if search_text.lower() in item.lower()
            ]

            # Update the menu_items with the filtered items
        self.menu_items = filtered_items

            # Open the dropdown if there are any filtered items
        if self.menu_items:
            self.show_menu()

    def set_text(self, text):
        """Set the selected item text in the search input field."""
        self.root.ids.search_input.text = text
        self.menu.dismiss()
###Searching functions end here
    def read_item(self):
        if self.root.ids.search_input.text=="":
            pass
        else:
            product_name = self.root.ids.search_input.text
            product_quantity=self.root.ids.search_quantity.text
            print(product_name, product_quantity)
            self.root.ids.search_input.text = ""
            self.root.ids.search_quantity.text="1"




Example().run()