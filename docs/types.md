# Engli Types

Engli has a rich type system with several built-in types and support for user-defined types.

## Built-in Types

### Number

Integer values:
```engli
Set x to 42.
```

### Decimal

Floating-point values:
```engli
Set pi to 3.14.
```

### Text

String values:
```engli
Set name to "AB".
```

### Boolean

True/false values:
```engli
Set active to true.
Set inactive to false.
```

### Nothing

Represents the absence of a value:
```engli
Set value to nothing.
```

### List

Ordered collection of values:
```engli
Set numbers to a list containing 1, 2, 3, 4, and 5.
```

List operations:
```engli
Say numbers at index 0.
Set numbers at index 0 to 100.
Add 6 to numbers.
Remove 3 from numbers.
Say the length of numbers.
```

### Map

Key-value pairs:
```engli
Set person to a map containing:
    "name" mapped to "AB",
    "age" mapped to 20.
```

Map operations:
```engli
Say person at "name".
Set person at "age" to 21.
```

### Set

Unordered collection of unique values:
```engli
Set unique to a set containing 1, 2, and 3.
```

### Function

First-class function values:
```engli
Define a function called add that takes a and b:
    Return a plus b.
End the function.

Set operation to add.
```

### Object

Runtime objects with properties:
```engli
Create an object called player.
Set player.name to "Hero".
Set player.health to 100.
```

### Type

User-defined type definitions:
```engli
Define a type called Player:
    A Player has a name which is text.
    A Player has health which is a number.
End the type.
```

### Enum

Enumeration definitions:
```engli
Define an enumeration called Direction containing:
    North,
    South,
    East,
    West.
End the enumeration.
```

### Error

Error values for error handling:
```engli
Throw an error saying "Invalid input".
```

## User-Defined Types

### Type Declaration

```engli
Define a type called Player:
    A Player has a name which is text.
    A Player has health which is a number.
    A Player has score which is a number.
End the type.
```

### Type Construction

```engli
Set player to a Player with:
    name equal to "Hero",
    health equal to 100,
    score equal to 0.
```

### Enumerations

```engli
Define an enumeration called Direction containing:
    North,
    South,
    East,
    West.
End the enumeration.

Set direction to Direction.North.
```

## Type Coercion

Engli performs automatic type coercion in certain contexts:

- Numbers and decimals can be used together in arithmetic
- Text can be concatenated with other text
- Lists, maps, and sets have specific operation rules

## Optional Values

Handle potentially missing values:
```engli
Set username to nothing.

If username exists:

    Say username.

Otherwise:

    Say "No username".

Set name to username or "Guest".
```

## Type Checking

The semantic analyzer performs static type checking where possible:
- Detects undefined variables
- Validates function calls
- Checks type consistency in operations

Runtime type checking is also performed for dynamic operations.
