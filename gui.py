import flet as ft

def main(page: ft.Page):
    body = ft.Container(bgcolor=ft.Colors.BLUE)

    page.add(body)

ft.app(target=main)