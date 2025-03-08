package com.ecommerce.service;

import com.ecommerce.config.EnvConfig; 
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.security.Key;
import java.util.Base64;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

@Service
public class JwtService {

    private String secret;
    private long expiration;
    private Key signingKey;

    @PostConstruct
    public void init() {
        // Cargar propiedades desde .env
        this.secret = EnvConfig.get("JWT_SECRET");
        this.expiration = Long.parseLong(EnvConfig.get("JWT_EXPIRATION"));

        // Configurar la clave de firma
        if (secret == null || secret.isEmpty()) {
            // Generar una clave secreta automáticamente si no se proporciona una
            signingKey = Keys.secretKeyFor(SignatureAlgorithm.HS256);
            secret = Base64.getEncoder().encodeToString(signingKey.getEncoded());
        } else {
            // Usar la clave secreta proporcionada en .env
            signingKey = Keys.hmacShaKeyFor(Base64.getDecoder().decode(secret));
        }
    }

    /**
     * Extrae el nombre de usuario (subject) del token JWT.
     *
     * @param token Token JWT.
     * @return Nombre de usuario.
     */
    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    /**
     * Extrae un claim específico del token JWT.
     *
     * @param token          Token JWT.
     * @param claimsResolver Función para resolver el claim.
     * @return Valor del claim.
     */
    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    /**
     * Extrae todos los claims del token JWT.
     *
     * @param token Token JWT.
     * @return Objeto Claims con todos los claims.
     */
    private Claims extractAllClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(signingKey)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    /**
     * Genera un token JWT para un usuario.
     *
     * @param username Nombre de usuario.
     * @return Token JWT.
     */
    public String generateToken(String username) {
        Map<String, Object> claims = new HashMap<>();
        return createToken(claims, username);
    }

    /**
     * Crea un token JWT con los claims y el subject proporcionados.
     *
     * @param claims  Claims adicionales.
     * @param subject Subject (nombre de usuario).
     * @return Token JWT.
     */
    private String createToken(Map<String, Object> claims, String subject) {
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(subject)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + expiration))
                .signWith(signingKey, SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * Valida un token JWT.
     *
     * @param token       Token JWT.
     * @param userDetails Detalles del usuario.
     * @return true si el token es válido, false en caso contrario.
     */
    public boolean validateToken(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }

    /**
     * Verifica si un token JWT ha expirado.
     *
     * @param token Token JWT.
     * @return true si el token ha expirado, false en caso contrario.
     */
    private boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    /**
     * Extrae la fecha de expiración del token JWT.
     *
     * @param token Token JWT.
     * @return Fecha de expiración.
     */
    private Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }
}