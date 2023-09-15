# this code reads 1 integer and prints it
# add code so that prints 1 iff
# the least significant (bottom) byte of the number read
# is equal to the 2nd least significant byte
# and it prints 0 otherwise

main:
    li   $v0, 5
    syscall

    move $t0, $v0

    li $t1, 255

    and $t2, $t0, $t1
    sll $t1, $t1, 8
    and $t3, $t0, $t1
    srl $t3, $t3, 8
    bne $t3, $t2, printzero

printone:
    li  $a0, 1
    li   $v0, 1
    syscall
    j end
printzero:
    li $a0, 0
    li $v0, 1
    syscall
end:
    li   $a0, '\n'
    li   $v0, 11
    syscall

    li   $v0, 0
    jr   $ra
