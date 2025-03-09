package com.ecommerce;

import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringEcommerceApplication {

    public static void main(String[] args) {
        // Cargar variables de entorno desde el archivo .env
        Dotenv dotenv = Dotenv.configure().load();
        
        // Establecer las variables de entorno en el sistema
        dotenv.entries().forEach(entry -> System.setProperty(entry.getKey(), entry.getValue()));

        // Iniciar la aplicación Spring Boot
        SpringApplication.run(SpringEcommerceApplication.class, args);
    }
}