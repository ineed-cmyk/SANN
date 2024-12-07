from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.audio import SoundLoader
KV = '''
MDScreenManager:
    MDScreen:
        name: "start_screen"
        md_bg_color: app.theme_cls.bg_dark
        MDIcon:
            icon: "exit-run"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            font_size: "120sp"
            theme_text_color: "Custom"
            text_color: 1, 0.5, 0, 1 
        #Text
        MDLabel:
            text: "CritKit"
            font_style: "H3"
            halign: "center"
            pos_hint: {"center_y": 0.6}
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1 
        #Tagline
        MDLabel:
            text: "Assess how prepared you are for any disaster."
            font_style: "Body1"
            halign: "center"
            pos_hint: {"center_y": 0.53}
            theme_text_color: "Custom"
            text_color: 0.8, 0.8, 0.8, 1 
        #Start button
        MDRaisedButton:
            text: "Get Started"
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            size_hint: (0.5, 0.08)
            md_bg_color: 1, 0.5, 0, 1  
            on_release:
                app.play_click_sound()
                app.root.transition.direction = "left"
                app.root.current = "first_input_page"
        
    MDScreen:
        name: "first_input_page"
        md_bg_color: app.theme_cls.bg_dark

        MDLabel:
            text: "Enter Duration (Days)"
            pos_hint: {"center_x": .75, "center_y": .69}

        MDLabel:
            text: "Enter Max People"
            pos_hint: {"center_x": .75, "center_y": .47}

        # Duration Slider
        MDBoxLayout:
            orientation: "vertical"
            spacing: "20dp"
            adaptive_height: True
            size_hint_x: .5
            pos_hint: {"center_x": .5, "center_y": .6}

            MDSlider:
                id: duration_slider
                step: 1
                max: 30
                min: 1
                value: 1

        # People Slider
        MDBoxLayout:
            orientation: "vertical"
            spacing: "20dp"
            adaptive_height: True
            size_hint_x: .5
            pos_hint: {"center_x": .5, "center_y": .4}

            MDSlider:
                id: people_slider
                step: 1
                max: 15
                min: 1
                value: 1

        # Back Button
        MDRaisedButton:
            text: "Back"
            pos_hint: {"center_x": .3, "center_y": .26}
            on_release:
                app.root.transition.direction = "right"
                app.root.current = "start_screen"

        # Enter Button
        MDRaisedButton:
            text: "Enter"
            pos_hint: {"center_x": .5, "center_y": .26}
            on_press:
                app.save_values()
                app.root.current="Second_input_page"

    MDScreen:
        name: "Second_input_page"
        md_bg_color: app.theme_cls.bg_dark
        MDBoxLayout:
            orientation: 'vertical'
            spacing: "20dp"
            size_hint: None, None
            size: "300dp", "400dp"  
            padding: "10dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.8}
            MDLabel:
                text: "Search and Select an option:"
                theme_text_color: "Secondary"
                halign: "center"  # Horizontally center the label
                pos:50,200
                
            MDTextField:
                id: search_input
                hint_text: "Search"
                size_hint_x: None
                width: "280dp"
                on_text:
                    app.filter_items(self.text)
                multiline: False
                on_text_validate:
                    app.read_item()
'''

class CritKitApp(MDApp):
    def save_values(self):
        duration = self.root.ids.duration_slider.value
        max_people = self.root.ids.people_slider.value
        print(f"Duration: {duration} days")
        print(f"Max People: {max_people}")

        # Optionally store the values
        self.duration = duration
        self.max_people = max_people
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"  # Set light theme
        return Builder.load_string(KV)
    def play_click_sound(self):
        click_sound = SoundLoader.load("button_click.mp3") 
        if click_sound:
            click_sound.play()
###Searching functions for drop down menu 
    def show_menu(self):
        """Display the dropdown menu."""
        # Close the previous menu if it exists
        if self.menu:
            self.menu.dismiss()

        # Create the dropdown menu
        self.menu = MDDropdownMenu(
            caller=self.root.ids.search_input,  # The widget that triggers the dropdown
            items=self.menu_items,
            width_mult=4,
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
        text = self.root.ids.search_input.text
        print(text)
        self.root.ids.search_input.text = ""
if __name__ == "__main__":
    CritKitApp().run()
