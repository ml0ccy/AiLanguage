default rel

section .data
    prompt_name db 'Enter your name: ', 0
    prompt_exit db 'Press any key to exit..', 0
    hello_msg   db 'Hello, ', 0
    exclamation db '!', 0
    newline     db 10, 0 ; Newline for cleaner output
    format_str  db '%s', 0  ; Format string for scanf and printf
    buffer      times 256 db 0  ; Buffer for input (256 bytes)

section .text
extern printf
extern scanf
extern ExitProcess

global main
main:
    sub rsp, 40  ; Allocate shadow space (and align to 16 bytes)

    lea rcx, [prompt_name]
    call printf

    lea rcx, [format_str]
    lea rdx, [buffer]
    call scanf


    lea rcx, [hello_msg]
    call printf

    lea rcx, [format_str]
    lea rdx, [buffer]
    call printf
    
    lea rcx, [exclamation]
    call printf
    
    lea rcx, [newline]
    call printf

    lea rcx, [prompt_exit]
    call printf

    lea rcx, [format_str]
    lea rdx, [buffer]  ; Reuse the buffer
    call scanf

    xor rcx, rcx        ; Set exit code to 0
    call ExitProcess