
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
    
    ; let i = vram_offset
    mov r2, (2 ** 11)
    ; let m = vram_offset + vram_size
    mov r3, ((2 ** 11) + (80 * 24) - 1)

.continue:
    mov ra, r3 ; m
    lt ra, r2 ; m < i
    jnz .break, ra

    ; vram_offset[i] = ' '
    mov ra, 65
    store r2, ra

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
