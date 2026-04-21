import requests

# 和风天气API配置
WEATHER_API_KEY = '54d446e1fbc041bd9ed69ac9b32b02a6'

# 测试不同的API端点
def test_different_endpoints():
    endpoints = [
        f'https://geoapi.qweather.com/v2/city/lookup?key={WEATHER_API_KEY}&location=北京',
        f'https://devapi.qweather.com/v7/weather/now?key={WEATHER_API_KEY}&location=101010100',  # 北京的location ID
        f'https://mq59fddrfk.re.qweatherapi.com/v2/city/lookup?key={WEATHER_API_KEY}&location=北京',
        f'https://mq59fddrfk.re.qweatherapi.com/v7/weather/now?key={WEATHER_API_KEY}&location=101010100'
    ]
    
    for endpoint in endpoints:
        print(f"\n测试端点: {endpoint}")
        try:
            response = requests.get(endpoint, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
        except Exception as e:
            print(f"错误: {e}")

if __name__ == '__main__':
    test_different_endpoints()
