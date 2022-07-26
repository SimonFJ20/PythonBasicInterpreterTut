# mamemalang
Manual Memory Management Programming Language

## Roadmap

 - [ ] Parser in Python
 - [ ] Interpreter in Python
 - [ ] BC Compiler in Python
 - [ ] BC VM in Python
 - [ ] BC VM in C

## Memory Management

No pointers.
Primitives by value.
Objects bt reference.

### Manually

The `allocate` function allocates a chunk the size of the given struct,
and returns the reference. Note, the object is NOT constructed jet.

```
MyClass object = allocate(object);
```

Objects are constructed by calling the `constructor`.

```
object.constructor();
```

After using the object, it can be deallocated by calling `destroy` on it.
This will first call the `destructor` of the object, then deallocate the object;

```
destroy(object);
```

With all together.

```
func myFunction() {
    MyClass object = allocate(object);
    object.constructor();

    destroy(object);
}
```

With some syntactic suger.

```
func myFunction() {
    MyClass object = MyClass();

    destroy(object);
}
```

### Automatically

Using the ownership model, the compiler can act like a garbage collecter.

```
func main() {
    Person a = Person("Larry");
    // `a` now owns the instance of Person aka. Larry

    a.waveTo(); // we can reference Larry
    a.xPos = 7; // and mutate Larry

    
    Person b = a;
    // `b` now owns Larry
    // `a` is no longer useable

    b.waveTo(); // with `b`, we can reference Larry
    b.xPos = 7; // with `b`, and mutate Larry

    a.waveTo(); // with `a`, we CANNOT reference Larry
    a.xPos = 7; // with `a`, and CANNOT mutate Larry

    //Person& c = reference(b);
    Person& c = &b;
    // `b` still owns Larry
    // `c` does not own, but has an immutable reference

    b.waveTo(); // with `b`, we can reference Larry
    b.xPos = 7; // with `b`, and mutate Larry

    c.waveTo(); // with `c`, we CAN reference Larry
    c.xPos = 7; // with `c`, and CANNOT mutate Larry

}
```
