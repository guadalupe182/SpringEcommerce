package com.ecommerce.service;

import com.ecommerce.model.Usuario;
import com.ecommerce.repository.IUsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private IUsuarioRepository usuarioRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // Busca el usuario en la base de datos
        Usuario usuario = usuarioRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException("Usuario no encontrado: " + username));

        // Retorna un UserDetails con los datos del usuario
        return User.builder()
                .username(usuario.getEmail())
                .password(usuario.getPassword())
                .roles(usuario.getTipo()) // Asegúrate de que el usuario tenga un rol
                .build();
    }
}