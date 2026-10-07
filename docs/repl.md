# REPL (Read-Eval-Print Loop)

The Engli REPL provides an interactive environment for writing and executing Engli code.

## Starting the REPL

```bash
engli repl
```

You'll see:
```
Engli REPL 0.1.0
Type :help for help, :exit to quit

>
```

## Basic Usage

### Simple Expressions

```
> Set x to 10.
> Say x.
10
>
```

### Multiline Blocks

The REPL supports multiline input for blocks:

```
> Define a function called square that takes x:
...     Return x multiplied by x.
... End the function.
>
> Say square with 5.
25
>
```

## REPL Commands

### :help

Show available commands:
```
> :help
Available commands:
  :help     - Show this help
  :clear    - Clear the input buffer
  :reset    - Reset the environment
  :load     - Load a file into the REPL
  :save     - Save the current buffer to a file
  :type     - Show the type of a variable
  :ast      - Show the AST of the current buffer
  :exit     - Exit the REPL
  :quit     - Exit the REPL
```

### :clear

Clear the current input buffer:
```
> :clear
Buffer cleared
```

### :reset

Reset the environment (clear all variables):
```
> :reset
Environment reset
```

### :load

Load and execute a file:
```
> :load examples/hello.engli
Loaded: examples/hello.engli
```

### :save

Save the current buffer to a file:
```
> Set x to 10.
> :save my_code.engli
Saved to: my_code.engli
```

### :type

Show the type of a variable:
```
> Set x to 10.
> :type x
x: number
```

### :ast

Show the AST (Abstract Syntax Tree) of the current buffer:
```
> Set x to 10.
> :ast
Program(statements=[VariableDeclaration(...)])
```

### :exit / :quit

Exit the REPL:
```
> :exit
Goodbye!
```

## Features

### Persistent State

Variables and functions persist between commands:
```
> Set x to 10.
> Add 5 to x.
> Say x.
15
>
```

### History

The REPL maintains command history (with prompt_toolkit):
- Use arrow keys to navigate history
- History is saved to `.engli_history`

### Auto-suggestion

With prompt_toolkit, the REPL suggests commands from history.

## Example Session

```
Engli REPL 0.1.0
Type :help for help, :exit to quit

> Set name to "World".
> Say "Hello, {name}!".
Hello, World!
> Define a function called add that takes a and b:
...     Return a plus b.
... End the function.
>
> Set result to add with 10 and 20.
> Say result.
30
> :type result
result: number
> :exit
Goodbye!
```

## Tips

1. **Use multiline for functions**: Define functions across multiple lines for clarity
2. **Check types**: Use `:type` to verify variable types
3. **Save work**: Use `:save` to save useful code snippets
4. **Load examples**: Use `:load` to try example programs
5. **Reset when needed**: Use `:reset` to clear a messy environment

## Limitations

- The REPL uses the same interpreter as file execution
- Some file-specific features (like imports) may behave differently
- State is lost when you exit the REPL

## Installation Note

The REPL requires `prompt_toolkit` for the best experience:
```bash
pip install prompt_toolkit
```

Without it, a basic REPL is still available with reduced features.
