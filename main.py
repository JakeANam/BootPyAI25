from http.client import responses
from fastapi import FastAPI # python web 개발 api
from pydantic import BaseModel # 유효성 검사용 pandatic - 입력 type 검사   
from starlette.middleware.base import BasesHTTPMiddleware # - request, response 사이의 특정 작업 수행

# middleware? - 모든 요쳥에 대해 실행되며, 요청을 처리하기 전, 응답을 반환하기 전에 특정 작업을  수행할 수 있다.(logging, 인증, cors처리, 압축 등)

app = FastAPI(  # FastAPI() 객체 생성해서 app 변수에 넣기(원래 Java라면 new 가 있어야 한다) - 생성자를 통해서 postman을 대체하는 문서화 tool이 내장되어 있다
    title = "MBC AI project",
    description = "python과 java boot를 연동한 Ai app",
    version = "1.0.0",
    docs_uri = None, # 보안상 이유로 None 처리
    # redoc_url = None
)

import logging # log 출력용 - log for ~

class LoggingMiddleware(BasesHTTPMiddleware): # log를 console에 출력하는 용도
    logging.basicConfig(level=logging.INFO) # log 출력 추가
    async def dispatch(self, request, call_next):
        logging.info(f"Req: {request.method}{request.url}")
        response = await call_next(request)
        logging.info(f"Status Code : {request.status_code}")
        return response # console에 log 표시
#  로그 표시에 관한 자세한 내용은 : https://wikidocs.net/book/8531
app.add_middleware(LoggingMiddleware) # 모든 요청에 대해 log를 남기는 middleware class를 사용함

class Item(BaseModel): # Item 객체 생성(BaseModel : 객체 연결 -> 상속 개념!) 
    name : str # 상품명 (문자열)
    description : str = None # 상품 설명 (문자열, 없어도 됨)
    price : float # 가격 (실수)
    tax : float = None # 소비세 (실수, 없어도 됨)

@app.get("/") # http://ip주소:port번호/(rootcontext)
async def read_root(): # 비동기 method
    return {"HELLO":"world"}

@app.get("/items/{item_id}") # http://ip주소:port번호/items/1 - get 방식
async def read_item(item_id: int, q: str = None): #
    return {"item_id": item_id, "q": q}
    # item_id: 상품의 번호 <- 경로 매개변수
    # q <- Query 매개변수 (기본값 None)
    # json type으로 return하기 때문에 {}로 묶여있다
    # terminal에서 가동할 때 - uvicorn main:app --reload --port 8001 -> tomcat 실행
    # http://127.0.0.1:8001 -> http://localhost:8001

@app.post("/items/") # http://ip주소:port번호/items/ - post 방식
async def create_item(item: Item): # BaseModel의 역할 - data modeling 을 쉽게 도와주고 유효성 검사도 수행한다 -> 잘못된 data가 들어오면 422code 반환
    return item
    # post방식이면 postman에서 점검해보자