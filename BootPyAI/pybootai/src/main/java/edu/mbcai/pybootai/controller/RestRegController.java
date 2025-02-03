package edu.mbcai.pybootai.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@RestController // python과 통신하는 비동기화 controller 역할
public class RestRegController {

    @Autowired // 생성자  자동 주입(객체 사용할 수 있도록)
    private WebClient webClient; // 방금 생성한 config controller 객체 생성

    @PostMapping("/java_service")
    public String serviceRequest(MultipartFile file, String message){

        MultipartBodyBuilder bodyBuilder = new MultipartBodyBuilder(); // multipart Form data 구성
        bodyBuilder.part("message", message); // Form data
        bodyBuilder.part("file", file.getResource()); // Form data file
        String result = webClient.post().uri("/detect") // post방식으로 요청, end point는 /detect
            .contentType(MediaType.MULTIPART_FORM_DATA) // file 전송 개시
            .body(BodyInserters.fromMultipartData(bodyBuilder.build())) //폼 데이터를 요청 본문으로 설정
            .retrieve() // 요청을 실행하고
            .bodyToMono(String.class) // 본문을 String type으로 변환
            .block(); // 비동기를 동기적으로 block해서 결과 반환

        return result;
    } // http://localhost:80/java_service 요청 post 처리

    // 1. java rest controller로 text와 image를 비동기 방식으로 전송
    // 2. AI server에서 image를 받아 객체 탐지 수행
    // 3. AI server에서 image를 base64 encording 문자열로 변환
    // 4. rest controller에서 비동기 방식으로 text와 image변환
    // 5. 비동기 요청한 view page에서 결과 화면 출력
}
