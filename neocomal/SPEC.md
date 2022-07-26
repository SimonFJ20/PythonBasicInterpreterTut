
# Neocomal Specification

## Keywords

- `int` [Integer]() value type
- `string` [String]() value type
- `proc` Definition start of a [Procedure]()
- `end` End of a code block

## Values

### Integer

64-bit signed integer value

```
0
-23
45678
```

### String

Immutable sequence of characters

```
""
"hello world"
"on\nseperate\nlines"
```

## Functions and Procedures

### Functions

A separated section of code with a reference, that generates output based on input

Functions are defined with a return type, a name, a list of parameters, some code, and an end statement

A parameter list, consists of between (inclusive) 0 to 4 parameters, declared as `type name`, seperated by commas

A function must always return a value with the `return <value>` keyword, and the type must be the same as the return type of the function definetion

*You should strive to make your functions "pure functions", meaning they only depend on the parameter input, and does not mutate or interact with the outer scope, and thereby limiting side effects and state dependency.*

```
int getDouble(int input)
    int double = input * 2
    return double
end

string numberAsString(int number)
    if number == 1 then
        return "one"
    else if number == 2 then
        return "two"
    else
        return "more than two"
end
```

### Procedures

Procedures are like functions, they have names, they take parameters, they have code and an end statement, except they never return a value

Procedures are used to generate side effects

Procedures are defined with the `proc` keyword, then a name, a parameter list, some code and an end statement

Procedures can use the `return` keyword, without a value, to stop executing and return to the previous location

```
import "std"

proc printHelloWorld()
    print("Hello world")
end
```

### 

## Features

### Main Procedure

Every program starts at the Main Procedure

```
proc main()
    // program starts here
end
```

### Global Contants

All symbols declared top level are immutabel

## STD Library

- `proc print(string value)` Print a [String]() to STDOUT

