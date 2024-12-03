import requests
import flet as ft
from flet import TextField, Text, Column, Row, Container, AppBar, TextButton, TextStyle, colors

AREA_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

def fetch_area_list():
    response = requests.get(AREA_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching area information: {response.status_code}")
        return None

def fetch_weather_forecast(area_code):
    url = FORECAST_URL_TEMPLATE.format(area_code=area_code)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0]["timeSeries"][0]["areas"][0]  # 簡略化されたデータ処理
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return None

def update_main_view_content(area_code, main_view, page):
    forecast = fetch_weather_forecast(area_code)
    if forecast:
        # 太字で大きなテキストでエリア名を更新
        area_name = Text(f"{forecast['area']['name']} ({area_code})", style=TextStyle(size=24, weight=ft.FontWeight.BOLD, color=colors.BLUE))
        weather_forecast = Text(f"{forecast['weathers'][0]}", style=TextStyle(size=18))
        
        main_view.controls.clear()
        main_view.controls.append(area_name)  # エリア名は大きく、太字で表示
        main_view.controls.append(weather_forecast)  # 天気の詳細は通常のスタイルで表示
    else:
        main_view.controls.clear()
        main_view.controls.append(Text("データがありません。", text_align="center"))
    page.update()

def main(page: ft.Page):
    page.title = "天気予報アプリ"  # アプリのタイトル
    app_bar = AppBar(title=Text("天気予報アプリ"))  # アプリバーのタイトル
    
    main_view = Column(expand=True)  # メインビューの初期化
    sidebar = Column(scroll=ft.ScrollMode.AUTO, width=250)  # サイドバーの初期化

    area_data = fetch_area_list()
    if area_data and "centers" in area_data:
        for code, center in area_data["centers"].items():
            sidebar.controls.append(Text(center["name"], style=TextStyle(size=20, weight=ft.FontWeight.BOLD)))
            for child_code in center["children"]:
                btn = TextButton(
                    content=Text(center["name"] + " (" + child_code + ")"),
                    on_click=lambda e, ac=child_code, mv=main_view, pg=page: update_main_view_content(ac, mv, pg)
                )
                sidebar.controls.append(btn)
    else:
        sidebar.controls.append(Text("地域リストの取得に失敗しました。"))

    # サイドバーとメインビューを含む行をページに追加
    page.add(Row(controls=[Container(content=sidebar, bgcolor=ft.colors.LIGHT_BLUE, padding=10), main_view], expand=True))
    page.appbar = app_bar  # ページのアプリバーを設定

ft.app(target=main)  # アプリの起動