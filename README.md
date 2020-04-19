# doctrans-py

> Python port for the go written doctrans

<div align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>
<a href=""><img alt="License: MIT" src="https://img.shields.io/badge/License%3A-MIT-green?style=flat-square">
</a><a href=""><img src="https://img.shields.io/badge/Python%3A-%5E3.6-green?style=flat-square"></a>
</div>

# proto from: https://github.com/googleapis/googleapis/tree/master/google/api

# Install

## Local Spring Boot Installation (linux / windows)

1. download the latest spring boot java application from https://start.spring.io/
    - **Project**: Maven Project
    - **Language**: Language
    - **Spring Boot**: 2.2.2
    - **Project Metadata**
        - *Group*: qds
        - *Artifact*: doctrans
    - **Dependencies**: Eureka Server

2. click on **Generate**
3. unzip the downloaded file and make the following file changes:

*src/main/java/com/example/demo/DemoApplication.java*:

    package com.example.demo;

    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer; // insert this line

    @EnableEurekaServer // insert this line
    @SpringBootApplication
    public class DemoApplication {

            public static void main(String[] args) {
                    SpringApplication.run(DemoApplication.class, args);
            }

    }

*src/main/resources/application.properties:*

    server.port=8761
    eureka.client.register-with-eureka=false
    eureka.client.fetch-registry=false

4. to start the server execute the following command

    - `./mvnw spring-boot:run` (linux)
    - `./mvnw.cmd spring-boot:run` (windows)

## Local doctrans-py setup

1. make sure to use at least **python 3.6** (currently it is not important but I am planning to use f-strings which are only ^3.6 compatible)
2. clone the repo `git clone https://github.com/B4rtware/doctrans-py.git`
3. `cd doctrans-py` and install dependencies via
    - `poetry install` ([Poetry](https://github.com/python-poetry/poetry))
    or
    - use the provided `requirements.txt`


# Usage

# License
MIT
