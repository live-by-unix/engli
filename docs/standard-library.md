# Standard Library

Engli includes a comprehensive standard library that provides common functionality.

## Core

### Length

Get the length of a collection:
```engli
Say the length of numbers.
```

## I/O

### Say

Output to console:
```engli
Say "Hello, World!".
```

### Ask

Prompt for input:
```engli
Ask the user for their name and store the answer in name.
```

## Filesystem

### Read File

```engli
Read the file "data.txt" into contents.
```

### Write File

```engli
Write contents to the file "output.txt".
```

### Append to File

```engli
Append "log entry" to the file "log.txt".
```

### File Exists

```engli
If the file "data.txt" exists:

    Say "File exists".
```

### Create Directory

```engli
Create the directory "data".
```

### List Directory

```engli
List the files in the directory "data" and store them in files.
```

### Delete File

```engli
Delete the file "old.txt".
```

## Environment

### Get Environment Variable

```engli
Get the environment variable "HOME" and store it in home.
```

### Set Environment Variable

```engli
Set the environment variable "MODE" to "production".
```

## Process

### Run Command

```engli
Run the command "git"
with arguments "status" and "--short"
and store the result in result.

Say result.output.
Say result.error.
Say result.exit_code.
Say result.succeeded.
```

### Run Shell Command

```engli
Run the shell command "echo hello && pwd"
and store the result in result.
```

## HTTP

### GET Request

```engli
Send a GET request to "https://example.com"
and store the response in response.

Say response.status.
Say response.headers.
Say response.body.
Say response.url.
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

Supports GET, POST, PUT, PATCH, DELETE.

## JSON

### Parse JSON

```engli
Parse response.body as JSON and store it in data.
```

### Stringify to JSON

```engli
Convert data to JSON and store it in json_string.
```

## Time

### Current Date and Time

```engli
Set now to the current date and time.
```

### Unix Timestamp

```engli
Set timestamp to the current Unix timestamp.
```

### Sleep

```engli
Wait for 2 seconds.
```

## Random

### Random Number

```engli
Set number to a random number between 1 and 100.
```

## Concurrency

### Start Task

```engli
Start a task:

    Say "Hello from task".

End the task.
```

### Wait for Task

```engli
Wait for task to finish.
```

### Create Channel

```engli
Create a channel called messages.
```

### Send Through Channel

```engli
Send "Hello" through messages.
```

### Receive from Channel

```engli
Receive a message from messages and store it in message.
```

## Security Considerations

- **Filesystem operations**: Engli can read and write files on your system
- **Process execution**: Engli can run arbitrary commands
- **Environment access**: Engli can access environment variables
- **Network access**: Engli can make HTTP requests
- **No sandbox**: Engli is not sandboxed; treat `.engli` files like any other executable

Always review `.engli` files before running them, especially from untrusted sources.
