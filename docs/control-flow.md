# Control Flow in Engli

Engli provides several control flow constructs for managing program execution.

## Conditionals

### If Statement

```engli
If condition:

    Statements.

Otherwise:

    Statements.
```

### If-Else-If

```engli
If condition:

    Statements.

Otherwise if another condition:

    Statements.

Otherwise:

    Statements.
```

Example:
```engli
Set age to 18.

If age is greater than or equal to 18:

    Say "You are an adult.".

Otherwise:

    Say "You are a minor.".
```

## Loops

### While Loop

```engli
While condition:

    Statements.

End the loop.
```

Example:
```engli
Set count to 0.

While count is less than 5:

    Say count.
    Add 1 to count.

End the loop.
```

### For Each Loop

```engli
For each item in items:

    Statements.

End the loop.
```

Example:
```engli
Set numbers to a list containing 1, 2, 3, 4, and 5.

For each number in numbers:

    Say number.

End the loop.
```

### For Range Loop

```engli
For each number from 1 through 10:

    Statements.

End the loop.
```

Example:
```engli
For each i from 1 through 10:

    Say i.

End the loop.
```

### Repeat Loop

```engli
Repeat 10 times:

    Statements.

End the repetition.
```

Example:
```engli
Repeat 3 times:

    Say "Hello!".

End the repetition.
```

### Forever Loop

```engli
Forever:

    Statements.

End the loop.
```

Example:
```engli
Set count to 0.

Forever:

    Say count.
    Add 1 to count.

    If count is greater than 10:

        Break out of the loop.

End the loop.
```

## Break and Continue

### Break

Exit a loop early:
```engli
Break out of the loop.
```

### Continue

Skip to the next iteration:
```engli
Continue with the next iteration.
```

Example:
```engli
For each number from 1 through 10:

    If number is equal to 5:

        Continue with the next iteration.

    Say number.

End the loop.
```

## Pattern Matching

```engli
Match value:
    When value is 1:
        Say "One".
    When value is 2:
        Say "Two".
    Otherwise:
        Say "Other".
End the match.
```

Example with enums:
```engli
Define an enumeration called Direction containing:
    North,
    South,
    East,
    West.
End the enumeration.

Set direction to Direction.North.

Match direction:
    When direction is Direction.North:
        Say "Going North".
    When direction is Direction.South:
        Say "Going South".
    Otherwise:
        Say "Other direction".
End the match.
```

## Error Handling

### Try-Catch

```engli
Try:

    Statements that might fail.

If an error occurs as error:

    Handle the error.
```

Example:
```engli
Try:

    Set x to 10 divided by 0.

If an error occurs as error:

    Say error.message.
```

### Throwing Errors

```engli
Throw an error saying "Invalid input".
```

## Control Flow Best Practices

1. **Use appropriate loop types**: Choose the loop that best fits your use case
2. **Avoid infinite loops**: Always include a termination condition in while/forever loops
3. **Handle errors gracefully**: Use try-catch for operations that might fail
4. **Use pattern matching**: For complex conditional logic, pattern matching can be clearer than nested if statements
