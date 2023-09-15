main:
    la   $a0, line
    la   $a1, 10000
    li   $v0, 8          # fgets(buffer, 256, stdin)
    syscall  

    la $t0, line
    li $t1, 0

    sub $sp, $sp, 8
    sw $t0, 4($sp)
    sw $ra, 0($sp)

    jal number

    move $t1, $v0
    lw $t0, 4($sp)
    lw $ra, 0($sp)
    add $sp, $sp, 8

    move $a0, $t1         # printf("%d", expression());
    li   $v0, 1
    syscall

    li   $a0, '\n'       # printf("%c", '\n');
    li   $v0, 11
    syscall

    li   $v0, 0          # return 0
    jr   $31


number:
    li $t0, 0 # int n = 0;
    lw $t1, 4($sp)
loop:
    
    lb $t2, ($t1) # resolve s*
    blt $t2, '0' return
    bgt $t2, '9' return
    mul $t0, $t0, 10
    add $t0, $t0, $t2
    sub $t0, $t0, '0'
    add $t1, $t1, 1
    j loop
return:
    move $v0, $t0
    sw $t1, 4($sp)
    lw $ra, 0($sp)
    jr $ra

.data
line:
    .space 10000