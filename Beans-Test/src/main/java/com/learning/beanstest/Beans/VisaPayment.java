package com.learning.beanstest.Beans;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(prefix = "visa", value = "payment", havingValue = "true", matchIfMissing = false)
public class VisaPayment implements CardPaymentBean {

    public VisaPayment(){
        System.out.println("Card paymentTypeVisa");

    }

    @Override
    public void processPayment(double amount) {
        System.out.println("Processing Visa payment of amount: " + amount);
    }
}
