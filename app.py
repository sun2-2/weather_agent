from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 和风天气API配置
WEATHER_API_KEY = '54d446e1fbc041bd9ed69ac9b32b02a6'
WEATHER_API_HOST = 'mq59fddrfk.re.qweatherapi.com'

class WeatherAPI:
    """和风天气API封装"""
    
    def __init__(self, api_key, api_host):
        self.api_key = api_key
        self.api_host = api_host
    
    def search_city(self, city_name):
        """搜索城市，获取location ID"""
        url = f'https://{self.api_host}/v2/city/lookup'
        params = {
            'key': self.api_key,
            'location': city_name
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('code') == '200' and data.get('location'):
                return data['location'][0]
            return None
        except Exception as e:
            print(f"城市搜索失败: {e}")
            return None
    
    def get_current_weather(self, location_id):
        """获取实时天气"""
        url = f'https://{self.api_host}/v7/weather/now'
        params = {
            'key': self.api_key,
            'location': location_id
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('code') == '200' and data.get('now'):
                return data['now']
            return None
        except Exception as e:
            print(f"获取实时天气失败: {e}")
            return None
    
    def get_forecast(self, location_id):
        """获取天气预报"""
        url = f'https://{self.api_host}/v7/weather/7d'
        params = {
            'key': self.api_key,
            'location': location_id
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('code') == '200' and data.get('daily'):
                return data['daily']
            return None
        except Exception as e:
            print(f"获取天气预报失败: {e}")
            return None
    
    def get_alert(self, location_id):
        """获取天气预警"""
        url = f'https://{self.api_host}/v7/warning/now'
        params = {
            'key': self.api_key,
            'location': location_id
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('code') == '200' and data.get('warning'):
                return data['warning']
            return []
        except Exception as e:
            print(f"获取天气预警失败: {e}")
            return []

# 初始化天气API实例
weather_api = WeatherAPI(WEATHER_API_KEY, WEATHER_API_HOST)

@app.route('/')
def index():
    """首页路由"""
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    """天气查询路由"""
    city = request.args.get('city')
    if not city:
        return jsonify({'error': '请输入城市名称'}), 400
    
    # 搜索城市
    city_info = weather_api.search_city(city)
    if not city_info:
        return jsonify({'error': '未找到该城市'}), 404
    
    # 获取实时天气
    current_weather = weather_api.get_current_weather(city_info['id'])
    if not current_weather:
        return jsonify({'error': '获取天气信息失败'}), 500
    
    # 构建响应数据
    weather_data = {
        'city': city_info['name'],
        'temperature': f"{current_weather['temp']}°C",
        'description': current_weather['text'],
        'humidity': f"{current_weather['humidity']}%",
        'wind': f"{current_weather['windDir']} {current_weather['windSpeed']}km/h"
    }
    
    return jsonify(weather_data)

@app.route('/forecast', methods=['GET'])
def get_forecast():
    """天气预报路由"""
    city = request.args.get('city')
    if not city:
        return jsonify({'error': '请输入城市名称'}), 400
    
    # 搜索城市
    city_info = weather_api.search_city(city)
    if not city_info:
        return jsonify({'error': '未找到该城市'}), 404
    
    # 获取天气预报
    forecast = weather_api.get_forecast(city_info['id'])
    if not forecast:
        return jsonify({'error': '获取天气预报失败'}), 500
    
    # 构建响应数据
    forecast_data = {
        'city': city_info['name'],
        'forecast': []
    }
    
    for day in forecast:
        forecast_data['forecast'].append({
            'date': day['date'],
            'temp_max': f"{day['tempMax']}°C",
            'temp_min': f"{day['tempMin']}°C",
            'text_day': day['textDay'],
            'text_night': day['textNight'],
            'precip': f"{day['precip']}mm"
        })
    
    return jsonify(forecast_data)

@app.route('/alert', methods=['GET'])
def get_alert():
    """天气预警路由"""
    city = request.args.get('city')
    if not city:
        return jsonify({'error': '请输入城市名称'}), 400
    
    # 搜索城市
    city_info = weather_api.search_city(city)
    if not city_info:
        return jsonify({'error': '未找到该城市'}), 404
    
    # 获取天气预警
    alerts = weather_api.get_alert(city_info['id'])
    
    # 构建响应数据
    alert_data = {
        'city': city_info['name'],
        'alerts': []
    }
    
    for alert in alerts:
        alert_data['alerts'].append({
            'sender': alert['sender'],
            'pubTime': alert['pubTime'],
            'title': alert['title'],
            'level': alert['level'],
            'text': alert['text']
        })
    
    return jsonify(alert_data)

@app.route('/about')
def about():
    """关于页面路由"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
