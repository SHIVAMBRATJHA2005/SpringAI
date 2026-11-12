package com.itbulls.springdemo2.oauthdemo;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class OAuthDemoController {

    @Value("${auth0.client-id}")
    private String clientId;

    @Value("${auth0.client-secret}")
    private String clientSecret;

    @Value("${auth0.audience}")
    private String audience;

    @Value("${auth0.token-url}")
    private String tokenUrl;
    
    @Value("${auth0.grant-type}")
    private String grantType;

    private final RestTemplate restTemplate;
    
    public OAuthDemoController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @GetMapping("/demo-machine-to-machine")
    public ResponseEntity<String> demo() {
        // 1. Prepare the token request
        HttpHeaders tokenHeaders = new HttpHeaders();
        tokenHeaders.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        MultiValueMap<String, String> tokenBody = new LinkedMultiValueMap<>();
        tokenBody.add("grant_type", grantType);
        tokenBody.add("client_id", clientId);
        tokenBody.add("client_secret", clientSecret);
        tokenBody.add("audience", audience);

        HttpEntity<MultiValueMap<String, String>> tokenRequest = new HttpEntity<>(tokenBody, tokenHeaders);

        // 2. Get access token
        ResponseEntity<TokenResponse> tokenResponse = restTemplate
        		.postForEntity(tokenUrl, tokenRequest, TokenResponse.class);
        if (!tokenResponse.getStatusCode().is2xxSuccessful()) {
            return ResponseEntity.status(tokenResponse.getStatusCode()).body("Auth0 error");
        }
        TokenResponse tokenResponseBody = tokenResponse.getBody();
        if (tokenResponseBody == null || tokenResponseBody.getAccess_token() == null) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                 .body("Token response is null or invalid");
        }

        String accessToken = tokenResponseBody.getAccess_token();
        
        System.out.println("========== " + accessToken);

        // 3. Use token to call protected endpoint
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(accessToken);
        HttpEntity<Void> entity = new HttpEntity<>(headers);

        ResponseEntity<String> apiResponse = restTemplate.exchange(
                "http://localhost:8080/payments",
                HttpMethod.GET,
                entity,
                String.class
        );

        // 4. Return API response to client
        String output = "Status Code: " + apiResponse.getStatusCode() + "\n\n" +
                        "Response Body:\n" + apiResponse.getBody();
        return ResponseEntity.status(apiResponse.getStatusCode()).body(output);
    }

    // Internal class to map token response JSON
    static class TokenResponse {
        private String access_token;
        public String getAccess_token() { return access_token; }
        public void setAccess_token(String access_token) { this.access_token = access_token; }
    }
}