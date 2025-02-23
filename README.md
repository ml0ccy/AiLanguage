# AILanguage: Innovative Programming Language with AI-Powered Compilation

**AILanguage** is an innovative programming language that utilizes Artificial Intelligence for compilation. Instead of a traditional compiler, AILanguage employs an **Artificial Intelligence** model to understand and translate AILanguage code into Assembly language (NASM for x86-64 architecture).

This project is under active development and aims to be a unique platform.

## Key Features

*   **Simple and Readable Syntax:** AILanguage is designed with a syntax similar to C or Python. Its syntax is simple, yet it remains a compilable programming language.
*   **Fundamental Data Types:** Supports integers (`int`), strings (`string`), floating-point numbers (`float`, `double`), and booleans (`bool`).
*   **Control Flow Structures:** Includes `if`, `else`, `while`, and `for` statements for program control flow.
*   **Functions:**  Allows defining and calling functions with parameters and return values.
*   **Arrays and Structures:** Supports static arrays and user-defined structures for data organization.
*   **Standard Library:**  Provides a basic standard library with functions for string manipulation (`strlen`, `substring`, `strcat`, `strcmp`, `atoi`, `itoa`) and input/output (`print`).
*   **AI-Powered Compilation:**  The core innovation - an AI model is used to compile AILanguage code into NASM Assembly.
*   **Easy to Extend and Improve:**  Thanks to the AI-powered compiler, AILanguage is designed to be easily extended with new features and improved over time.  Adding new language constructs or optimizing code generation can be achieved by simply updating the AI's "documentation" and training data, making the development process more flexible and iterative compared to traditional compilers.

## Getting Started

1.  **Download NASM:** [https://www.nasm.us/pub/nasm/releasebuilds/2.16.01/win64/](https://www.nasm.us/pub/nasm/releasebuilds/2.16.01/win64/)
2.  **Download Mingw-64:** [https://www.mingw-w64.org/](https://www.mingw-w64.org/)
3.  **Explore Examples:** Check out the `samples/` directory for example AILanguage programs.
4.  **Write your AILanguage code:** Create a file with the `.ail` extension (e.g., `test.ail`).
5.  **Compile your code:** Run the `compiler.py` script (or your compiled compiler), providing the path to your `.ail` file as an argument.
    ```bash
    python compiler.py test.ail
    ```
6.  **Done:** The compiler will automatically assemble and link the files into an `.exe`. If you encounter linking or assembling errors, it's possible that the compiler provided incorrect `.asm` code, or you added functions to the `.ail` file that are not in the documentation for the AI. This could cause the compiler to compile incorrectly.

## Documentation

The documentation for the AI regarding AILanguage syntax, functions, and the standard library is located in the `docs/ail_reference_ru.ail` file (currently in Russian). This documentation serves as the brain for the compiler, but you as a user can also try to study it.
User documentation is planned for release in the near future.

## Examples

See the `samples/` directory for example AILanguage programs demonstrating various language features. Don't be afraid to write your own programs and test them, as well as experiment with prompts and documentation for the AI.

## Contributing

Contributions are welcome! If you are interested in contributing to AILanguage, we are looking for help with:

*   Improving the AI compiler model
*   Expanding the standard library
*   Writing documentation (especially English documentation)
*   Creating new examples and tutorials
*   Developing a VS Code extension for AILanguage

## License

AILanguage is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## Contacts

You can write comments in the official Telegram channel for the AILanguage language: [https://t.me/AiLangu](https://t.me/AiLangu)
Also, the author's Telegram channel: [https://t.me/mloccy](https://t.me/mloccy)

---

**Try AILanguage and discover the exciting world of AI-powered compilation!**
