# Learning Engli

Engli is an English-like interpreted programming language. This guide will help you get started with writing Engli programs.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Running Programs

Run an Engli file:
```bash
engli examples/hello.engli
```

Start the interactive REPL:
```bash
engli repl
```

## Basic Syntax

### Variables

Set variables using the `Set` keyword:

```engli
Set name to "World".
Set age to 20.
Set score to 100.
```

Reassign variables:
```engli
Set age to 21.
```

### Output

Use `Say` to print values:

```engli
Say "Hello, World!".
Say name.
Say age.
```

String interpolation:
```engli
Say "Hello, {name}!".
```

### Arithmetic

Basic arithmetic:

```engli
Set result to 10 plus 5.
Set result to 10 minus 3.
Set result to 10 multiplied by 2.
Set result to 20 divided by 4.
```

Arithmetic assignment:
```engli
Add 10 to score.
Subtract 5 from score.
Multiplied score by 2.
Divided score by 3.
```

### Comparisons

```engli
If age is greater than 18:
    Say "Adult".
Otherwise:
    Say "Minor".
```

Available comparisons:
- `is equal to`
- `is not equal to`
- `is greater than`
- `is less than`
- `is greater than or equal to`
- `is less than or equal to`

### Boolean Logic

```engli
If age is greater than 18 and active:
    Say "Allowed".
```

## Control Flow

### If Statements

```engli
If score is greater than 100:
    Say "You won!".
Otherwise if score is equal to 100:
    Say "Perfect score!".
Otherwise:
    Say "Keep trying.".
```

### While Loops

```engli
Set count to 0.

While count is less than 5:
    Say count.
    Add 1 to count.
```

### For Loops

Iterate over a list:
```engli
For each item in items:
    Say item.
```

Range loop:
```engli
For each number from 1 through 10:
    Say number.
```

### Repeat Loops

```engli
Repeat 5 times:
    Say "Hello".
```

### Break and Continue

```engli
For each number from 1 through 10:
    If number is equal to 5:
        Break out of the loop.
    Say number.
```

## Functions

### Defining Functions

```engli
Define a function called greet that takes name:
    Say "Hello, {name}!".
End the function.
```

### Calling Functions

```engli
Set greeting to greet with "World".
```

### Functions with Return Values

```engli
Define a function called add that takes x and y:
    Return x plus y.
End the function.

Set result to add with 10 and 20.
Say result.
```

### Recursion

```engli
Define a function called factorial that takes n:
    If n is less than or equal to 1:
        Return 1.
    Return n multiplied by factorial with n minus 1.
End the function.

Say factorial with 5.
```

## Data Structures

### Lists

Create a list:
```engli
Set numbers to a list containing 1, 2, 3, 4, and 5.
```

Add to a list:
```engli
Add 6 to numbers.
```

### Maps

```engli
Set person to a map containing:
    "name" mapped to "AB",
    "age" mapped to 20.
```

Access map values:
```engli
Say person at "name".
```

## REPL Commands

The REPL supports special commands starting with `:`:

- `:help` - Show help
- `:clear` - Clear the input buffer
- `:reset` - Reset the environment
- `:load <file>` - Load a file
- `:save <file>` - Save buffer to file
- `:type <var>` - Show variable type
- `:ast` - Show AST of current buffer
- `:exit` or `:quit` - Exit REPL

## Example Programs

### Hello World

```engli
Set name to "World".
Say "Hello, {name}!".
```

### Sum 1 to 100

```engli
Set total to 0.

For each number from 1 through 100:
    Add number to total.

Say total.
```

### Factorial

```engli
Define a function called factorial that takes n:
    If n is less than or equal to 1:
        Return 1.
    Return n multiplied by factorial with n minus 1.
End the function.

Say factorial with 10.
```

## Important Rules

1. **Statements end with a period `.`**
2. **Blocks use `:` and indentation**
3. **Commas `,` continue a statement on the next line**
4. **All keywords are lowercase**
5. **Strings use double quotes `"..."`**

## Next Steps

- Explore the `examples/` directory for more examples
- Read the full documentation in `docs/`
- Try the REPL: `engli repl`
- Run the test suite: `pytest`
