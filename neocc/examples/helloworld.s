.global _start

.data
string1:
    .ascii "Hello world!\n"
    string1_len = . - string1

.text
_start:
    mov $4, %rax
    mov $1, %rbx
    mov $string1, %rcx
    mov $string1_len, %rdx
    int $0x80

exit:
    mov $1, %rax
    mov $0, %rbx
    int $0x80
    