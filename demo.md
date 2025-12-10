# Markdown ASCII Renderer Demo

This document demonstrates all the features of the markdown ASCII renderer.

## Headers (Level 2)
Headers come in different levels:

### Bold Text (Level 3)
You can make text **bold** using double asterisks or double underscores: __this is also bold__.

### Italic Text (Level 3)
You can make text *italic* using single asterisks or single underscores: _this is also italic_.

### Combined Formatting
You can combine **bold and *italic* text** together.

## Code
### Inline Code
You can use `inline code` with backticks. For example, `print("Hello, World!")` or `const x = 42;`.

### Code Blocks

You can create code blocks with triple backticks:

```
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

You can also specify a language:

```python
def greet(name):
    print(f"Hello, {name}!")
    return True
```

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
    return true;
}
```

## Links and Images

### Links

Here are some examples of links:
- [Example.com](https://example.com)
- [GitHub](https://github.com)
- [Python Documentation](https://docs.python.org)

You can also have inline links like this: Check out [Python](https://python.org) for more information.

### Images

Images are rendered as text descriptions:
![Python Logo](https://python.org/logo.png)
![Example Image](https://example.com/image.jpg)

## Lists

### Unordered Lists

You can create unordered lists with dashes or asterisks:

- First item
- Second item
- Third item
  - Nested item
  - Another nested item
- Fourth item

Or with asterisks:

* Apple
* Banana
* Cherry

### Ordered Lists

You can create ordered lists:

1. First item
2. Second item
3. Third item
   1. Nested numbered item
   2. Another nested item
4. Fourth item

## Blockquotes

You can create blockquotes with the `>` character:

> This is a blockquote.
> It can span multiple lines.
> 
> You can have multiple paragraphs in a blockquote.

> Another blockquote example.
> 
> Blockquotes are great for highlighting important information.

## Horizontal Rules

You can create horizontal rules with three or more dashes or asterisks:

---

***

---

## Mixed Content Example

Here's an example that combines multiple features:

### Project Setup

To get started with this project:

1. Clone the repository using `git clone https://github.com/example/repo.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

> **Note:** Make sure you have Python 3.8+ installed.

For more information, visit the [project homepage](https://example.com/project).

```bash
#!/bin/bash
echo "Setting up project..."
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Complex Example

Here's a more complex example showing nested structures:

### Documentation

This section demonstrates **complex formatting**:

- **Bold items** in lists
- *Italic items* in lists
- Items with `code` in them
- Items with [links](https://example.com)

> **Important:** Always test your code before deploying.
> 
> Use `pytest` for testing: `pytest tests/`

```python
class Example:
    """An example class."""
    
    def __init__(self, name: str):
        self.name = name
    
    def greet(self):
        print(f"Hello, {self.name}!")
```

For more examples, see the [documentation](https://docs.example.com).

---

## Conclusion

This markdown renderer supports:

- ✅ Headers (all 6 levels)
- ✅ **Bold** and *italic* text
- ✅ `Inline code` and code blocks
- ✅ [Links](https://example.com) and images
- ✅ Ordered and unordered lists
- ✅ Blockquotes
- ✅ Horizontal rules
- ✅ Custom handler registration

Enjoy using the markdown ASCII renderer!

