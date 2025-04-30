package edu.mbcai.pybootai.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {
    
    // WebClient를 구성하고 정의하여 application에서 사용할 수 있도록
    // https://m.blog.naver.com/seek316/223337685249

    @Bean
    WebClient webclient(){
        return WebClient.builder().exchangeStrategies(ExchangeStrategies.builder()
                .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(-1))
                .build())
        .baseUrl("http://localhost:8001").build();


    }
}
