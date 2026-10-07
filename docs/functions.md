# Functions in Engli

Functions are first-class citizens in Engli. They can be defined, called, passed as arguments, and returned from other functions.

## Function Definition

```engli
Define a function called add that takes a and b:

    Return a plus b.

End the function.
```

## Function Call

```engli
Set result to add with 10 and 20.
```

## Parameters

Functions can take multiple parameters:
```engli
Define a function called greet that takes name and age:

    Say "Hello, {name}, you are {age} years old.".

End the function.

greet with "AB" and 25.
```

## Return Values

Functions can return values:
```engli
Define a function called square that takes x:

    Return x multiplied by x.

End the function.

Set result to square with 5.
```

Functions without explicit return return `nothing`:
```engli
Define a function called say_hello:

    Say "Hello!".

End the function.
```

## Recursion

Engli supports recursive functions:
```engli
Define a function called factorial that takes n:

    If n is less than or equal to 1:

        Return 1.

    Return n multiplied by factorial with n minus 1.

End the function.

Say factorial with 5.
```

Fibonacci example:
```engli
Define a function called fibonacci that takes n:

    If n is less than or equal to 0:

        Return 0.

    If n is equal to 1:

        Return 1.

    Return fibonacci with n minus 1 plus fibonacci with n minus 2.

End the function.

Say fibonacci with 10.
```

## First-Class Functions

Functions can be assigned to variables:
```engli
Define a function called add that takes a and b:

    Return a plus b.

End the function.

Set operation to add.
Set result to operation with 10 and 20.
```

## Closures

Functions support lexical closures:
```engli
Define a function called make_counter:

    Set count to 0.

    Define a function called increment:

        Add 1 to count.
        Return count.

    End the function.

    Return increment.

End the function.

Set counter to make_counter.
Say counter with.
Say counter with.
Say counter with.
```

## Higher-Order Functions

Functions can take other functions as arguments:
```engli
Define a function called apply that takes func and value:

    Return func with value.

End the function.

Define a function called double that takes x:

    Return x multiplied by 2.

End the function.

Set result to apply with double and 5.
```

## Local Variables

Functions can have local variables:
```engli
Define a function called calculate that takes x:

    Set temp to x multiplied by 2.
    Set result to temp plus 10.
    Return result.

End the function.
```

## Nested Functions

Functions can be defined inside other functions:
```engli
Define a function called outer:

    Define a function called inner:

        Say "Inner function".

    End the function.

    inner.

End the function.
```

## Function Best Practices

1. **Use descriptive names**: Function names should clearly describe what they do
2. **Keep functions focused**: Each function should do one thing well
3. **Use parameters**: Avoid hardcoded values, use parameters instead
4. **Document purpose**: While Engli doesn't have inline documentation, choose clear names
5. **Handle edge cases**: Consider what happens with invalid inputs
