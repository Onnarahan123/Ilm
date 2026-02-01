import requests
import json

# Linnad ja koordinaadid (lisa siia soovi korral juurde)
linnad = [
    {"nimi": "Tallinn", "lat": 59.4370, "lon": 24.7536},
    {"nimi": "Tartu", "lat": 58.3780, "lon": 26.7290},
    {"nimi": "Pärnu", "lat": 58.3859, "lon": 24.4971},
    {"nimi": "Kuressaare", "lat": 58.2532, "lon": 22.4886},
    {"nimi": "Viljandi", "lat": 58.3639, "lon": 25.5900}
]

def get_icon(code):
    # Ilmakoodid emoji'deks
    if code == 0: return "☀️"
    if code in [1, 2, 3]: return "⛅"
    if code in [45, 48]: return "🌫️"
    if code in [51, 53, 55]: return "🌧️"
    if code in [61, 63, 65]: return "☔"
    if code in [71, 73, 75, 77]: return "❄️"
    if code > 80: return "⛈️"
    return "☁️"

data_list = []

print("Alustan ilma laadimist...")
for linn in linnad:
    try:
        # Küsime OpenMeteo API-lt andmeid
        url = f"https://api.open-meteo.com/v1/forecast?latitude={linn['lat']}&longitude={linn['lon']}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        r = requests.get(url, timeout=10)
        meteo = r.json()

        curr = meteo['current_weather']
        daily = meteo['daily']

        data_list.append({
            "nimi": linn['nimi'],
            "temp": round(curr['temperature']),
            "tuul": curr['windspeed'],
            "ikoon": get_icon(curr['weathercode']),
            "min": round(daily['temperature_2m_min'][0]),
            "max": round(daily['temperature_2m_max'][0]),
            "sadu": daily['precipitation_sum'][0]
        })
        print(f"OK: {linn['nimi']}")
    except Exception as e:
        print(f"Viga {linn['nimi']}: {e}")

# Salvestame
with open('ilm.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)
print("Valmis!")
