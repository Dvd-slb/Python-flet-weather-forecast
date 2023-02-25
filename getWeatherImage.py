import requests
import sqlite3
import os
import urllib.request


def get_icons():
    with open("secret.txt") as file:
        api_key = file.readline()

    response = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=%C4%8Cesk%C3%A1%20L%C3%ADpa&days=8&aqi=no&alerts=no")
    response.raise_for_status()
    response = response.json()

    connect = sqlite3.connect("icons.db")
    cursor = connect.cursor()

    def icons_down(url, file_name):
        if url != "":
            path = os.getcwd() + "\\assets\\"
            full_path = path + file_name + ".png"
            urllib.request.urlretrieve(url, full_path)
            cursor.execute("UPDATE icons SET done=? WHERE path=? AND description=?", (1, url, file_name))

    def move_downloaded():
        cursor.execute("INSERT INTO downloaded_icons SELECT description, path FROM icons WHERE done=?", (1,))
        cursor.execute("UPDATE icons SET path=?, done=? WHERE done=?", ("", 2, 1))

    def insert_icon(code, description, path):
        cursor.execute("INSERT INTO icons VALUES(?, ?, ?, ?)", (code, description, path, 0))

    def check_doubles(code, description, path_to_down):
        cursor.execute("SELECT code FROM icons WHERE code=?", (code,))
        result = cursor.fetchone()
        if not result:
            insert_icon(code, description, path_to_down)

    for day in response["forecast"]["forecastday"]:
        description = day["day"]["condition"]["text"]
        code = day["day"]["condition"]["code"]
        path_to_down = "http:" + day["day"]["condition"]["icon"]
        if "night" in path_to_down:
            path_to_down = path_to_down.replace("night", "day")
        check_doubles(code, description, path_to_down)
        for icons in day["hour"]:
            description = icons["condition"]["text"]
            code = icons["condition"]["code"]
            path_to_down = "http:" + icons["condition"]["icon"]
            if "night" in path_to_down:
                path_to_down = path_to_down.replace("night", "day")
            check_doubles(code, description, path_to_down)

    cursor.execute("SELECT path, description, done FROM icons")
    urls = cursor.fetchall()
    for url in urls:
        icons_down(url[0], url[1])

    move_downloaded()

    connect.commit()
    connect.close()
