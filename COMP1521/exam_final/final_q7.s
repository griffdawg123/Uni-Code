# this code reads 1 integer and prints it
# change it to read integers until their sum is >= 42
# and then print theintgers read in reverse order

main:
    li $t1, 0   # int i = 0
    li $t2, 0   # int sum = 0
loop1:
    bge $t2, 42, loop2
    li   $v0, 5        #   scanf("%d", &x);
    syscall            #
    move $t3, $v0       # int x
    la $t4, array   # get array address
    mul $t5, $t1, 4 # multiply index by 4
    add $t4, $t4, $t5 # find location to store new int
    sw $t3, ($t4)   # numbers[i] = x;
    add $t1, $t1, 1 # i++;
    add $t2, $t2, $t3   # sum += x;
    j loop1

loop2:
    blez $t1, loopend
    sub $t1, $t1, 1
    la $t4, array   # get array address
    mul $t5, $t1, 4 # multiply index by 4
    add $t4, $t4, $t5 # find location of int
    lw $t3, ($t4)   # numbers[i] = x;

    move $a0, $t3      #   printf("%d\n", x);
    li   $v0, 1
    syscall

    li   $a0, '\n'     #   printf("%c", '\n');
    li   $v0, 11
    syscall

    j loop2

loopend:





    li   $v0, 0        # return 0
    jr   $ra

array:  .space 4000 # 1000 size int array
