package com.ecommerce.runner;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.ecommerce.model.Usuario;
import com.ecommerce.service.IUsuarioService;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Component
public class InicializadorDatosRunner implements CommandLineRunner {
	
	private final IUsuarioService usuarioService;
	private final BCryptPasswordEncoder passwordEncoder;
	
	public InicializadorDatosRunner(IUsuarioService usuarioService, BCryptPasswordEncoder passwordEncoder) {
		this.usuarioService = usuarioService;
		this.passwordEncoder = passwordEncoder;
	}
	
	@Override
	public void run(String...args)throws Exception{
		
		//Crear un usuario admin por defecto si no existe
		if(usuarioService.findByEmail("admin@ecommerce.com").isEmpty()) {
			Usuario admin = new Usuario();
			admin.setEmail("admin@ecommerce.com");
			admin.setPassword(passwordEncoder.encode("admin123"));
			admin.setTipo("ADMIN");
			usuarioService.save(admin);
			System.out.println("Usuario admin creado con exito");
		}
		
	}
}
