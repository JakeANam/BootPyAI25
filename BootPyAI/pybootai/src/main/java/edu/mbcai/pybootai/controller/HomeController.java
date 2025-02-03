package edu.mbcai.pybootai.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller // controller의 역할? - Routing, 경로 설정
public class HomeController {

   @GetMapping("/")
   public String home(){
       
       return "index"; // resource/templates/index.html
       // http://localhost:80/에 반응하는 controller (숫자 바꾸려면 application.properties에서 바꿔라)
       // -> test 완료
   }
}
