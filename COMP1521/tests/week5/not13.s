main:
    li $v0, 5           #   scanf("%d", &x);
    syscall             #
    move $t0, $v0

    li $v0, 5           #   scanf("%d", &y);
    syscall             #
    move $t1, $v0

    move $t3 $t0
    add $t3, $t3, 1
loop:
    bge $t3, $t1, end
    beq $t3, 13, looper

    move $a0, $t3          #   printf("%d\n", 42);
    li $v0, 1
    syscall
    li   $a0, '\n'      #   printf("%c", '\n');
    li   $v0, 11
    syscall

looper:
    add $t3, $t3, 1
    j loop
    
end:

    li $v0, 0           # return 0
    jr $31
