KV = """
ScreenManager:
    id: screenmanager
    MenuScreen:
    WeatherScreen:

<MenuScreen>:
    name: "menu"
    Screen:
        NavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation: 'vertical'
                        MDToolbar:
                            title: "Menu"
                            elevation: 10
                            left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
                        MDGridLayout:
                            id: gridlayout
                            rows: 5
                            spacing: "40dp"
                            padding: "40dp"
                            row_force_default:True
                            row_default_height: 40

                            MDTextField:
                                id: user_input
                                hint_text: "Enter the name of the city"
                                pos_hint:{"center_x": 0.5, "center_y": 0.8}

                            MDRoundFlatButton:
                                text: "Weather"
                                size_hint: (0.5, 0.5)
                                on_press: app.show_weather_screen()

                            MDRoundFlatButton:
                                text: "Air quality"
                                size_hint: (0.5, 0.5)
                                on_release: app.show_aqi()

                            MDRectangleFlatButton:
                                id: info_button
                                text_color: 1,1,1,1
                                size_hint: (0.5, 0.5)

                            AnchorLayout:
                                anchor_x: 'right'
                                anchor_y: 'bottom'
                                MDIconButton:
                                    icon: "trash-can-outline"
                                    on_release: app.clear_info()


                        Widget:

            MDNavigationDrawer:
                id: nav_drawer
                BoxLayout:
                    orientation: "vertical"
                    spacing: '8dp'
                    padding: '8dp'

                    ScrollView:
                        MDList:
                            id: dropdownmenu
                            OneLineAvatarIconListItem:
                                text: "Info"
                                Container:
                                    id: container

                                    MDIconButton:
                                        icon: "plus"
                                        on_release: app.nav_drawer_info()

<WeatherScreen>:
    name: "weather"
    BoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: "20dp"
        MDLabel:
            id: city
            halign: "center"
        MDIcon:
            id: icon_label
            size_hint: (None, None)
            width: "100dp"
            height: "100dp"
            pos_hint:{"center_x": 0.5, "center_y": 0.8}
        MDLabel:
            id: temp
            halign: "center"
        MDLabel:
            id: main_description
            halign: "center"
        MDLabel:
            id: add_description
            halign: "center"
        AnchorLayout:
            anchor_x: 'right'
            anchor_y: 'bottom'
            MDIconButton:
                icon:  "home-circle-outline"
                on_release: root.manager.current = "menu"


"""
