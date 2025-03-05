import flet as ft
from backend import get_weather

#App Dimensions
width = 400
height = 800

#UI Colors
background_color = '#15719f'
app_icon_color = ft.Colors.AMBER
app_title_color = ft.Colors.WHITE
search_bar_color = '#d1bd21'
search_icon_color = '#000000'
transparent_black = ft.Colors.with_opacity(0.25, '#000000')
divider_color = '#000000'
sunrise_gradient = [ft.Colors.AMBER_200, '#FFC107', '#FFEB3B']
sunset_gradient = ['#000033', '#001A66', '#001F54']
error_text_color = ft.Colors.AMBER



def main(page: ft.Page):
    global gui_values


    #App Page Settings
    page.window.width = 440
    page.window.height = 860
    page.title = 'Weatheria'
    page.scroll = 'auto'
    page.window.always_on_top = True #REMEMBER TO REMOVE IT FOR FINAL APP

    def call_weather(search_bar):

        gui_values["search_bar"].value = search_bar.content.value
        get_weather(gui_values)

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
                             width = width/1.5, border_color = search_bar_color, border_width = 2.5, border_radius = 25),
        padding = ft.padding.only(top=10)
    )
    
    search_button = ft.Container(
        content = ft.IconButton(icon = ft.Icons.SEARCH, icon_color = search_icon_color, bgcolor = transparent_black, on_click = lambda e: call_weather(search_bar)), #NEED TO ADD THE GET_WEATHER FUNCTION
        padding = ft.padding.only(top = 10),
    )

    temp_button = ft.Container(
        content = ft.ElevatedButton(text="\u0B00F", )
    )

    section_divider = ft.Divider(
        color = divider_color,
        leading_indent = 10,
        trailing_indent = 10,
        height = 3,
        thickness = 2,
    )

    invisible_divider = ft.Divider(
        color = ft.Colors.TRANSPARENT,
        thickness = 5,
    )

    city_container = ft.Container(
        content = ft.Text(value = "City_Name", size = 25, weight = 'w300'),
        padding = ft.padding.only(left = width/16, bottom = -height/85),
    )
    location_icon = ft.Container(
        content = ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, color='white', size=25),
        padding = ft.padding.only(left = -width/40, bottom = -height/85)
    )

    current_temp_container = ft.Container(
        content = ft.Text(value=f'--\u00B0F', size=45),
        padding  =ft.padding.only(top = -height/85, left = width/16),
        width = 150
    )

    max_min_container = ft.Container(
        width = width/5, height=width/5,
        bgcolor = transparent_black,
        border_radius = 10,
        padding = ft.padding.only(left = width/3.3)
    )

    def temp_container(padding_value):
        template1 = ft.Container(
            content = ft.Text(value = f'--\u00B0F', size = 20, text_align = ft.TextAlign.CENTER),
            padding = padding_value,
            width = max_min_container.width, height = max_min_container.height,
        )
        return(template1)

    max_temp_container = temp_container(padding_value = ft.padding.only(top = 5))
    min_temp_container = temp_container(padding_value = ft.padding.only(top = 45))

    max_min_stack = ft.Container(
        content = ft.Stack(
            controls = [
                max_min_container,
                max_temp_container,
                min_temp_container,
            ]
        ), padding = ft.padding.only(left = width/3.3)
    )

    weather_desc_container = ft.Container(
        content = ft.Text(value = "Weather Description", size = 17, weight = 'w600'),
        padding = ft.padding.only(left = width/16, top = -height/34),
    )

    feels_like_container = ft.Container(
        content = ft.Text(value = f'Feels like --\u00B0F', size = 17, weight = 'w600'),
        padding = ft.padding.only(left = width/16, top = -height/75),
    )

    def sun_time_container(color_gradient, sun_time, text_color, time_value):
        template2 = ft.Container(
            width = width*0.40,
            height = height/10,
            gradient = ft.LinearGradient(
                begin = ft.alignment.center_left,
                end = ft.alignment.center_right,
                colors = color_gradient,
                tile_mode = ft.GradientTileMode.CLAMP
            ),
            border_radius = 50
        )
        template_stack = ft.Stack([
            template2,
            ft.Container(
                content = ft.Text(value = sun_time, color = text_color, size = 17, weight = 'w600'), 
                width = template2.width, height = template2.height, alignment = ft.alignment.top_center
            ),
            ft.Container(
                content = ft.Text(value = time_value, color = text_color, size = 25),
                padding = ft.padding.only(top = 10),
                alignment = ft.alignment.center,
                width = template2.width, height = template2.height
            )
        ])
        return(template_stack)

    sunrise_stack = sun_time_container(color_gradient = sunrise_gradient, sun_time = 'Sun Rise', text_color = sunset_gradient[1], time_value = f'--:-- AM')
    sunset_stack = sun_time_container(color_gradient = sunset_gradient, sun_time = 'Sun Set', text_color = sunrise_gradient[1], time_value = f'--:-- PM')

    def weather_info_container(icon_value, text_value, info_value):
        info_box = ft.Container(
            width = width*0.40,
            height = height/13,
            bgcolor = transparent_black,
            border_radius = 25,
        )

        info_stack = ft.Container(
            content = ft.Stack(
                [
                    info_box,
                    ft.Row([
                        ft.Container(ft.Icon(icon_value, size = 24), padding = ft.padding.only(left = 10, top = 10)),
                        ft.Container(ft.Text(value = text_value, size = 15, weight = 'w300'), padding = ft.padding.only(left = -5, top = 10))
                        ]),
                    ft.Container(
                        content = ft.Text(value = info_value, text_align = ft.TextAlign.LEFT, weight = 'w600', size=20),
                        padding = ft.padding.only(top = height/30, left = 25, bottom = 15),
                        alignment = ft.alignment.center_left
                    )
                ]
            )
        )
        return(info_stack)

    wind_stack = weather_info_container(icon_value = ft.Icons.AIR, text_value = 'Wind Speed', info_value = f'-- km/hr')
    humidity_stack = weather_info_container(icon_value = ft.Icons.GRAIN, text_value = 'Humidity', info_value = f'-- %')
    pressure_stack = weather_info_container(icon_value = ft.Icons.SPEED, text_value = 'Pressure', info_value = f'-- hPa')
    visibility_stack = weather_info_container(icon_value = ft.Icons.REMOVE_RED_EYE, text_value = 'Visibility', info_value = f'---- m')
    sea_lvl_stack = weather_info_container(icon_value = ft.Icons.WATER, text_value = 'Sea Level', info_value = f'---- m')
    ground_lvl_stack = weather_info_container(icon_value = ft.Icons.GRASS, text_value = 'Ground Level', info_value = f'---- m')

    weather_info_column = ft.Column(
        controls = [
            ft.Row([wind_stack, humidity_stack], alignment = ft.MainAxisAlignment.CENTER),
            ft.Row([pressure_stack, visibility_stack], alignment = ft.MainAxisAlignment.CENTER),
            ft.Row([sea_lvl_stack, ground_lvl_stack], alignment = ft.MainAxisAlignment.CENTER),
        ],
    )

    error_container = ft.Container(
        content = ft.Text(value = f'', color = error_text_color, size = 25, weight = 'w600'),
        padding = ft.padding.only(top = 20)
    )

    # gui_values = {search_bar.content.value, city_container.content.value, current_temp_container.content.value, max_temp_container.content.value,
    #                         min_temp_container.content.value, weather_desc_container.content.value, feels_like_container.content.value,
    #                           sunrise_stack.controls[2].content.value, sunset_stack.controls[2].content.value, wind_stack.content.controls[2].content.value,
    #                             humidity_stack.content.controls[2].content.value, pressure_stack.content.controls[2].content.value,
    #                               visibility_stack.content.controls[2].content.value, sea_lvl_stack.content.controls[2].content.value,
    #                                 ground_lvl_stack.content.controls[2].content.value, error_container.content.value}

    gui_values = {
        "search_bar": search_bar.content,
        "city_name": city_container.content,
        "current_temp": current_temp_container.content,
        "max_temp": max_temp_container.content,
        "min_temp": min_temp_container.content,
        "weather_desc": weather_desc_container.content,
        "feels_like": feels_like_container.content,
        "sunrise": sunrise_stack.controls[2].content,
        "sunset": sunset_stack.controls[2].content,
        "wind_speed": wind_stack.content.controls[2].content,
        "humidity": humidity_stack.content.controls[2].content,
        "pressure": pressure_stack.content.controls[2].content,
        "visibility": visibility_stack.content.controls[2].content,
        "sea_lvl": sea_lvl_stack.content.controls[2].content,
        "ground_lvl": ground_lvl_stack.content.controls[2].content,
        "error": error_container.content,
    }

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
                section_divider,
                ft.Row([city_container, location_icon]), 
                ft.Row([current_temp_container, max_min_stack]),
                ft.Row([weather_desc_container]),
                ft.Row([feels_like_container]),
                invisible_divider,
                ft.Row([sunrise_stack, sunset_stack], alignment = ft.MainAxisAlignment.CENTER),
                invisible_divider,
                weather_info_column,
                ft.Row([error_container], alignment = ft.MainAxisAlignment.CENTER)
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
        padding = ft.padding.only(top = 25),
        border_radius = 10,
    )

    page.add(body)

ft.app(target = main)