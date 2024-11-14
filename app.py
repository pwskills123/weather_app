import json
import requests
from flask import Flask, request, render_template
from weather.constansts import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict_weather',methods=['POST'])
def predict_weather():
    if request.method == 'POST':
        location = request.form.get('location')
        try:
            response = fetch_weather_data(location)
            weather_data = parse_weather_data(response)
            return render_template('home.html',**weather_data)
        except Exception as e:
            return render_template("home.html",error="Please enter a correct place name.....")
        
def fetch_weather_data(location):
    url = API_URL
    headers = {
        'X-RapidAPI-key': API_KEY,
        'X-RapidAPI-Host': API_HOST
    }

    querystring = {"q":location}

    response = requests.get(url,headers=headers,params=querystring)
    response.raise_for_status()
    return response.json()

def parse_weather_data(data):
    location_data = data['location']
    current_data = data['current']
    return {
        'name': location_data['name'],
        'region': location_data['region'],
        'country': location_data['country'],
        'lat': location_data['lat'],
        'lon': location_data['lon'],
        'tz_id': location_data['tz_id'],
        'localtime_epoch': location_data['localtime_epoch'],
        'localtime': location_data['localtime'],
        'last_updated_epoch': current_data['last_updated_epoch'],
        'last_updated': current_data['last_updated'],
        'temp_c': current_data['temp_c'],
        'temp_f': current_data['temp_f'],
        'is_day': current_data['is_day'],
        'condition_text': current_data['condition']['text'],
        'condition_icon': current_data['condition']['icon'],
        'wind_mph': current_data['wind_mph'],
        'wind_kph': current_data['wind_kph'],
        'wind_degree': current_data['wind_degree'],
        'wind_dir': current_data['wind_dir'],
        'pressure_mb': current_data['pressure_mb'],
        'pressure_in': current_data['pressure_in'],
        'precip_mm': current_data['precip_mm'],
        'precip_in': current_data['precip_in'],
        'humidity': current_data['humidity'],
        'cloud': current_data['cloud'],
        'feelslike_c': current_data['feelslike_c'],
        'feelslike_f': current_data['feelslike_f'],
        'vis_km': current_data['vis_km'],
        'vis_miles': current_data['vis_miles'],
        'uv': current_data['uv'],
        'gust_mph': current_data['gust_mph'],
        'gust_kph': current_data['gust_kph'],
    }


if __name__ == '__main__':
    app.run(debug=True)

