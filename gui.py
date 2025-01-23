import flet as ft

#App Dimensions
width = 400
height = 800

#UI Colors
background_color = '#15719f'
app_icon_color = ft.Colors.AMBER
app_title_color = ft.Colors.WHITE
search_bar_color = '#91cfec'
search_icon_color = '#000000'
transparent_black = ft.Colors.with_opacity(0.25, '#000000')



def main(page: ft.Page):

    #App Page Settings
    page.window.width = 440
    page.window.height = 860
    page.title = 'Weatheria'
    page.scroll = 'auto'
    page.window.always_on_top = True #REMEMBER TO REMOVE IT FOR FINAL APP


    #Individual UI Elements
    app_icon = ft.Icon(ft.Icons.SUNNY, color = app_icon_color, size=30)
    app_title = ft.Text('Weatheria', color = app_title_color, size = 25, weight = 'w500')
    app_title_bar = ft.Container(
        content = ft.Row(
            controls = [
                app_title,
                app_icon,
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER
        ),
        alignment = ft.alignment.center
    )

    search_bar = ft.Container(
        content = ft.TextField(label = 'City Name', hint_text = 'Arlington', text_align = ft.TextAlign.LEFT, 
                             width = width/1.5, border_color = search_bar_color, border_width = 2.5, border_radius = 10),
        padding = ft.padding.only(top=10)
    )
    
    search_button = ft.Container(
        content = ft.IconButton(icon = ft.Icons.SEARCH, icon_color = search_icon_color, bgcolor = transparent_black, on_click = False), #NEED TO ADD THE GET_WEATHER FUNCTION
        padding = ft.padding.only(top = 10),
    )

    city_container = ft.Container(
        content = ft.Text(value = "City_Name", size = 25, weight = 'w300'),
        padding = ft.padding.only(left = width/16, bottom = -height/85),
    )
    location_icon = ft.Container(
        content = ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, color='white', size=25),
        padding = ft.padding.only(left = -width/40, bottom = -height/85)
    )

    #UI Elements Display
    app_page = ft.Container(
        content = ft.Column(
            controls = [
               ft.Row(
                    [app_title_bar], alignment = ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [search_bar, search_button], alignment = ft.MainAxisAlignment.CENTER
                ),
                ft.Row([city_container, location_icon]), 
            ]
        )
    )

    body = ft.Container(
        content = ft.Column(controls = [app_page]),
        width= width,
        height = height,
        bgcolor = background_color,
        ink = True,
        on_click = lambda e: None,
        padding = ft.padding.only(top = 25)
    )

    page.add(body)

ft.app(target = main)