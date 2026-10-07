# HTTP/REST in Engli

Engli provides built-in HTTP client functionality for making web requests.

## HTTP Requests

### GET Request

```engli
Send a GET request to "https://example.com"
and store the response in response.
```

### POST Request with JSON

```engli
Send a POST request to "https://api.example.com/users"
with JSON containing:
    "name" mapped to "AB",
    "age" mapped to 20
and store the response in response.
```

### Other HTTP Methods

Engli supports all common HTTP methods:
- GET
- POST
- PUT
- PATCH
- DELETE

Example:
```engli
Send a PUT request to "https://api.example.com/users/1"
with JSON containing:
    "name" mapped to "Updated"
and store the response in response.

Send a DELETE request to "https://api.example.com/users/1"
and store the response in response.
```

## Response Object

The response object contains:
- `response.status` - HTTP status code (e.g., 200, 404)
- `response.headers` - Response headers as text
- `response.body` - Response body as text
- `response.url` - Final URL (after redirects)

### Example: Check Response Status

```engli
Send a GET request to "https://example.com"
and store the response in response.

Say response.status.

If response.status is equal to 200:

    Say "Request succeeded".

Otherwise:

    Say "Request failed".
```

## Headers

### Custom Headers

```engli
Send a GET request to "https://api.example.com"
with headers containing:
    "Authorization" mapped to "Bearer token123",
    "Content-Type" mapped to "application/json"
and store the response in response.
```

## Request Body

### JSON Body

```engli
Send a POST request to "https://api.example.com/users"
with JSON containing:
    "name" mapped to "AB",
    "age" mapped to 20
and store the response in response.
```

### Text Body

```engli
Send a POST request to "https://api.example.com/data"
with "raw text data"
and store the response in response.
```

## JSON Handling

### Parse JSON Response

```engli
Send a GET request to "https://api.example.com/users"
and store the response in response.

Parse response.body as JSON and store it in data.

Say data at "name".
```

### Send JSON Data

```engli
Set user_data to a map containing:
    "name" mapped to "AB",
    "age" mapped to 20.

Convert user_data to JSON and store it in json_string.

Send a POST request to "https://api.example.com/users"
with json_string
and store the response in response.
```

## Complete Example

```engli
# Make an API request
Send a GET request to "https://httpbin.org/get"
and store the response in response.

Say "Status: {response.status}".
Say "Body: {response.body}".

# Parse JSON response
Parse response.body as JSON and store it in data.

Say "Parsed data: {data}".

# POST JSON data
Send a POST request to "https://httpbin.org/post"
with JSON containing:
    "name" mapped to "Engli",
    "version" mapped to "0.1.0"
and store the response in response.

Say response.status.
```

## Error Handling

### Network Errors

```engli
Try:

    Send a GET request to "https://invalid-url"
    and store the response in response.

If an error occurs as error:

    Say "Request failed: {error.message}".
```

### HTTP Errors

```engli
Send a GET request to "https://example.com/nonexistent"
and store the response in response.

If response.status is greater than or equal to 400:

    Say "HTTP error: {response.status}".
```

## Best Practices

1. **Check status codes**: Always verify the response status
2. **Handle errors**: Use try-catch for network operations
3. **Use timeouts**: Long-running requests can hang (future feature)
4. **Validate responses**: Check that response data is as expected
5. **Secure credentials**: Don't hardcode API keys in source files

## Dependencies

Engli uses the `httpx` library for HTTP requests. Ensure it's installed:
```bash
pip install httpx
```
