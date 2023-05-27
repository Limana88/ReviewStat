package ru.itis.db.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.itis.db.entity.User;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByNameAndCountry(String name, String country);
}
