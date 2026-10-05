package com.learning.beanstest.Service;

import com.learning.beanstest.Beans.BikeBeans;
import com.learning.beanstest.Beans.PrototypeBeans;
import com.learning.beanstest.Config.BikeCofig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class BikeService {

    @Autowired
    PrototypeBeans prototypeBeans;
    @Autowired
    BikeBeans beans;

    @Autowired
    BikeCofig bikeCofig;



    public void bikeDetails() {

    }



}
