package coding;

public class REQUSTthroughFastApi {
	import org.springframework.stereotype.Service;
	import org.springframework.web.client.RestClient;

	@Service
	public class FastApiService {

	    private final RestClient restClient;

	    public FastApiService(RestClient.Builder builder) {

	        this.restClient = builder
	                .baseUrl("http://localhost:8000")
	                .build();
	    }

	    public ChatResponse sendToFastAPI(String message) {

	        ChatRequest request = new ChatRequest(message);

	        return restClient
	                .post()
	                .uri("/api/chat")
	                .body(request)
	                .retrieve()
	                .body(ChatResponse.class);
	    }
	}
}
