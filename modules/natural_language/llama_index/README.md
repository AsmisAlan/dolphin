This is a poc, this approach works but is not so good, its take too much time.

with the given data I created this:

# Printing in Python

Python offers a variety of ways to print to the console or terminal window. In this tutorial, we'll explore the different methods of printing in Python, and how to use them.

## Using the print() Function

The simplest and most common way of printing in Python is by using the built-in `print()` function. The `print()` function takes one or more arguments, and prints them to the standard output, which is usually the console or terminal window.

For example, to print the string "Hello World":

```python
print("Hello World")
```

This will output `Hello World` to the console.

## Printing in the Middle of the Screen

Python 3 offers the `shutil.get_terminal_size()` function, which returns a tuple with the current terminal size. Then, `str.center()` can be used to center text using spaces.

Here's an example of how to print "hello world" in the middle of the screen using Python 3:

```python
import shutil

columns = shutil.get_terminal_size().columns
print("hello
```
