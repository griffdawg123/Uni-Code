# this code reads 1 integer and prints it
# change it to read 2 integers
# then print their sum

main:
    li   $v0, 5        #   scanf("%d", &x);
    syscall            #

    move $t1, $v0

    li $v0, 5
    syscall

    add $t1, $t1, $v0

    move $a0, $t1      #   printf("%d\n", x);
    li   $v0, 1
    syscall

    li   $a0, '\n'     #   printf("%c", '\n');
    li   $v0, 11
    syscall

    li   $v0, 0        # return 0
    jr   $ra
