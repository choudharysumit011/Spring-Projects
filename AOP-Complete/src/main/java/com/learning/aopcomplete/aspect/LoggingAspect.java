package com.learning.aopcomplete.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class LoggingAspect {

    @Around("execution(* com.learning.aopcomplete.service.UserService.*(..))")
    public Object log(ProceedingJoinPoint pjp ) throws Throwable{
        System.out.println("➡️ Enter: " + pjp.getSignature());

        Object result = pjp.proceed();

        System.out.println("⬅️ Exit: " + pjp.getSignature());

        return result;
    }

}
