package ru.itis.db.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.itis.db.entity.Review;

public interface ReviewRepository extends JpaRepository<Review, Long> {
}
