# Engli

An English-like interpreted programming language.

## What is Engli?

Engli is a serious, general-purpose, Turing-complete programming language that reads like English but uses a deterministic grammar. It's implemented as an interpreter in Python 3.12+.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## First Program

Create `hello.engli`:

```engli
Set name to "World".
Say "Hello, {name}.".
```

Run it:

```bash
engli hello.engli
```

Output:

```
Hello, World.
```

## Running Programs

```bash
engli main.engli
engli run main.engli
```

## REPL

Start the interactive REPL:

```bash
engli repl
```

Example session:

```
Engli REPL 0.1.0

> Set x to 10.
> Add 5 to x.
> Say x.
15
>
```

## CLI Commands

- `engli <file>` - Run an Engli program
- `engli run <file>` - Run an Engli program
- `engli repl` - Start the REPL
- `engli check <file>` - Lex, parse, and semantically check without executing
- `engli format <file>` - Format an Engli file
- `engli test` - Run the test suite
- `engli version` - Show version information
- `engli help` - Show help

## Language Overview

Engli uses English-like syntax with a deterministic grammar:

```engli
Set name to "AB".
Set age to 20.

If age is greater than or equal to 18:

    Say "Hello, {name}.".
```

### Key Features

- **Variables**: `Set x to 10.`
- **Arithmetic**: `Set result to (10 plus 5) multiplied by 2.`
- **Conditionals**: `If condition: ... Otherwise: ...`
- **Loops**: `While condition: ... End the loop.`
- **Functions**: `Define a function called add that takes a and b: ... End the function.`
- **Lists**: `Set numbers to a list containing 1, 2, 3, 4, and 5.`
- **Maps**: `Set person to a map containing: "name" mapped to "AB", "age" mapped to 20.`
- **Objects**: `Create an object called player. Set player.name to "Hero".`
- **Custom Types**: `Define a type called Player: ... End the type.`
- **Enumerations**: `Define an enumeration called Direction containing: North, South, East, West.`
- **Pattern Matching**: `Match direction: When direction is Direction.North: ... End the match.`
- **Filesystem**: `Read the file "data.txt" into contents.`
- **Terminal Commands**: `Run the command "git" with arguments "status" and store the result in result.`
- **HTTP**: `Send a GET request to "https://example.com" and store the response in response.`
- **JSON**: `Parse response.body as JSON and store it in data.`
- **Imports**: `Import square from the file "./math.engli".`
- **Error Handling**: `Try: ... If an error occurs as error: ...`
- **Concurrency**: `Start a task: ... Wait for task to finish.`

## Examples

See the `examples/` directory for working examples:

- `hello.engli` - Hello World
- `variables.engli` - Variables and arithmetic
- `conditions.engli` - Conditionals
- `loops.engli` - Loops
- `functions.engli` - Functions
- `recursion.engli` - Recursion
- `lists.engli` - Lists
- `maps.engli` - Maps
- `objects.engli` - Objects
- `filesystem.engli` - Filesystem operations
- `terminal.engli` - Terminal commands
- `http.engli` - HTTP requests
- `json.engli` - JSON handling
- `errors.engli` - Error handling
- `imports.engli` - Imports and modules
- `concurrency.engli` - Concurrency
- `everything.engli` - Comprehensive showcase

## Architecture

Engli follows a traditional interpreter architecture:

1. **Source Loader** - Reads `.engli` files
2. **Lexer** - Converts source to tokens
3. **Parser** - Builds AST from tokens
4. **Semantic Analyzer** - Validates the AST
5. **Interpreter** - Executes the AST
6. **Runtime** - Provides values, environment, and standard library

## Project Status

**Version**: 1.0.0

Engli is in active development. The core language features are implemented and tested.

## Development

### Setup

```bash
git clone https://github.com/live-by-unix/engli
cd engli
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Testing

```bash
engli test
# or
pytest
```

### Formatting

```bash
black src/ tests/
ruff check src/ tests/
mypy src/
```

## Documentation

See the `docs/` directory for detailed documentation:

- `language.md` - Language overview
- `syntax.md` - Syntax reference
- `types.md` - Type system
- `control-flow.md` - Control flow
- `functions.md` - Functions
- `modules.md` - Modules and imports
- `standard-library.md` - Standard library
- `terminal.md` - Terminal and shell commands
- `http.md` - HTTP/REST
- `errors.md` - Error handling
- `repl.md` - REPL usage

## License

MIT License - see LICENSE file for details.

## Contributing

See CONTRIBUTING.md for contribution guidelines.
