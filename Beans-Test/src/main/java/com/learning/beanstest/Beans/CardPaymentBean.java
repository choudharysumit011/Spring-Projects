package com.learning.beanstest.Beans;

import org.springframework.stereotype.Component;

@Component
public interface CardPaymentBean extends PaymentBean{

    @Override
    void processPayment(double amount);

}
