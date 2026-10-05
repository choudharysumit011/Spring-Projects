package com.learning.aopcomplete.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class AuditAspect {

    @Around(
            "execution(* com.learning.aopcomplete.service..*(..)) || " +
                    "execution(* com.learning.aopcomplete.repo..*(..))"
    )
    public Object audit(ProceedingJoinPoint pjp) throws Throwable {

        String className =
                pjp.getTarget().getClass().getSimpleName();
        String methodName =
                pjp.getSignature().getName();

        long start = System.currentTimeMillis();

        try {
            Object result = pjp.proceed();

            long time = System.currentTimeMillis() - start;

            System.out.println(
                    "✅ SUCCESS | " +
                            className + "." + methodName +
                            " | time=" + time + "ms"
            );

            return result;

        } catch (Throwable ex) {

            long time = System.currentTimeMillis() - start;

            System.out.println(
                    "❌ ERROR | " +
                            className + "." + methodName +
                            " | time=" + time + "ms" +
                            " | ex=" + ex.getClass().getSimpleName() +
                            " | msg=" + ex.getMessage()
            );

            throw ex; // VERY IMPORTANT
        }
    }
}

