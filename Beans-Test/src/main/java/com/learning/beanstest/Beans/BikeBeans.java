package com.learning.beanstest.Beans;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;

@Configuration
public class BikeBeans {

    @Bean
    public String bikeName() {
        System.out.println("Bike Name: Yamaha R15");
        return "Yamaha R15";
    }




}
