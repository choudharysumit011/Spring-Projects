package com.example.csvReader.demo;

import com.example.csvReader.demo.Service.StudentServiceImpl;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.context.annotation.Bean;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EntityScan("com.example.csvReader.demo.Model")
@EnableJpaRepositories("com.example.csvReader.demo.repository")
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@Bean
	CommandLineRunner loadCsv(StudentServiceImpl csvService) {
		return args -> {
			System.out.println("Starting CSV load...");
			csvService.loadStudentsFromCsv();
			System.out.println("CSV load completed.");
		};
	}

}
