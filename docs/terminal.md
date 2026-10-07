# Terminal and Shell Commands

Engli provides powerful capabilities for interacting with the terminal and executing system commands.

## Running Commands

### Basic Command Execution

Execute a command with arguments:
```engli
Run the command "git"
with arguments "status" and "--short"
and store the result in result.
```

The result object contains:
- `result.output` - Standard output
- `result.error` - Standard error
- `result.exit_code` - Exit code (0 for success)
- `result.succeeded` - Boolean indicating success

### Example: Git Status

```engli
Run the command "git"
with arguments "status" and "--short"
and store the result in result.

Say result.output.

If result.succeeded:

    Say "Command succeeded".

Otherwise:

    Say "Command failed".
```

## Shell Commands

### Shell Execution

Execute commands through the shell:
```engli
Run the shell command "echo hello && pwd"
and store the result in result.
```

### Example: Complex Shell Command

```engli
Run the shell command "ls -la | grep .engli"
and store the result in result.

Say result.output.
```

## Security Implications

### Important Security Notes

1. **Command injection**: Be careful when using user input in commands
2. **Shell execution**: Shell commands have full system access
3. **No sandbox**: Engli is not sandboxed; commands run with your permissions
4. **Trust source**: Only run `.engli` files from trusted sources

### Safe Practices

1. **Validate input**: Sanitize any user input before using in commands
2. **Use explicit commands**: Prefer `Run the command` over shell commands when possible
3. **Check exit codes**: Always verify command success
4. **Limit privileges**: Run with minimum required permissions

## Common Use Cases

### File Operations

```engli
Run the command "ls"
with arguments "-la"
and store the result in result.

Say result.output.
```

### System Information

```engli
Run the command "uname"
with arguments "-a"
and store the result in result.

Say result.output.
```

### Process Management

```engli
Run the command "ps"
with arguments "aux"
and store the result in result.

Say result.output.
```

## Error Handling

Always handle potential command failures:
```engli
Try:

    Run the command "nonexistent"
    and store the result in result.

If an error occurs as error:

    Say "Command failed: {error.message}".
```

## Cross-Platform Considerations

Commands are platform-specific:
- Use appropriate commands for your OS (Linux/macOS vs Windows)
- Consider using Engli's filesystem APIs instead of shell commands for portability
- Test on target platforms before deployment
