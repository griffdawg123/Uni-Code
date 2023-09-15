# this code reads a line of input and prints 42
# change it to evaluate the arithmetic expression

main:
    la   $a0, line
    la   $a1, 10000
    li   $v0, 8          # fgets(buffer, 256, stdin)
    syscall              #

    la $t0, line    # s
    li $t1, 0       # value of expression
    sub $sp, $sp, 8 #saving s and $ra onto the stack
    sw $t0, 4($sp)
    sw $ra, 0($sp)

    jal expression
    
    move $t1, $v0 # set $t1 to be the evaluated expression
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

expression:
    li $t1, 0 #int left
    lw $t0, 4($sp) # $t0 = *s

    sub $sp, $sp, 8 # save *s and return adress on stack
    sw $t0, 4($sp)
    sw $ra, 0($sp)

    jal expression

    move $t1, $v0 # set $t1 to be the evaluated expression
    lw $t0, 4($sp)
    lw $ra, 0($sp)

    add $sp, $sp, 8

    lb $t3, ($t0)
    bne $t3, '+', leftE
    add $t0, $t0, 1 # s++;
    li $t2, 0; # int right

    sub $sp, $sp, 12
    sw $t1, 8($sp)
    sw $t0, 4($sp)
    sw $ra, 0($sp)

    jal term

    move $t2, $v0 # set $t1 to be the evaluated expression
    lw $t1, 8($sp)
    lw $t0, 4($sp)
    lw $ra, 0($sp)

    add $sp, $sp, 12
    j leftrightE
leftE:
    move $v0, $t1
    sw $t0, 4($sp)
    jr $ra
leftrightE:
    add $v0, $t1, $t2
    sw $t0, 4($sp)
    jr $ra

term:
    li $t1, 0 #int left
    lw $t0, 4($sp) # $t0 = *s

    sub $sp, $sp, 8 # save *s and return adress on stack
    sw $t0, 4($sp)
    sw $ra, 0($sp)

    jal number

    move $t1, $v0 # set $t1 to be the evaluated expression
    lw $t0, 4($sp)
    lw $ra, 0($sp)

    add $sp, $sp, 8

    lb $t3, ($t0)
    bne $t3, '*', leftE
    add $t0, $t0, 1 # s++;
    li $t2, 0; # int right

    sub $sp, $sp, 12
    sw $t1, 8($sp)
    sw $t0, 4($sp)
    sw $ra, 0($sp)

    jal term

    move $t2, $v0 # set $t1 to be the evaluated expression
    lw $t1, 8($sp)
    lw $t0, 4($sp)
    lw $ra, 0($sp)

    add $sp, $sp, 12
    j leftrightT
leftT:
    move $v0, $t1
    sw $t0, 4($sp)
    jr $ra
leftrightT:
    mul $v0, $t1, $t2
    sw $t0, 4($sp)
    jr $ra

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
    jr $ra

.data
line:
    .space 10000


