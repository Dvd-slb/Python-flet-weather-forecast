from flet import *
import requests
import datetime
from getWeatherImage import get_icons

with open("secret.txt") as file:
    api_key = file.readline()

response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=%C4%8Cesk%C3%A1%20L%C3%ADpa&days=8&aqi=no&alerts=no")
response.raise_for_status()
response = response.json()

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def main(page: Page):
    page.title = "Weather app"
    page.bgcolor = colors.BLUE_GREY_400
    page.window_width = 400
    page.window_height = 650
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def top_cont_expand(e):
        # FOR MOBILE
        # if central_conteiner.content.controls[1].height < 350:
        #     central_conteiner.content.controls[1].height = 530
        #     central_conteiner.content.controls[1].update()
        # else:
        #     central_conteiner.content.controls[1].height = 600 * 0.41
        #     central_conteiner.content.controls[1].update()

        # FOR DESKTOP
        if e.data == "true":
            central_conteiner.content.controls[1].height = 530
            central_conteiner.content.controls[1].update()
        else:
            central_conteiner.content.controls[1].height = 600 * 0.41
            central_conteiner.content.controls[1].update()

    def current_temp():
        curr_temp = float(response["current"]["temp_c"])
        curr_temp = round(curr_temp)

        curr_weather = response["current"]["condition"]["text"]

        curr_weather_desc = response["current"]["condition"]["text"]

        curr_wind = float(response["current"]["wind_kph"])
        curr_wind = round(curr_wind)

        curr_humidity = int(response["current"]["humidity"])

        curr_feels = float(response["current"]["feelslike_c"])
        curr_feels = round(curr_feels)

        return [curr_temp, curr_weather, curr_weather_desc, curr_wind,
                curr_humidity, curr_feels]

    def current_extra():
        extra_info = []
        sunrise_time = response["forecast"]["forecastday"][0]["astro"]["sunrise"]
        sunset_time = response["forecast"]["forecastday"][0]["astro"]["sunset"]

        extra = [
            [round(int(response["current"]["vis_km"])), " km", "Visibility", "./assets/visibility.png"],
            [round(int(response["current"]["pressure_mb"])), " hPa", "Pressure", "./assets/pressure.png"],
            [sunrise_time, "", "Sunrise", "./assets/sunrise.png"],
            [sunset_time, "", "Sunset", "./assets/sunset.png"],
        ]

        for box in extra:
            one_box = Container(
                bgcolor="white10",
                border_radius=12,
                alignment=alignment.center,
                padding=5,
                content=Column(
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=0,
                    controls=[
                        Container(
                            alignment=alignment.center,
                            width=40,
                            height=40,
                            margin=margin.only(bottom=20),
                            content=Image(src=box[3], color="white")
                        ),
                        Text(
                            str(box[0]) + box[1],
                            color="white",
                            size=14
                        ),
                        Text(
                            box[2],
                            color="white54",
                            size=12
                        )
                    ]
                )
            )
            extra_info.append(one_box)

        return extra_info

    # top container
    def top_part():
        today = current_temp()
        more_info = current_extra()

        today_extra = GridView(
            max_extent=200,
            expand=1,
            run_spacing=10,
            spacing=10,
            controls=more_info,
            padding=padding.only(right=30, left=30),
            )

        top_container = Container(
            width=350,
            height=600 * 0.41,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["lightblue600", "lightblue900"]
            ),
            border_radius=40,
            animate=animation.Animation(duration=400, curve=AnimationCurve.DECELERATE),
            on_hover=lambda e: top_cont_expand(e),
            padding=10,
            content=Column(
                alignment=MainAxisAlignment.START,
                spacing=10,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(
                                "Česká Lípa, CZ",
                                color="white",
                                size=16,
                                weight="w600"
                            )
                        ]
                    ),
                    Container(padding=padding.only(bottom=5)),
                    Row(
                        alignment="center",
                        spacing=90,
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                        width=100,
                                        height=100,
                                        image_src=f"./assets/{today[2]}.png"
                                    )
                                ]
                            ),
                            Column(
                                spacing=0,
                                horizontal_alignment="center",
                                controls=[
                                    Text(
                                        "Today",
                                        size=12,
                                        text_align="center",
                                        color="white",
                                    ),
                                    Container(
                                        margin=-10,
                                        content=Text(
                                            f"{today[0]}°",
                                            size=52,
                                            color="white",
                                            text_align="center"
                                        )
                                    ),
                                    Text(
                                        today[2],
                                        width=140,
                                        max_lines=2,
                                        size=11,
                                        color="white54",
                                        text_align="center",
                                    )
                                ]
                            )
                        ]
                    ),
                    Divider(
                        height=8, thickness=1, color="white10"
                    ),
                    Row(
                        alignment="spaceAround",
                        controls=[
                            Container(
                                content=Column(
                                    horizontal_alignment="center",
                                    spacing=0,
                                    controls=[
                                        Container(
                                            width=25,
                                            height=25,
                                            alignment=alignment.center,
                                            content=Image(src="./assets/wind2.png",
                                                          color="white"),
                                        ),
                                        Text(
                                            str(today[3]) + " km/h",
                                            color="white",
                                            size=12,
                                        ),
                                        Text(
                                            "Wind",
                                            color="white54",
                                            size=11
                                        )
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    spacing=0,
                                    horizontal_alignment="center",
                                    controls=[
                                        Container(
                                            width=25,
                                            height=25,
                                            alignment=alignment.center,
                                            content=Image(src="./assets/humidity.png",
                                                          color="white")
                                        ),
                                        Text(
                                            str(today[4]) + " %",
                                            color="white",
                                            size=12,
                                        ),
                                        Text(
                                            "Humidity",
                                            color="white54",
                                            size=11
                                        )
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    spacing=0,
                                    horizontal_alignment="center",
                                    controls=[
                                        Container(
                                            width=25,
                                            height=25,
                                            alignment=alignment.center,
                                            content=Image(src="./assets/feels.png",
                                                          color="white")
                                        ),
                                        Text(
                                            f"{today[5]}°",
                                            color="white",
                                            size=12
                                        ),
                                        Text(
                                            "Feels like",
                                            color="white54",
                                            size=11
                                        )
                                    ]
                                )
                            )
                        ]
                    ),
                    today_extra
                ]

            )
        )
        return top_container

    def bottom_data():
        day = days[datetime.datetime.weekday(datetime.datetime.fromtimestamp(response["location"]["localtime_epoch"]))]
        day_index = days.index(day)
        another_day = 1

        bot_data = []

        for i in range(1, 3):
            day_name = days[day_index + another_day]
            another_day += 1
            desc = response["forecast"]["forecastday"][i]["day"]["condition"]["text"]

            bot_data.append(
                Row(
                    spacing=5,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Row(
                            expand=1,
                            alignment="start",
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Text(
                                        day_name,
                                        color="white"
                                    )
                                )
                            ]
                        ),
                        Row(
                            expand=1,
                            controls=[
                                Container(
                                    content=Row(
                                        alignment="start",
                                        controls=[
                                            Container(
                                                width=27,
                                                height=27,
                                                alignment=alignment.center_left,
                                                # content=Image(src="./assets/cloudy.png")
                                                content=Image(src=f"./assets/{desc}.png")
                                            ),
                                            Text(
                                                response["forecast"]["forecastday"][i]["day"]["condition"]["text"],
                                                width=115,
                                                max_lines=2,
                                                color="white54",
                                                size=11,
                                                text_align="center"
                                            )
                                        ]
                                    )
                                )
                            ]
                        ),
                        Row(
                            expand=1,
                            alignment="end",
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Row(
                                        alignment="center",
                                        spacing=5,
                                        controls=[
                                            Container(
                                                width=20,
                                                content=Text(
                                                    round(float(response["forecast"]["forecastday"][i]["day"]["maxtemp_c"])),
                                                    color="white",
                                                    text_align="start"
                                                )
                                            ),
                                            Container(
                                                width=20,
                                                content=Text(
                                                    round(float(
                                                        response["forecast"]["forecastday"][i]["day"]["mintemp_c"])),
                                                    color="white",
                                                    text_align="end"
                                                )
                                            ),
                                        ]
                                    )
                                )
                            ]
                        )
                    ]

                )
            )
        return bot_data

    def bottom():
        bot_column = Column(
            alignment="center",
            horizontal_alignment="center",
            spacing=80,
        )

        for data in bottom_data():
            bot_column.controls.append(data)

        bottom_cont = Container(
            padding=padding.only(top=250, left=20, right=20, bottom=20),
            content=bot_column
        )

        return bottom_cont

    central_conteiner = Container(
        width=350,
        height=600,
        bgcolor="black",
        border_radius=40,
        padding=5,
        content=Stack(
            width=330,
            height=550,
            controls=[
                bottom(),
                top_part(),
            ]
        )
    )

    page.add(central_conteiner)


get_icons()

if __name__ == "__main__":
    app(target=main, assets_dir="assets")
