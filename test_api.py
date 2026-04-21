import requests
import urllib.parse

# 测试天气API
def test_weather_api():
    print("测试天气API...")
    # 手动构建URL，确保编码正确
    city = '北京'
    encoded_city = urllib.parse.quote(city)
    url = f'http://127.0.0.1:5000/weather?city={encoded_city}'
    print(f"请求URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        data = response.json()
        print(f"响应数据: {data}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == '__main__':
    test_weather_api()
