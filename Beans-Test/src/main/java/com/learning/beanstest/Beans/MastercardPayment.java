package com.learning.beanstest.Beans;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(prefix = "mastercard", name = "payment", havingValue = "true")
public class MastercardPayment implements CardPaymentBean {

    public MastercardPayment(){
        System.out.println("This is mastercard class");
    }


    @Override
    public void processPayment(double amount) {
        System.out.println("Processing Mastercard payment of amount: " + amount);
    }
}
