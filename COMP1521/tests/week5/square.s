main:
    li $v0, 5           #   scanf("%d", &x);
    syscall             #
    move $t0, $v0

    li $t1, 0
looprow:
    bge $t1, $t0, end
    li $t2, 0
loopcol:
    bge $t2, $t0, colend
    li $a0, '*'          #   printf("%d\n", '*');
    li $v0, 11
    syscall
    add $t2, $t2, 1
    j loopcol
colend:
    li   $a0, '\n'      #   printf("%c", '\n');
    li   $v0, 11
    syscall
    add $t1, $t1, 1
    j looprow
end:
    li $v0, 0           # return 0
    jr $31
