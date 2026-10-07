# Engli Language

Engli is an English-like interpreted programming language with a deterministic grammar. It's designed to be readable while being unambiguous and executable.

## Philosophy

Engli reads like English but does NOT attempt to understand arbitrary English. It has a fixed, deterministic grammar with specific syntax rules. This makes it both readable to humans and parseable by computers.

## Key Characteristics

- **English-like syntax**: Statements read like natural English sentences
- **Deterministic grammar**: Fixed syntax rules, no ambiguity
- **Interpreted**: Code is executed directly by the Engli interpreter
- **Turing-complete**: Supports all general-purpose programming constructs
- **Safe**: Provides error handling and useful diagnostics

## Example

```engli
Set name to "World".
Say "Hello, {name}.".
```

This simple program demonstrates:
- Variable declaration with `Set ... to ...`
- String interpolation with `{variable}`
- Output with `Say`
- Statement termination with `.`

## Design Goals

1. **Readability**: Code should be understandable at a glance
2. **Predictability**: The same code always produces the same result
3. **Learnability**: The syntax should be intuitive for English speakers
4. **Expressiveness**: Support all common programming paradigms
5. **Safety**: Catch errors early with clear messages

## What Engli Is Not

- **Not an AI language parser**: Engli does not use LLMs or NLP to understand English
- **Not a toy**: It's a fully-functional programming language
- **Not a transpiler**: It doesn't convert to another language
- **Not ambiguous**: Every construct has one clear meaning

## Getting Started

See the [README](../README.md) for installation and first steps.

## Next Steps

- [Syntax Reference](syntax.md) - Detailed syntax documentation
- [Types](types.md) - Type system overview
- [Control Flow](control-flow.md) - Conditional and loop constructs
- [Functions](functions.md) - Function definition and usage
- [Modules](modules.md) - Import and module system
- [Standard Library](standard-library.md) - Built-in functionality
