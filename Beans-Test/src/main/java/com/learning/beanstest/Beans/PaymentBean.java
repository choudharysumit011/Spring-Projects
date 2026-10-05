package com.learning.beanstest.Beans;

import org.springframework.stereotype.Component;

@Component
public interface PaymentBean {

    void processPayment(double amount);
}
