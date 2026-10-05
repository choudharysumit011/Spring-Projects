package com.learning.springtransactions.service;

import com.learning.springtransactions.model.Customer;
import com.learning.springtransactions.repo.CustomerRepo;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class PaymentService {

    private final CustomerRepo customerRepo;

    public PaymentService(CustomerRepo customerRepo) {
        this.customerRepo = customerRepo;
    }

    @Transactional
    public void createCustomer(Long id, String name, Long accountNumber, double balance) {
        Customer customer = Customer.builder()
                .id(id)
                .name(name)
                .accountNumber(accountNumber)
                .balance(balance)
                .build();
        customerRepo.save(customer);
    }

    @Transactional
    public int creditPayment(Long customerId, double amount) {
        // Validate input first
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be greater than zero: " + amount);
        }

        if (amount > 10000) {
            throw new IllegalArgumentException("Amount exceeds the maximum limit: " + amount);
        }

        // Load the existing customer, modify and save — do not create a partial entity with the builder
        Customer customer = customerRepo.findById(customerId)
                .orElseThrow(() -> new IllegalArgumentException("Customer ID not found: " + customerId));

        customer.setBalance(customer.getBalance() + amount);
        customerRepo.save(customer);

        System.out.println("Crediting $" + amount + " to customer ID: " + customerId);
        return 1; // Return 1 to indicate success
    }

    @Transactional
    public int debitPayment(Long customerId, double amount) {
        // Validate input first
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be greater than zero: " + amount);
        }

        if (amount > 10000) {
            throw new IllegalArgumentException("Amount exceeds the maximum limit: " + amount);
        }

        Customer customer = customerRepo.findById(customerId)
                .orElseThrow(() -> new IllegalArgumentException("Customer ID not found: " + customerId));

        if (customer.getBalance() < amount) {
            throw new IllegalArgumentException("Insufficient balance for customer ID: " + customerId);
        }

        customer.setBalance(customer.getBalance() - amount);
        customerRepo.save(customer);

        System.out.println("Debiting $" + amount + " from customer ID: " + customerId);
        return 1; // success
    }
}
