import requests
import pandas as pd

deskripsi_cuaca_id = {
    "clear sky": "Cerah",
    "few clouds": "Berawan Sebagian",
    "broken clouds": "Berawan",
    "overcast clouds": "Mendung",
    "moderate rain": "Hujan Sedang",
    "light rain": "Hujan Ringan",
    "shower rain": "Hujan Gerimis",
    "rain": "Hujan",
    "thunderstorm": "Badai Petir",
    "snow": "Salju",
    "mist": "Kabut",
}


def get_cuaca(kota, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={kota}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def analisis_cuaca(data):
    if data is None:
        return None

    forecast_list = data.get("list", [])
    dates = []
    temperatur = []
    humidities = []
    desc_weather = []

    for item in forecast_list:
        date = item["dt_txt"].split(" ")[0]
        dates.append(date)

        temperatur.append(item["main"]["temp"])
        humidities.append(item["main"]["humidity"])

        desc = item["weather"][0]["description"]
        desc_weather.append(deskripsi_cuaca_id.get(desc, desc))

    df = pd.DataFrame(
        {
            "Tanggal": dates,
            "Suhu (k)": temperatur,
            "Kelembapan (%)": humidities,
            "Desc Cuaca": desc_weather,
        }
    )

    df["Suhu (c)"] = df["Suhu (k)"] - 273.15
    df = df.drop(columns=["Suhu (k)"])

    df_daily = (
        df.groupby("Tanggal")
        .agg(
            {
                "Suhu (c)": "mean",
                "Kelembapan (%)": "mean",
                "Desc Cuaca": lambda x: x.mode()[0],
            }
        )
        .reset_index()
    )

    df_daily.index = df_daily.index + 1
    return df_daily


def main():
    kota = input("Masukan Nama Kota: ")
    api_key = ""

    data = get_cuaca(kota, api_key)
    df = analisis_cuaca(data)

    if df is not None:
        print(df.head())


if __name__ == "__main__":
    main()
