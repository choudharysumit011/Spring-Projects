package com.example.csvReader.demo.Service;

import com.example.csvReader.demo.Model.User;
import com.example.csvReader.demo.repository.UserRepository;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.InputStreamReader;

@Service
public class StudentServiceImpl {

    private final UserRepository userRepository;

    StudentServiceImpl(UserRepository userRepository){
        this.userRepository = userRepository;
    }

    public void loadStudentsFromCsv(){

        try {
            ClassPathResource classPathResource = new ClassPathResource("students.csv");
            BufferedReader reader = new BufferedReader(new InputStreamReader(classPathResource.getInputStream()));

            String line;
            Boolean isHeader = true;

            while ((line = reader.readLine()) != null){

                if (isHeader){
                    isHeader = false;
                    continue;
                }
                System.out.println("Inside data load");

                String[] data = line.split(",");
                User user = User.builder().
                rollNo(Integer.parseInt(data[0]))
                        .name(data[1])
                        .physics(Integer.parseInt(data[2]))
                        .maths(Integer.parseInt(data[3]))
                        .chemistry(Integer.parseInt(data[4]))
                        .english(Integer.parseInt(data[5]))
                        .sports(Integer.parseInt(data[6]))
                        .build();
                userRepository.save(user);
                System.out.println("Load compleete");
            }
            reader.close();

        }
        catch (Exception e){
            throw new RuntimeException("Field to load CSV", e);
        }
    }

}
