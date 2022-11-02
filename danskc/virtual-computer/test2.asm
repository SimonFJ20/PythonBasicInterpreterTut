
offset: noop
one: noop

    mov [offset], (2 ** 11)
    mov [one], 1

    mov r1, 65
    mov r5, [offset]

.repeat:
    add r5, [one]
    store r5, r1

    mov ra, ((2**11) + (80*24))
    lt ra, r5
    xor ra, [one]
    jnz [.repeat], ra

    jmp [32000]