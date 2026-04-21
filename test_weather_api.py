import requests

# 和风天气API配置
WEATHER_API_KEY = '54d446e1fbc041bd9ed69ac9b32b02a6'

# 测试标准和风天气API地址
def test_standard_api():
    print("测试标准和风天气API地址...")
    url = 'https://geoapi.qweather.com/v2/city/lookup'
    params = {
        'key': WEATHER_API_KEY,
        'location': '北京'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        data = response.json()
        print(f"响应数据: {data}")
    except Exception as e:
        print(f"错误: {e}")

# 测试用户提供的API地址
def test_user_api():
    print("\n测试用户提供的API地址...")
    WEATHER_API_HOST = 'mq59fddrfk.re.qweatherapi.com'
    url = f'https://{WEATHER_API_HOST}/v2/city/lookup'
    params = {
        'key': WEATHER_API_KEY,
        'location': '北京'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        data = response.json()
        print(f"响应数据: {data}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == '__main__':
    test_standard_api()
    test_user_api()
