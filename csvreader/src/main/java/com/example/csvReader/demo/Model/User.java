package com.example.csvReader.demo.Model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "students")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class User {
    @Id
    private Integer rollNo;
    private String name;
    private Integer physics;
    private Integer maths;
    private Integer chemistry;
    private Integer english;
    private Integer sports;
}
