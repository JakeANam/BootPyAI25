# 1. 선행 준비
# ip 카메라 준비 -> ipTime의 제조회사의 관련 network설정 -> VMS 프로그램 설치 -> ip, password, rtsp protocol 활성화
# 2. python - front 연동 (mqtt api 활용해서)
# mqtt: 실시간 출력 protocol - 자세한 내용은 https://underflow101.tistory.com/22
# mqtt broker용 program - mosquitto api - 다운로드는  https://mosquitto.org/download/ - 여기서는 mosquitto-2.0.18 사용한다
# mosquitto 환경 설정 변경 - 메모장, 관리자 권한으로 C:\Program Files\mosquitto\mosquitto.conf 열기
    # MQTT 기본 listener 설정
    # listener 1883
    # protocol mqtt
    #
    # # WebSocket listener 설정
    # listener 9001
    # protocol websockets
    #
    # # 익명 접속 허용
    # allow_anonymous true

# 방화볍 설정 추가 실행에서 wf.msc -> 인바운드 규칙 -> 새 규칙 -> 포트 -> 특정 로컬 포트 1883, 9001 -> 연결 허용 -> 도메인, 개인, 공용 check -> 이름, 설명 입력후 마침
# terminal에서 환경설정 적용 실행하자
# terminal에서 cd\ 하면 c:로 이동
# mosquitto 위치에서 mosquitto -c mosquitto.conf -v 입력
# mosquitto version 2.0.18 running - 이렇게 출력되면 OK
# 만약 안된다면 services.msc에서 서비스 재실행
# 이게 실행되야 broker 켜진다 - cmd에서 했으면 cmd 닫지 말 것!

# Network는 환경설정file, services, 방화벽 이렇게 세가지가 한 번에 작동되야 가능하다

import base64
import io
from PIL import Image
import numpy as np
import json

from fontTools.misc.cython import returns
from ultralytics import YOLO
import paho.mqtt.client as mqtt # broker 추가 - service 켜지면 설정
import cv2
import time

model = YOLO('yolov8n.pt')
client = mqtt.Client() # mosquiotto -c mosquiotto.conf
topic = '/camera/objects' # 경로
client.connect('localhost', 1883, 60)

# 연결용 함수
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# 객체 감지용 색상 함수
def get_colors(num_colors):
    np.random.seed(0)
    colors = [tuple(np.random.randint(0, 255, 3).tolist()) for _ in range(num_colors)]
    return colors

class_names = model.names # model에서 받은 class 이름
num_classes = len(class_names) # class 번호
colors = get_colors(num_classes) # 사각 박스 color 색

client.on_connect = on_connect # client 연결 정보
cap = cv2.VideoCapture('rtsp://admin:mbc312AI!!@192.168.0.4:554/mbcai312') # rtsp 정보 (vms 참고)
# https://deep-learning-study.tistory.com/107
# 카메라와 비디오 장치 속성 값 참조 - 컴퓨터 과부화를 조심해서 잘 설정하자!
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # bRec = False
    # prevTime = 0

# --- 전처리 과정 완료 ---

# model이 객체를 탐지하기 위한 함수
def detect_objects(image: np.array):
    results = model(image, verbose=False)
    class_names = model.names

    for result in results:
        boxes = result.boxes.xyxy
        confidences = result.boxes.conf
        class_ids = result.boxes.cls
        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = class_names[int(class_id)]
            cv2.rectangle(image, (x1, y1), (x2, y2), colors[int(class_id)], 2)
            cv2.putText(image, f'{label}{confidence:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, colors[int(class_id)], 2)

    return image

# 객체 탐지 반복용 loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    result_image = detect_objects(frame)

    _, buffer = cv2.imencode('.jpg', result_image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    payload = json.dumps({'image': jpg_as_text})
    client.publish(topic, payload)
    cv2.imshow('Frame', result_image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break # 영상 출력 중에 q가 입력되면 종료

cap.release() # Video Capture
cv2.destroyAllWindows() # 창 닫기
client.disconect() # 연결 해제