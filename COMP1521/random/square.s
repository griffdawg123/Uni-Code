main:
    la $a0, string0
    li $v0, 4
    syscall

    li $v0, 5
    syscall

    mul $t0, $v0, $v0
    move $a0, $t0
    li $v0, 1
    syscall

    li $a0, '\n'
    li $v0, 11
    syscall
    b end

end:
    li $v0, 0
    jr $ra

    .data
string0:
    .asciiz "Enter a number: "
