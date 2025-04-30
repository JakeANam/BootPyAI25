# -> pip install fastapi uvicorn pydantic Pillow numpy requests
# pip install ultralytics opencv-python python-multipart
# fastapi : 비동기 웹 framework, 자동 api문서 생성
# uvcorn : 고성능 비동기 server, ASGI 표준 지원
# pydantic : data 검증, 직렬화, type, hinting, 설정 관리
# Pillow : image 열기, 저장, 변환, 다양한 image 처리
# numpy : 수치 계산, 배열 및 행렬 연산, 다양한 수학 함수
# requests : 간단한 http요청 및 응답 처리
# ultralytics : YOLO8 객체 탐지 model 제공 - roboflow 에서 받기 위해
# opencv-python : 이미지 및 video 처리, 컴퓨터 vision 기능(roboflow 대체)
# python-multipart : multipart  form data를 pashing 하기 위해 필요

# uvicorn main:app --reload
# post 요청을 통해 이미지가 전송되면 인공지능 객체 탐지 model을 이용해서 객체 탐지
# 그리고 그 결과 image를 base64 encording된 문자열로 반환하는 service

from fastapi import FastAPI, UploadFile, File, Form
# Routing, File Upload, Form 처리

from pydantic import BaseModel# pydantic의 data model 정의

import io # File 입출력에 필요한 model
import base64 # data를 Base64로 encording & decording
# base64에 대해서는 : https://ko.wikipedia.org/wiki/%EB%B2%A0%EC%9D%B4%EC%8A%A464

from PIL import Image # Pillow image 처리 library
import numpy as np # 배열 및 행렬 연산
from ultralytics import YOLO # yolo8 model 사용
import cv2 # computer vision 작업을 위한 library

# 위 과정에서 error 표시 발생? pip 과정에서 설치가 안 됬을 수도!

app = FastAPI()

model = YOLO('yolov8n.pt') # YOLOv8 model load (yolo8n.pt model의 가중치 file)

class DetectionResult(BaseModel): # pydantic을 사용하여 data model을 정의 (응답 data를 구조화)
    message : str # client가 보낸 message
    image: str # Base64로 encording된 탐지 결과 표시

# 객체 탐지 함수 - 각 개체 탐지를 위한 함수 정의로 model에 image를 넣어 객체를 탐지하고 그 결과에서 bounding box 정보를 추출한 후 image에 binding box와 class이름, 신뢰도를 표시하고 반환
def detect_objects(image: Image):
    img = np.array(image) # image -> numpy 배열로 변환
    results = model(img) # 객체 탐지
    class_names = model.names # class 이름 저장

    # 결과를 bounding box, class name, 정확도로 image에 표시
    for result in results:
        boxes = result.boxes.xyxy # bounding box
        confidences = result.boxes.conf # 신뢰도
        class_ids = result.boxes.cls # class name

        for box, confidences, class_ids in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box) # 좌표를 정수로 변환
            label = class_names[int(class_ids)] # class name
            cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2) # 여기서는 붉은 색으로 box 칠하기
            cv2.putText(img, f'{label}{confidences:.2f}',(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

    result_image = Image.fromarray(img) # 결과 image를 PIL로 변환
    return result_image

@app.get("/") # get 방식의 요청 test용 message를 json 형식으로 반환 - 받는 것
async def read_root():
    return {"message" : "Hello FastAPI"}

@app.post("/detect", response_model=DetectionResult) # 나가는 것, 객체 탐지 end point
async def detect_service(message: str = Form(...), file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))

    if image.mode == 'RGBA' : image = image.convert('RGB')
    elif image.mode != 'RGB' : image = image.convert('RGB')

    result_image = detect_objects(image) # 객체 탐지 수령

    # image 결과를 base64로 encording
    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG") # JPG 형태로 전환
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return DetectionResult(message=message, image=img_str)
    # 결론 : http://localhost:8001/detect 경로에 post 요청 처리 - client로 upload된 image를 읽고 PIL image로 변환하고 alpha channel이 있으면 alpha channel제거
    # https://developer.mozilla.org/ko/docs/Glossary/Alpha
    # 객체 탐지 함수를 호출해서 탐지 결과 image를 얻는다.
    # 탐지 결과 image를 Base64 문자열로 encording
    # DetectionResult model을 사용해서 message와 encording된 image를 json 응답으로 반환


if __name__=="__main__":
    # uvicorn main:app 인 경우 port와 uvicorn 실행
    # spring application 시작 전에 여기부터 실행하고 실행하자!(안그러면 )
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # 생성자

