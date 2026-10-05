package com.learning.aopcomplete.service;

import com.learning.aopcomplete.model.User;
import com.learning.aopcomplete.repo.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class UserService {

    private final UserRepository repo;

    public UserService(UserRepository repo) {
        this.repo = repo;
    }

    @Transactional
    public User create(String name) {
        User user = new User();
        user.setName(name);
        user.setId(null);
        return repo.save(user);
    }

    public List<User> findAll() {
        return repo.findAll();
    }
}

