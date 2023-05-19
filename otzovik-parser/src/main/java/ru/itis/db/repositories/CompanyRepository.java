package ru.itis.db.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.itis.db.entity.Company;

public interface CompanyRepository extends JpaRepository<Company, Long> {

    Company getCompanyByName(String name);
}
