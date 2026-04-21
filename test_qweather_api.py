import requests

# 和风天气API配置
WEATHER_API_KEY = '54d446e1fbc041bd9ed69ac9b32b02a6'
WEATHER_API_HOST = 'mq59fddrfk.re.qweatherapi.com'

# 测试城市搜索（使用用户提供的API Host）
def test_city_search():
    print("测试城市搜索...")
    url = f'https://{WEATHER_API_HOST}/v2/city/lookup'
    params = {
        'key': WEATHER_API_KEY,
        'location': '北京'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        if response.text:
            data = response.json()
            print(f"响应数据: {data}")
        else:
            print("响应为空")
    except Exception as e:
        print(f"错误: {e}")

# 测试实时天气（使用用户提供的API Host）
def test_current_weather():
    print("\n测试实时天气...")
    # 先搜索城市获取ID
    url = f'https://{WEATHER_API_HOST}/v2/city/lookup'
    params = {
        'key': WEATHER_API_KEY,
        'location': '北京'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"城市搜索状态码: {response.status_code}")
        print(f"城市搜索响应内容: {response.text}")
        if response.text:
            data = response.json()
            if data.get('code') == '200' and data.get('location'):
                location_id = data['location'][0]['id']
                print(f"北京的Location ID: {location_id}")
                
                # 测试实时天气
                weather_url = f'https://{WEATHER_API_HOST}/v7/weather/now'
                weather_params = {
                    'key': WEATHER_API_KEY,
                    'location': location_id
                }
                weather_response = requests.get(weather_url, params=weather_params, timeout=10)
                print(f"天气查询状态码: {weather_response.status_code}")
                print(f"天气查询响应内容: {weather_response.text}")
            else:
                print(f"城市搜索失败，代码: {data.get('code')}")
        else:
            print("城市搜索响应为空")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == '__main__':
    test_city_search()
    test_current_weather()
