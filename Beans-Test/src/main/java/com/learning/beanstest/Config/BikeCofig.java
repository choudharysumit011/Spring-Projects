package com.learning.beanstest.Config;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import lombok.Data;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Data
public class BikeCofig {

    String bikeName = "BMW";

    @Bean
    public String bikeConfigMethod(){
        System.out.println("Bike Config Method");
        return bikeName;
    }
    @Bean
    @Lazy
    public String displayBikeName() {
        System.out.println("Bike Name: " + bikeName);
        return bikeName;
    }

    @PostConstruct
    public void init(){
        System.out.println("Bike Config Initialized");
    }

    @PreDestroy
    public void destroy(){
        System.out.println("Bike Config Destroyed");
    }


}
