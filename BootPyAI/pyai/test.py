import requests

url = "http://127.0.0.1:8001/detect" # 요청보낼 url
message = "Test message" # server로 전송할 message
# file_path = "test2.jpg" # 전송할 image pile 경로(현재 파일과 같은 위치에서)
# file_path = "test_RSL_lineup.jpg" # 전송할 image pile 경로(현재 파일과 같은 위치에서)
file_path = "test_TTH_lineup.jpg" # 전송할 image pile 경로(현재 파일과 같은 위치에서)

with open(file_path, "rb") as file:
    response = requests.post(url, data={"message":message}, files={"file":file})

print(response.json()) # console