package com.learning.aopcomplete.rest;

import com.learning.aopcomplete.model.User;
import com.learning.aopcomplete.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/users")
public class Controller {

    private final UserService service;

    public Controller(UserService service) {
        this.service = service;
    }

    @PostMapping("/create")
    public User create(@RequestParam String name) {
       return service.create(name);
    }
    @GetMapping("/getAll")
    public List<User> findAll() {
        return service.findAll();}

}
