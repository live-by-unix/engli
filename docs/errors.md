# Error Handling in Engli

Engli provides comprehensive error handling with try-catch blocks and detailed error messages.

## Try-Catch

### Basic Syntax

```engli
Try:

    Statements that might fail.

If an error occurs as error:

    Handle the error.
```

### Example: Division by Zero

```engli
Try:

    Set x to 10 divided by 0.

If an error occurs as error:

    Say "Error: {error.message}".
```

### Example: File Operations

```engli
Try:

    Read the file "nonexistent.txt" into contents.

If an error occurs as error:

    Say "Cannot read file: {error.message}".
```

## Throwing Errors

### Throw Statement

```engli
Throw an error saying "Invalid input".
```

### Example: Validation

```engli
Define a function called divide that takes a and b:

    If b is equal to 0:

        Throw an error saying "Division by zero".

    Return a divided by b.

End the function.

Try:

    Set result to divide with 10 and 0.

If an error occurs as error:

    Say error.message.
```

## Error Types

Engli errors include:
- **Message**: Human-readable error description
- **Type**: Error category (e.g., "RuntimeError", "DivisionByZero")
- **Source location**: File, line, and column where error occurred
- **Stack trace**: Call stack information where available

## Error Messages

Engli provides detailed, source-aware error messages:

```
error: Division by zero

 --> main.engli:5:15
  |
5 | Set x to 10 divided by 0.
  |               ^

Cannot divide by zero.
```

## Common Errors

### Undefined Variable

```
error: Undefined variable: x

 --> main.engli:3:5
  |
3 | Say x.
  |     ^

Variable 'x' is not defined. Define it before use.
```

### Type Mismatch

```
error: Cannot add these types

 --> main.engli:4:10
  |
4 | Set x to 10 plus "hello".
  |          ^

Cannot add number and text.
```

### Index Out of Bounds

```
error: Index out of bounds

 --> main.engli:5:15
  |
5 | Say numbers at index 10.
  |               ^

Index 10 is out of bounds for list of length 3.
```

## Runtime vs Compile-Time Errors

### Compile-Time Errors

Detected during parsing/semantic analysis:
- Syntax errors
- Undefined variables
- Invalid types (where detectable)
- Break/continue outside loops

### Runtime Errors

Detected during execution:
- Division by zero
- File not found
- Network errors
- Type mismatches in dynamic operations
- Thrown errors

## Error Handling Best Practices

1. **Anticipate errors**: Use try-catch for operations that might fail
2. **Provide context**: Include helpful error messages when throwing
3. **Log errors**: Use error messages for debugging
4. **Fail gracefully**: Provide fallback behavior when possible
5. **Validate input**: Check inputs before operations

## Error Recovery

### Retry Logic

```engli
Define a function called fetch_data that takes url:

    Set max_retries to 3.
    Set attempts to 0.

    While attempts is less than max_retries:

        Try:

            Send a GET request to url
            and store the response in response.

            If response.succeeded:

                Return response.

        If an error occurs as error:

            Add 1 to attempts.

            If attempts is equal to max_retries:

                Throw an error saying "Failed after {max_retries} attempts".

    Return nothing.

End the function.
```

### Default Values

```engli
Try:

    Read the file "config.txt" into config.

If an error occurs as error:

    Set config to "default config".
```

## Debugging

### Stack Traces

Errors include stack traces for debugging:
```
RuntimeError: Division by zero
  at main.engli:5:15

Stack trace:
  at divide (math.engli:10:5)
  at main (main.engli:5:10)
```

### Diagnostic Mode

Use the `check` command to analyze without executing:
```bash
engli check main.engli
```

This reports syntax and semantic errors without running the program.
