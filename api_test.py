import requests
import urllib.parse

# 和风天气API配置
WEATHER_API_KEY = '54d446e1fbc041bd9ed69ac9b32b02a6'

# 测试城市搜索
def test_city_search():
    print("测试城市搜索...")
    city = '北京'
    encoded_city = urllib.parse.quote(city)
    url = f'https://geoapi.qweather.com/v2/city/lookup?key={WEATHER_API_KEY}&location={encoded_city}'
    print(f"请求URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        print(f"响应头: {dict(response.headers)}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_city_search()
