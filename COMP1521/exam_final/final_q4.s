# this code reads 1 integer and prints it
# change it to read integers until their sum is >= 42
# and then print their sum

main:
    li   $t1, 0        #   int sum = 0
loop:
    bge $t1, 42, loopend # while sum < 42
    li   $v0, 5        #   scanf("%d", &x);
    syscall
    move $t2, $v0
    add $t1, $t1, $t2
    j loop      
loopend:
    move $a0, $t1      #   printf("%d\n", x);
    li   $v0, 1
    syscall

    li   $a0, '\n'     #   printf("%c", '\n');
    li   $v0, 11
    syscall

    li   $v0, 0        # return 0
    jr   $ra
