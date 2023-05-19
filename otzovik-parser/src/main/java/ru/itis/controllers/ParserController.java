package ru.itis.controllers;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import ru.itis.service.parser.OtzovikParser;

@RequiredArgsConstructor
@Controller
@RequestMapping("/parse")
public class ParserController {

    private final OtzovikParser otzovikParser;

    @GetMapping("/{company-name}")
    public ResponseEntity getAddBookPage(@PathVariable("company-name") String companyName){
        otzovikParser.parse(companyName);
        return ResponseEntity.ok().build();
    }
}
