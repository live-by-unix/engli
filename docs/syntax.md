# Engli Syntax Reference

## Statement Punctuation

Engli uses specific punctuation rules:

- **Period (`.`)**: Terminates a statement
- **Comma (`,`)**: Continues a statement or separates elements
- **Colon (`:`)**: Starts a block

Example:
```engli
Set x to 10,
then add 5 to x,
then multiply x by 2.
```

## Comments

Single-line comments:
```engli
# This is a comment
```

Multiline comments:
```engli
/*
This is a
multiline comment
*/
```

## Indentation

Blocks use indentation with colons:
```engli
If condition:

    Statement 1.
    Statement 2.

Otherwise:

    Statement 3.
```

## Variables

Declaration:
```engli
Set name to "AB".
Set age to 20.
Set active to true.
```

Reassignment:
```engli
Set age to 21.
```

Arithmetic assignment:
```engli
Add 10 to score.
Subtract 5 from score.
Multiply score by 2.
Divide score by 2.
```

## Constants

```engli
Define the constant MAX_PLAYERS as 16.
```

## Literals

Numbers:
```engli
Set x to 42.
Set y to 3.14.
```

Strings:
```engli
Set text to "Hello, World!".
```

Booleans:
```engli
Set flag to true.
Set flag to false.
```

Nothing:
```engli
Set value to nothing.
```

## Expressions

Arithmetic:
```engli
Set result to 10 plus 5.
Set result to 10 minus 5.
Set result to 10 multiplied by 5.
Set result to 10 divided by 5.
Set result to 10 modulo 3.
```

Comparisons:
```engli
Set result to x is equal to y.
Set result to x is not equal to y.
Set result to x is greater than y.
Set result to x is less than y.
Set result to x is greater than or equal to y.
Set result to x is less than or equal to y.
```

Boolean logic:
```engli
Set result to x and y.
Set result to x or y.
Set result to not x.
```

## Conditionals

```engli
If condition:

    Statements.

Otherwise:

    Statements.
```

With else-if:
```engli
If condition:

    Statements.

Otherwise if another condition:

    Statements.

Otherwise:

    Statements.
```

## Loops

While:
```engli
While condition:

    Statements.

End the loop.
```

For each:
```engli
For each item in items:

    Statements.

End the loop.
```

For range:
```engli
For each number from 1 through 10:

    Statements.

End the loop.
```

Repeat:
```engli
Repeat 10 times:

    Statements.

End the repetition.
```

Forever:
```engli
Forever:

    Statements.

End the loop.
```

Break and continue:
```engli
Break out of the loop.
Continue with the next iteration.
```

## Functions

Definition:
```engli
Define a function called add that takes a and b:

    Return a plus b.

End the function.
```

Call:
```engli
Set result to add with 10 and 20.
```

## Data Structures

Lists:
```engli
Set numbers to a list containing 1, 2, 3, 4, and 5.
```

Maps:
```engli
Set person to a map containing:
    "name" mapped to "AB",
    "age" mapped to 20.
```

Sets:
```engli
Set unique to a set containing 1, 2, and 3.
```

Objects:
```engli
Create an object called player.
Set player.name to "Hero".
```

## Custom Types

```engli
Define a type called Player:
    A Player has a name which is text.
    A Player has health which is a number.
End the type.

Set player to a Player with:
    name equal to "Hero",
    health equal to 100.
```

## Enumerations

```engli
Define an enumeration called Direction containing:
    North,
    South,
    East,
    West.
End the enumeration.

Set direction to Direction.North.
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

## Error Handling

```engli
Try:

    Statements.

If an error occurs as error:

    Handle error.
```

Throwing errors:
```engli
Throw an error saying "Something went wrong".
```

## I/O

Output:
```engli
Say "Hello, World!".
```

Input:
```engli
Ask the user for their name and store the answer in name.
```

## File Operations

```engli
Read the file "data.txt" into contents.
Write contents to the file "output.txt".
Append "log" to the file "log.txt".
```

## HTTP

```engli
Send a GET request to "https://example.com"
and store the response in response.

Send a POST request to "https://api.example.com/users"
with JSON containing:
    "name" mapped to "AB"
and store the response in response.
```

## JSON

```engli
Parse data as JSON and store it in parsed.
Convert data to JSON and store it in json_string.
```

## Imports

Named import:
```engli
Import square from the file "./math.engli".
```

Module import:
```engli
Import the file "./math.engli".
```

Export:
```engli
Export function_name.
```
