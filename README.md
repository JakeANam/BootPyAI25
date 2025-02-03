# BootPyAI25
Java-spring boot, python AI 협업module

주제

카메라로부터 실시간으로 전송된 데이터를 ai 서버에서 객체를 인식하고 대상 물체를 탐지한 후 그 결과를 웹서버에 전송하여 웹 또는 모바일 화면으로 보여줌

파이썬 애플리케이션은 카메라에서 전송된 이미지를 MQTT 브로커를 통해 전송 -> 자바 웹 애플리케이션이 해당 이미지를 받아 웹 화면에 송출

개발환경구축

파이썬 인터프리터 : http://www.python.org/ -> 3.12버전 설치(3.8이상필수)

IDE 설치 : https://www.jetbrains.com/ko-kr/pycharm/download/?section=windows -> 커뮤니티 설치

FastAPI 설치 : pip install fastapi uvicorn uvicorn
-> ASGI(Asynchronus Server Gateway Interface) 는 파이썬에서 비동기 웹서버와 웹 애플케이션 간의 인터페이스 표준 ASGI는 기존 WSGI(Web Server Gateway Interface)의 비동기 버전으로, 파이썬에서 비동기 처리를 지원하는 웹 애플리케이션을 구축하기 위함
-> pycharm-terminal과 cmd가 경로가 서로 다르기 때문에 각자 설치해야 한다
https://velog.io/@hwaya2828/WSGI-ASGI

ASGI 특징

비동기 지원 : ASGI는 비동기 코드 실행을 지원하며 높은 성능과 동시성을 제공, 웹소켓이나 서버 푸시와 같은 비동기 통신이 필요한 애플리케이션에 유용
범용성 : HTTP뿐만 아니라, WebSocket, gRPC와 같은 다른 프로토콜로 지원
유연성 : ASGI 애플리케이션은 다양한 서버 및 프레임워크와 호환되며, 모듈식으로 구성
FastAPI와 ASGI

FastAPI는 ASGI 표준을 따르는 웹 프레임 워크임
FastAPI 애플리케이션은 비동기 처리를 기본으로 하며, Uvicorn과 같은 ASGI 서버를 사용하여 높은 성능을 제공
FastAPI server 실행

main.py 실행
Terminal에서 D:\phthonWorkSpace> uvicorn main:app --reload --port8001(위치 확인)

![image](https://github.com/user-attachments/assets/24039fca-a64a-431f-bdbe-ad113ee02be2)

