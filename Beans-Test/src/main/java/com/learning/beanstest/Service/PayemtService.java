package com.learning.beanstest.Service;

import com.learning.beanstest.Beans.CardPaymentBean;
import com.learning.beanstest.Beans.MastercardPayment;
import com.learning.beanstest.Beans.PaymentBean;
import com.learning.beanstest.Beans.VisaPayment;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PayemtService {

    private final PaymentBean paymentBean;

    private final CardPaymentBean mastercardPayment;

    @Autowired(required = false)
    public PayemtService(PaymentBean paymentBean, CardPaymentBean mastercardPayment) {
        this.paymentBean = paymentBean;
        this.mastercardPayment = mastercardPayment;
    }
}
