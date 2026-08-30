package com.tom.main2;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin("*")
public class OllamaController {

    private final ChatClient chatClient;

    public OllamaController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @GetMapping("/{message}")
    public ResponseEntity<String> getAnswers(@PathVariable String message) {

        String response = chatClient
                .prompt()
                .user(message)
                .call()
                .content();

        return ResponseEntity.ok(response);
    }
}