# Modules and Imports in Engli

Engli supports a module system for organizing code into reusable files.

## Exporting Symbols

Export a function or variable from a module:
```engli
Define a function called square that takes x:

    Return x multiplied by x.

End the function.

Export square.
```

## Named Import

Import a specific symbol from a file:
```engli
Import square from the file "./math.engli".

Set result to square with 5.
```

## Module Import

Import an entire module:
```engli
Import the file "./math.engli".

Set result to math.square with 5.
```

## Relative Paths

Imports are resolved relative to the importing file:
```engli
Import square from the file "./math.engli".
Import square from the file "../utils/math.engli".
Import square from the file "/absolute/path/math.engli".
```

## Module Caching

Engli caches loaded modules to avoid redundant loading and prevent infinite circular imports.

## Circular Imports

Engli detects and prevents circular import dependencies.

## Example Module Structure

`math.engli`:
```engli
Define a function called square that takes x:

    Return x multiplied by x.

End the function.

Define a function called cube that takes x:

    Return x multiplied by x multiplied by x.

End the function.

Export square.
Export cube.
```

`main.engli`:
```engli
Import square from the file "./math.engli".
Import cube from the file "./math.engli".

Say square with 5.
Say cube with 3.
```

## Module Best Practices

1. **Organize logically**: Group related functions in modules
2. **Export selectively**: Only export symbols that should be public
3. **Use clear names**: Module and symbol names should be descriptive
4. **Avoid circular dependencies**: Structure modules to avoid circular imports
5. **Document modules**: Use README files or comments to document module purpose
