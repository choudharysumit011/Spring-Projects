package com.learning.beanstest.Beans;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@Scope("prototype")
public class PrototypeBeans {


    public PrototypeBeans() {
        System.out.println("Prototype Bean instance created: " + this);
    }

}
