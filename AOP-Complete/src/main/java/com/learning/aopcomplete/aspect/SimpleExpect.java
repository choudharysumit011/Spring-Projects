package com.learning.aopcomplete.aspect;

import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.stereotype.Component;

@Component
@Aspect
public class SimpleExpect {

    @Before("execution(* com.learning.aopcomplete.rest.Controller.findAll(..))")
    public void expectCreate() {
        System.out.println("Expecting find method to be called");
    }

    @Before("within(*com.learning.aopcomplete.service..*)")
    public void expectService() {
        System.out.println("Expecting service method to be called");
    }

    @Before("@within(org.springframework.stereotype.Controller)")
    public void expectRepo() {
        System.out.println("Controller  method to be called");

    }
}
