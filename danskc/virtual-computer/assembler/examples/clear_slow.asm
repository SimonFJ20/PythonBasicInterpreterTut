
; r5 = pointer
; r6 = stack pointer
; r7 = base stack pointer
iv:
    noop
    noop
    noop
    noop
    noop

_entry:
    ; initialize int values
    mov ra, 0
    mov r1, 1
    mov [iv], ra
    add ra, r1
    mov [iv + 1], ra
    add ra, r1
    mov [iv + 2], ra
    add ra, r1
    mov [iv + 3], ra

    ; initialize stack
    mov r6, (2 ** 12)
    mov r7, r6

    ; call main
    mov r5, ._entry_return
    store r6, r5
    jmp main
._entry_return:
    jmp _exit

vram_offset: noop
vram_size: noop

clear_screen:
    ; enter
    add r6, [iv + 1]
    store r6, r7
    mov r7, r6
    
    ; let i = 0
    mov r2, 0
    ; let m = vram_size
    mov r3, [vram_size]

.continue:
    ; i < m
    mov ra, r2 ; i
    lt ra, r3
    xor ra, [iv + 1]
    jnz .break, ra

    ; vram_offset[i] = ' '
    mov r5, [vram_offset]
    add r5, r2
    mov ra, 66
    store r5, ra

    ; i++
    add r2, [iv + 1]

    jmp .continue
.break:
    ; return
    mov r6, r7
    load r7, r6
    sub r6, [iv + 1]
    load r5, r6
    sub r6, [iv + 1]
    jmp r5

main:
    ; enter
    add r6, [iv + 1]
    store r6, r7
    mov r7, r6

    mov [vram_offset], (2 ** 11)
    mov [vram_size], (80 * 24)

    add r6, [iv + 1]
    mov r5, .return
    store r6, r5
    jmp clear_screen
.return:

    ; return
    mov r6, r7
    load r7, r6
    sub r6, [iv + 1]
    load r5, r6
    sub r6, [iv + 1]
    jmp r5

_exit:
    jmp (2 ** 14)
