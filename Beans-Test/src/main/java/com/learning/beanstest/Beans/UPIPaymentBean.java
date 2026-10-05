package com.learning.beanstest.Beans;

import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Component
@Primary
public class UPIPaymentBean implements PaymentBean {


    @Override
    public void processPayment(double amount) {
        System.out.println("Processing UPI payment of amount: " + amount);
    }
}
