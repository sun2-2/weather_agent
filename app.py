from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# 和风天气API配置
WEATHER_API_KEY = '54d446e1fbc041bd9ed69ac9b32b02a6'
WEATHER_API_HOST = 'mq59fddrfk.re.qweatherapi.com'

# DeepSeek API配置
DEEPSEEK_API_KEY = 'sk-20618fcccd074def8a5e9b2d4ae6ec3b'
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

class WeatherAPI:
    """和风天气API封装"""
    
    def __init__(self, api_key, api_host):
        self.api_key = api_key
        self.api_host = api_host
        self.base_url = f'https://{api_host}'
    
    def search_city(self, city_name):
        """搜索城市，获取location ID"""
        # 暂时硬编码一些主要城市的location信息
        city_mapping = {
            '北京': {'id': '101010100', 'name': '北京'},
            '上海': {'id': '101020100', 'name': '上海'},
            '广州': {'id': '101280101', 'name': '广州'},
            '深圳': {'id': '101280601', 'name': '深圳'},
            '杭州': {'id': '101210101', 'name': '杭州'}
        }
        
        # 转换为小写进行匹配
        city_name_lower = city_name.lower()
        for city in city_mapping:
            if city.lower() == city_name_lower:
                print(f"找到城市: {city}")
                return city_mapping[city]
        
        # 如果没有找到，返回None
        print(f"未找到城市: {city_name}")
        return None
    
    def get_current_weather(self, location_id):
        """获取实时天气"""
        url = f'{self.base_url}/v7/weather/now'
        params = {
            'key': self.api_key,
            'location': location_id
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"实时天气响应状态码: {response.status_code}")
            print(f"实时天气响应内容: {response.text}")
            
            if not response.text:
                print("实时天气响应为空")
                return None
                
            data = response.json()
            if data.get('code') == '200' and data.get('now'):
                return data['now']
            else:
                print(f"获取实时天气失败，代码: {data.get('code')}")
                return None
        except Exception as e:
            print(f"获取实时天气失败: {e}")
            return None
    
    def get_forecast(self, location_id):
        """获取天气预报"""
        url = f'{self.base_url}/v7/weather/7d'
        params = {
            'key': self.api_key,
            'location': location_id
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"天气预报响应状态码: {response.status_code}")
            print(f"天气预报响应内容: {response.text}")
            
            if not response.text:
                print("天气预报响应为空")
                return None
                
            data = response.json()
            if data.get('code') == '200' and data.get('daily'):
                return data['daily']
            else:
                print(f"获取天气预报失败，代码: {data.get('code')}")
                return None
        except Exception as e:
            print(f"获取天气预报失败: {e}")
            return None
    
    def get_alert(self, location_id):
        """获取天气预警"""
        url = f'{self.base_url}/v7/warning/now'
        params = {
            'key': self.api_key,
            'location': location_id
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"天气预警响应状态码: {response.status_code}")
            print(f"天气预警响应内容: {response.text}")
            
            if not response.text:
                print("天气预警响应为空")
                return []
                
            data = response.json()
            if data.get('code') == '200' and data.get('warning'):
                return data['warning']
            else:
                print(f"获取天气预警失败，代码: {data.get('code')}")
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

@app.route('/chat', methods=['POST'])
def chat():
    """聊天功能路由"""
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': '请输入消息'}), 400
    
    try:
        # 调用DeepSeek API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        }
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': '你是一个智能天气助手，除了回答天气相关问题外，也可以回答其他一般问题。'}, 
                {'role': 'user', 'content': message}
            ],
            'temperature': 0.7
        }
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response_data = response.json()
        
        if 'choices' in response_data and response_data['choices']:
            reply = response_data['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            return jsonify({'error': '获取回复失败'}), 500
    except Exception as e:
        print(f"聊天请求失败: {e}")
        return jsonify({'error': '聊天服务暂时不可用'}), 500

if __name__ == '__main__':
    app.run(debug=True)
