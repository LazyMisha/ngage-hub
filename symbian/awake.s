@ ARMv4T extension for EKA1 and Nokia's PyS60 1.3.1.
.syntax unified
.arm
.text
.balign 4
image:
entry:
    mov r0, #0
    bx lr

@ PyS60 loads the Python module initializer from export ordinal 1.
init_module:
    push {r4, lr}
    sub sp, sp, #8
    ldr r4, python_api_version
    str r4, [sp]
    adr r0, module_name
    adr r1, methods
    mov r2, #0
    mov r3, #0
    ldr ip, import_init_module
    mov lr, pc
    bx ip
    add sp, sp, #8
    pop {r4, lr}
    bx lr

reset_idle:
    push {r4, lr}
    ldr ip, import_reset_idle
    mov lr, pc
    bx ip
    mov r0, #0
    pop {r4, lr}
    ldr ip, import_int_from_long
    bx ip

python_api_version:
    .word 1011
module_name:
    .asciz "_ngageawake"
reset_name:
    .asciz "reset"
.balign 4
methods:
method_name_pointer:
    .word 0x10000000 + (reset_name - image)
method_function_pointer:
    .word 0x10000000 + (reset_idle - image)
    .word 4, 0                  @ METH_NOARGS, no doc string
    .word 0, 0, 0, 0            @ PyMethodDef sentinel

@ PETRAN PE-style import address table. The Symbian loader replaces the
@ ordinals with addresses before PyS60 calls init_module.
import_reset_idle:
    .word 933                   @ euser: User::ResetInactivityTime()
import_int_from_long:
    .word 164                   @ python222: PyInt_FromLong
import_init_module:
    .word 530                   @ python222: Py_InitModule4
    .word 0
export_table:
    .word init_module - image
