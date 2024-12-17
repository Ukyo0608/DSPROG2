import requests
import sqlite3
import datetime
import flet as ft

# データベースの初期化
conn = sqlite3.connect('weather.db', check_same_thread=False)
cursor = conn.cursor()

# 既存のテーブルがある場合は削除
cursor.execute('DROP TABLE IF EXISTS weather_forecasts')
cursor.execute('DROP TABLE IF EXISTS areas_by_region')

# Weather forecasts テーブルの作成
cursor.execute('''CREATE TABLE IF NOT EXISTS weather_forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    area_code INT,
                    weather_code INT,
                    weather TEXT,
                    wind TEXT,
                    max_temp INT,
                    min_temp INT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS areas_by_region (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    region TEXT,
                    prefecture TEXT,
                    area_code TEXT
                )''')

conn.commit()

AREA_JSON_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

# 天気コードと天気情報のマッピングをグローバルに配置
weather_data = {
  '100': ('晴れ', "https://www.jma.go.jp/bosai/forecast/img/100.svg"),
    '101': ('晴れ 時々 くもり', "https://www.jma.go.jp/bosai/forecast/img/101.svg"),
    '102': ('晴れ 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '103': ('晴れ 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '104': ('晴れ 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/104.svg"),
    '105': ('晴れ 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/104.svg"),
    '106': ('晴れ 一時 雨か雪', "https://www.jma.go.jp/bosai/forecast/img/104.svg"),
    '107': ('晴れ 一時 雨か雪', "https://www.jma.go.jp/bosai/forecast/img/104.svg"),
    '108': ('晴れ 一時 雨か雷雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '110': ('晴れ のち時々 くもり', "https://www.jma.go.jp/bosai/forecast/img/110.svg"),
    '111': ('晴れ のち くもり', "https://www.jma.go.jp/bosai/forecast/img/110.svg"),
    '112': ('晴れ のち一時 雨', "https://www.jma.go.jp/bosai/forecast/img/112.svg"),
    '113': ('晴れ のち一時 雨', "https://www.jma.go.jp/bosai/forecast/img/112.svg"),
    '114': ('晴れ のち 雨', "https://www.jma.go.jp/bosai/forecast/img/112.svg"),
    '115': ('晴れ のち一時 雪', "https://www.jma.go.jp/bosai/forecast/img/115.svg"),
    '116': ('晴れ のち一時 雪', "https://www.jma.go.jp/bosai/forecast/img/115.svg"),
    '117': ('晴れ のち 雪', "https://www.jma.go.jp/bosai/forecast/img/115.svg"),
    '118': ('晴れ のち 雨か雪', "https://www.jma.go.jp/bosai/forecast/img/115.svg"),
    '119': ('晴れ のち 雨か雷雨', "https://www.jma.go.jp/bosai/forecast/img/112.svg"),
    '120': ('晴れ 朝夕 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '121': ('晴れ 朝の内一時 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '122': ('晴れ 夕方一時 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '123': ('晴れ 山沿い 雷雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '124': ('晴れ 山沿い 雪', "https://www.jma.go.jp/bosai/forecast/img/104.svg"),
    '125': ('晴れ 午後は雷雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '126': ('晴れ 昼頃から 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '127': ('晴れ 夕方から 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '128': ('晴れ 夜は 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '129': ('晴れ 夜半から 雨', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '130': ('朝の内 霧 後 晴れ', "https://www.jma.go.jp/bosai/forecast/img/100.svg"),
    '131': ('晴れ 明け方 霧', "https://www.jma.go.jp/bosai/forecast/img/100.svg"),
    '132': ('晴れ 朝夕 くもり', "https://www.jma.go.jp/bosai/forecast/img/101.svg"),
    '140': ('晴れ 時々 雨で雷を伴う', "https://www.jma.go.jp/bosai/forecast/img/102.svg"),
    '160': ('晴れ 一時 雪か雨', "https://www.jma.go.jp/bosai/forecast/img/104.svg"),
    '170': ('晴れ 一時 雪か雨', "https://www.jma.go.jp/bosai/forecast/img/104.svg"),
    '181': ('晴れ のち 雪か雨', "https://www.jma.go.jp/bosai/forecast/img/115.svg"),
    '200': ('くもり', "https://www.jma.go.jp/bosai/forecast/img/200.svg"),
    '201': ('くもり 時々 晴れ', "https://www.jma.go.jp/bosai/forecast/img/201.svg"),
    '202': ('くもり 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '203': ('くもり 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '204': ('くもり 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '205': ('くもり 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '206': ('くもり 一時 雨か雪', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '207': ('くもり 一時 雨か雪', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '208': ('くもり 一時 雨か雷雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '209': ('霧', "https://www.jma.go.jp/bosai/forecast/img/200.svg"),
    '210': ('くもり のち 時々 晴れ', "https://www.jma.go.jp/bosai/forecast/img/210.svg"),
    '211': ('くもり のち 晴れ', "https://www.jma.go.jp/bosai/forecast/img/210.svg"),
    '212': ('くもり のち 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/212.svg"),
    '213': ('くもり のち 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/212.svg"),
    '214': ('くもり のち 雨', "https://www.jma.go.jp/bosai/forecast/img/212.svg"),
    '215': ('くもり のち 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/215.svg"),
    '216': ('くもり のち 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/215.svg"),
    '217': ('くもり のち 雪', "https://www.jma.go.jp/bosai/forecast/img/215.svg"),
    '218': ('くもり のち 雨か雪', "https://www.jma.go.jp/bosai/forecast/img/215.svg"),
    '219': ('くもり のち 雨か雷雨', "https://www.jma.go.jp/bosai/forecast/img/212.svg"),
    '220': ('くもり 朝夕 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '221': ('くもり 朝の内一時 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '222': ('くもり 夕方 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '223': ('くもり 日中 時々 晴れ', "https://www.jma.go.jp/bosai/forecast/img/201.svg"),
    '224': ('くもり 昼頃から 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '225': ('くもり 夕方から 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '226': ('くもり 夜は 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '227': ('くもり 夜半から 雨', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '228': ('くもり 昼頃から 雪', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '229': ('くもり 夕方から 雪', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '230': ('くもり 夜は 雪', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '231': ('くもり 海上海岸は霧か霧雨', "https://www.jma.go.jp/bosai/forecast/img/200.svg"),
    '240': ('くもり 時々 雨で雷を伴う', "https://www.jma.go.jp/bosai/forecast/img/202.svg"),
    '250': ('くもり 時々 雪で雷を伴う', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '260': ('くもり 一時 雪か雨', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '270': ('くもり 一時 雪か雨', "https://www.jma.go.jp/bosai/forecast/img/204.svg"),
    '281': ('くもり のち 雪か雨', "https://www.jma.go.jp/bosai/forecast/img/215.svg"),
    '300': ('雨', "https://www.jma.go.jp/bosai/forecast/img/300.svg"),
    '301': ('雨 時々 晴れ', "https://www.jma.go.jp/bosai/forecast/img/301.svg"),
    '302': ('雨 時々止む', "https://www.jma.go.jp/bosai/forecast/img/302.svg"),
    '303': ('雨 時々 雪', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '304': ('雨か雪', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '306': ('大雨', "https://www.jma.go.jp/bosai/forecast/img/300.svg"),
    '307': ('風雨共に強い', "https://www.jma.go.jp/bosai/forecast/img/300.svg"),
    '308': ('雨で暴風を伴う', "https://www.jma.go.jp/bosai/forecast/img/308.svg"),
    '309': ('雨 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '311': ('雨 のち 晴れ', "https://www.jma.go.jp/bosai/forecast/img/311.svg"),
    '313': ('雨 のち くもり', "https://www.jma.go.jp/bosai/forecast/img/313.svg"),
    '314': ('雨 のち 時々 雪', "https://www.jma.go.jp/bosai/forecast/img/314.svg"),
    '315': ('雨 のち 雪', "https://www.jma.go.jp/bosai/forecast/img/314.svg"),
    '316': ('雨か雪 のち 晴れ', "https://www.jma.go.jp/bosai/forecast/img/311.svg"),
    '317': ('雨か雪 のち くもり', "https://www.jma.go.jp/bosai/forecast/img/313.svg"),
    '320': ('朝の内雨 のち 晴れ', "https://www.jma.go.jp/bosai/forecast/img/311.svg"),
    '321': ('朝の内雨 のち くもり', "https://www.jma.go.jp/bosai/forecast/img/313.svg"),
    '322': ('雨 朝晩 一時 雪', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '323': ('雨 昼頃から 晴れ', "https://www.jma.go.jp/bosai/forecast/img/311.svg"),
    '324': ('雨 夕方から 晴れ', "https://www.jma.go.jp/bosai/forecast/img/311.svg"),
    '325': ('雨 夜は 晴', "https://www.jma.go.jp/bosai/forecast/img/311.svg"),
    '326': ('雨 夕方から 雪', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '327': ('雨 夜は 雪', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '328': ('雨 一時強く降る', "https://www.jma.go.jp/bosai/forecast/img/300.svg"),
    '329': ('雨 一時 みぞれ', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '340': ('雪か雨', "https://www.jma.go.jp/bosai/forecast/img/303.svg"),
    '350': ('雨で雷を伴う', "https://www.jma.go.jp/bosai/forecast/img/300.svg"),
    '361': ('雪か雨 のち 晴れ', "https://www.jma.go.jp/bosai/forecast/img/311.svg"),
    '371': ('雪か雨 のち くもり', "https://www.jma.go.jp/bosai/forecast/img/313.svg"),
    '400': ('雪', "https://www.jma.go.jp/bosai/forecast/img/400.svg"),
    '401': ('雪 時々 晴れ', "https://www.jma.go.jp/bosai/forecast/img/401.svg"),
    '402': ('雪 時々止む', "https://www.jma.go.jp/bosai/forecast/img/402.svg"),
    '403': ('雪 時々 雨', "https://www.jma.go.jp/bosai/forecast/img/403.svg"),
    '405': ('大雪', "https://www.jma.go.jp/bosai/forecast/img/400.svg"),
    '406': ('風雪強い', "https://www.jma.go.jp/bosai/forecast/img/406.svg"),
    '407': ('暴風雪', "https://www.jma.go.jp/bosai/forecast/img/406.svg"),
    '409': ('雪 一時 雨', "https://www.jma.go.jp/bosai/forecast/img/403.svg"),
    '411': ('雪 のち 晴れ', "https://www.jma.go.jp/bosai/forecast/img/411.svg"),
    '413': ('雪 のち くもり', "https://www.jma.go.jp/bosai/forecast/img/413.svg"),
    '414': ('雪 のち 雨', "https://www.jma.go.jp/bosai/forecast/img/414.svg"),
    '420': ('朝の内雪 のち 晴れ', "https://www.jma.go.jp/bosai/forecast/img/411.svg"),
    '421': ('朝の内雪 のち くもり', "https://www.jma.go.jp/bosai/forecast/img/413.svg"),
    '422': ('雪 昼頃から 雨', "https://www.jma.go.jp/bosai/forecast/img/414.svg"),
    '423': ('雪 夕方から 雨', "https://www.jma.go.jp/bosai/forecast/img/414.svg"),
    '424': ('雪 夜半から 雨', "https://www.jma.go.jp/bosai/forecast/img/414.svg"),
    '425': ('雪 一時強く降る', "https://www.jma.go.jp/bosai/forecast/img/400.svg"),
    '426': ('雪 のち みぞれ', "https://www.jma.go.jp/bosai/forecast/img/403.svg"),
    '427': ('雪 一時 みぞれ', "https://www.jma.go.jp/bosai/forecast/img/403.svg"),
    '450': ('雪で雷を伴う', "https://www.jma.go.jp/bosai/forecast/img/400.svg")
}

# 地域マッピングの定義をグローバルに配置
region_mappings = {
    "01": "北海道",
    "02": "東北",
    "03": "東北",
    "04": "東北",
    "05": "東北",
    "06": "東北",
    "07": "東北",
    "08": "東北",
    "09": "関東",
    "10": "関東",
    "11": "関東",
    "12": "関東",
    "13": "関東",
    "14": "関東",
    "15": "中部",
    "16": "中部",
    "17": "中部",
    "18": "中部",
    "19": "中部",
    "20": "中部",
    "21": "中部",
    "22": "中部",
    "23": "中部",
    "24": "近畿",
    "25": "近畿",
    "26": "近畿",
    "27": "近畿",
    "28": "近畿",
    "29": "近畿",
    "30": "近畿",
    "31": "中国",
    "32": "中国",
    "33": "中国",
    "34": "中国",
    "35": "中国",
    "36": "四国",
    "37": "四国",
    "38": "四国",
    "39": "四国",
    "40": "九州・沖縄",
    "41": "九州・沖縄",
    "42": "九州・沖縄",
    "43": "九州・沖縄",
    "44": "九州・沖縄",
    "45": "九州・沖縄",
    "46": "九州・沖縄",
    "47": "九州・沖縄"
}

# エリア情報を取得する関数
def get_area_info():
    try:
        response = requests.get(AREA_JSON_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve area information: {e}")
        return None

# データベースに天気情報を保存する関数
def fetch_and_save_weather_forecast(area_code):
    url = FORECAST_URL_TEMPLATE.format(area_code=area_code)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        time_series = data[0]["timeSeries"]
        weather_areas = time_series[0]["areas"]
        dates = time_series[0]["timeDefines"]
        weathers = weather_areas[0]["weathers"]
        winds = weather_areas[0]["winds"]

        temp_info_section = next((ts for ts in time_series if 'temps' in ts["areas"][0]), None)
        max_temps = min_temps = ["データ未取得"] * len(dates)
        if temp_info_section:
            temps = temp_info_section["areas"][0]["temps"]
            max_temps = temps[1::2]
            min_temps = temps[0::2]

        for i in range(len(dates)):
            if i < len(dates):
                date_str = datetime.datetime.fromisoformat(dates[i]).strftime('%Y-%m-%d')
                weather_code = weather_areas[0]["weatherCodes"][i] if i < len(weather_areas[0]["weatherCodes"]) else "999"
                weather = weathers[i] if i < len(weathers) else None
                wind = winds[i] if i < len(winds) else None
                max_temp = max_temps[i] if i < len(max_temps) else None
                min_temp = min_temps[i] if i < len(min_temps) else None
                cursor.execute('''
                    INSERT OR REPLACE INTO weather_forecasts (date, area_code, weather_code, weather, wind, max_temp, min_temp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (date_str, area_code, weather_code, weather, wind, max_temp, min_temp))
        
        conn.commit()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve weather forecast for area code {area_code}: {e}")

# 都道府県情報と天気情報を取得してデータベースに保存
def save_area_and_weather_data():
    area_info = get_area_info()
    if area_info:
        for area_code, details in area_info['offices'].items():
            region = region_mappings.get(area_code[:2])
            if region:
                cursor.execute('''
                    INSERT OR REPLACE INTO areas_by_region (region, prefecture, area_code)
                    VALUES (?, ?, ?)
                ''', (region, details['name'], area_code))
                fetch_and_save_weather_forecast(area_code)

save_area_and_weather_data()

# データベースから地域の都道府県名を取得
def get_area_names(region):
    cursor.execute("SELECT prefecture, area_code FROM areas_by_region WHERE region=?", (region,))
    areas = cursor.fetchall()
    return {area[0]: {"code": area[1]} for area in areas}

# データベースから指定日付の天気情報を取得
def get_weather_for_date(area_code, date):
    cursor.execute('''
        SELECT weather_code, weather, wind, max_temp, min_temp
        FROM weather_forecasts
        WHERE area_code = ? AND date = ?
    ''', (area_code, date))
    return cursor.fetchone()

# 地域に基づいて都道府県のリストタイルを作成

def build_list_tiles(region, on_select, regions_data):
    """地域に基づいて選択された都道府県のリストタイルを作成"""
    list_tiles = []
    areas = get_area_names(region)
    
    for area_name, details in areas.items():
        area_code = details['code']
        list_tile = ft.ListTile(
            title=ft.Text(area_name),
            on_click=lambda e, code=area_code, name=area_name: on_select(e, code, name)
        )
        list_tiles.append(list_tile)
    return list_tiles

def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.width = 1000  

    region_label = ft.Text(value="地方を選択してください", size=24)
    weather_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    prefecture_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    regions_data = {
        "北海道": {},
        "東北": {},
        "関東": {},
        "中部": {},
        "近畿": {},
        "中国": {},
        "四国": {},
        "九州・沖縄": {}
    }

    JAPAN_REGIONS_KEYS = list(regions_data.keys())

    def on_region_change(e):
        selected_region = JAPAN_REGIONS_KEYS[e.control.selected_index]
        region_label.value = f"{selected_region}の都道府県を選択してください"
        list_tiles = build_list_tiles(selected_region, on_prefecture_select, regions_data)
        prefecture_list.controls.clear()
        for tile in list_tiles:
            prefecture_list.controls.append(tile)
        prefecture_list.update()
        weather_container.controls.clear()
        weather_container.update()

    def on_prefecture_select(e, area_code, prefecture_name):
        region_label.value = f"{prefecture_name}の天気情報を表示"
        page.update()
        weather_container.controls.clear()
        weather_container.update()

        today = datetime.date.today()
        dates = [(today + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(3)]  # 日付を2日に制限

        try:
            for date_str in dates:
                data = get_weather_for_date(area_code, date_str)
                if data:
                    weather_code, weather, wind, max_temp, min_temp = data
                    weather_info = weather_data.get(str(weather_code), ("未知の天気コード", f"https://www.jma.go.jp/bosai/forecast/img/999.svg"))
                    image_url = weather_info[1]

                    forecast_card = ft.Container(
                        content=ft.Column([
                            ft.Text(f"日付: {date_str}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                            ft.Text(f"天気: {weather}", size=18, color=ft.colors.BLACK),
                            ft.Image(src=image_url, width=80, height=80),
                            ft.Text(f"最高気温: {max_temp}℃", size=18, color=ft.colors.RED),
                            ft.Text(f"最低気温: {min_temp}℃", size=18, color=ft.colors.BLUE),
                            ft.Text(f"風: {wind}", size=18, color=ft.colors.BLACK),
                            
                        ]),
                        padding=10,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        alignment=ft.alignment.center,
                        width=500,
                        height=300
                    )
                    weather_container.controls.append(forecast_card)
                else:
                    region_label.value = "天気情報が取得できませんでした。"
        except Exception as e:
            region_label.value = "天気情報の処理中にエラーが発生しました。"
            print(f"Error processing weather data: {e}")

        region_label.update()
        weather_container.update()

    side_nav = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    leading=ft.Text("地域選択"),
    group_alignment=-1,
    destinations=[
        ft.NavigationRailDestination(label=region, icon=ft.icons.SUNNY, selected_icon=ft.icons.SUNNY)
        for region in JAPAN_REGIONS_KEYS
    ],
    on_change=on_region_change,
    expand=True,
    bgcolor=ft.colors.BLUE  
)

    page.add(
        ft.Row([
            ft.Container(
                ft.Column([side_nav], expand=True),
                width=80,
            ),
            ft.Container(
                ft.Column([prefecture_list], expand=True),
                width=350,
            ),
            ft.Container(
                ft.Column([region_label, weather_container], expand=True),
                width=700,
            )
        ], expand=True)
    )

    initial_event = type("Event", (object,), {"control": type("Control", (object,), {"selected_index": 0})})()
    on_region_change(initial_event)

ft.app(target=main)