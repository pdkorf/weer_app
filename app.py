from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
from config import API_KEY, UNSPLASH_ACCESS_KEY

app = Flask(__name__)

def get_city_image(city):
    """Haal een afbeelding op van de skyline van een stad via Unsplash API"""
    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": f"{city} skyline",
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape",
        "per_page": 1
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]
    except Exception as e:
        print(f"Error fetching image: {e}")
    return None

def get_weather(city):
    """Haal het huidige weer op voor een stad"""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "nl"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return {
            'temperatuur': round(data['main']['temp']),
            'beschrijving': data['weather'][0]['description'],
            'luchtvochtigheid': data['main']['humidity'],
            'windsnelheid': round(data['wind']['speed'] * 3.6, 1),
            'icon_code': data['weather'][0]['icon']
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def get_forecast(city):
    """Haal de 5-daagse weersverwachting op"""
    url = f"http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "nl"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        forecast = []
        seen_dates = set()
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            if date not in seen_dates and len(forecast) < 5:
                seen_dates.add(date)
                forecast.append({
                    'datum': date.strftime("%d-%m"),
                    'temp': round(item['main']['temp']),
                    'beschrijving': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'regen': item.get('rain', {}).get('3h', 0),
                    'wind': round(item['wind']['speed'] * 3.6, 1)
                })
        return forecast
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return None

@app.route('/')
def index():
    """Render de hoofdpagina"""
    favorite_cities = ["Amsterdam", "Reykjavik", "Parijs", "New York"]
    return render_template('index.html', favorite_cities=favorite_cities)

@app.route('/weather/<city>')
def weather(city):
    """API endpoint voor weer data"""
    weather_data = get_weather(city)
    forecast_data = get_forecast(city)
    city_image = get_city_image(city)
    
    # Get city coordinates
    try:
        geo_response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={city}")
        geo_data = geo_response.json()
        if geo_data:
            coordinates = {
                'lat': float(geo_data[0]['lat']),
                'lon': float(geo_data[0]['lon'])
            }
        else:
            coordinates = None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        coordinates = None
    
    if weather_data and forecast_data:
        return jsonify({
            'weather': weather_data,
            'forecast': forecast_data,
            'city_image': city_image,
            'coordinates': coordinates
        })
    return jsonify({'error': 'City not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    # Of zonder debug mode voor meer veiligheid:
    # app.run(host='0.0.0.0', port=5000) 