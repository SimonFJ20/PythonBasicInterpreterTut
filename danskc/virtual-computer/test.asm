
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
    add ra, r1
    mov [iv + 1], ra

    ; initialize stack
    mov r6, (2 ** 12)

    ; call main
    mov r5, ._entry_return
    store r6, r5
    mov r5, main
    jmp r5
._entry_return:
    mov r5, _exit
    jmp r5

vram_offset: noop
vram_size: noop

clear_screen:
    ; enter
    add r6, [iv + 1]
    store r6, r7
    mov r7, r6
    ; allocate stack frame
    add r6, [iv + 2]
    
    ; let i = 0
    store r6, [iv + 0]
    
    ; let m = vram_size
    mov r5, r6
    sub r5, [iv + 1]
    mov ra, [vram_size]
    store r5, ra

.loop_continue:
    ; i < m
    load ra, r6 ; i
    mov r5, r6
    sub r5, [iv + 1]
    load r1, r5 ; m
    lt ra, r1
    xor ra, [iv + 0]
    mov ra, 1
    mov r5, .loop_break 
    jnz r5, ra

    ; vram_offset[i] = ' '
    load ra, r6 ; i
    mov r5, [vram_offset]
    add r5, ra
    mov ra, 32
    store r5, ra

    ; i++
    load ra, r6 ; i
    add ra, [iv + 1]
    store r6, ra

    mov r5, .loop_continue
    jmp r5
.loop_break:
    ; return
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

    sub r6, [iv + 1]
    mov r5, .main_return
    store r6, r5
    mov r5, clear_screen
    jmp r5

.main_return:
    ; return
    load r7, r6
    sub r6, [iv + 1]
    load r5, r6
    sub r6, [iv + 1]
    jmp r5

_exit:
    mov r5, 16000
    jmp r5
