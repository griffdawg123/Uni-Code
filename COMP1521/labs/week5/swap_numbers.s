# read 10 numbers into an array
# swap any pairs of of number which are out of order
# then print the 10 numbers

# i in register $t0,
# registers $t1 - $t3 used to hold temporary results

main:

    li $t0, 0           # i = 0
loop0:
    bge $t0, 10, end0   # while (i < 10) {

    li $v0, 5           #   scanf("%d", &numbers[i]);
    syscall             #

    mul $t1, $t0, 4     #   calculate &numbers[i]
    la $t2, numbers     #
    add $t3, $t1, $t2   #
    sw $v0, ($t3)       #   store entered number in array

    add $t0, $t0, 1     #   i++;
    b loop0             # }
end0:

    li $t0, 1   #i = 1;
    li $t1, 0   #swapped = 0;
    la $t2, numbers # start of array
    li $t3, 0 # index of array

swaploop:
    bge $t0, 10, endswap   #   while (i < 10) {

    mul $t4, $t0, 4     # calculate &numbers[i]
    add $t3, $t2, $t4   # add offset to array start
    lw  $t5, ($t3)      # numbers[i]
    sub $t3, $t3, 4     
    lw $t6, ($t3)       # numbers[i-1]

    bge $t5, $t6, loopend

    #swap
    sw $t5, ($t3)
    add $t3, $t3, 4
    sw $t6, ($t3)


loopend:
    add $t0, $t0, 1 # i++;
    j swaploop

endswap:
    li $t0, 0           # i = 0
loop1:
    bge $t0, 10, end1   # while (i < 10) {

    mul $t1, $t0, 4     #   calculate &numbers[i]
    la $t2, numbers     #
    add $t3, $t1, $t2   #
    lw $a0, ($t3)       #   load numbers[i] into $a0
    li $v0, 1           #   printf("%d", numbers[i])
    syscall

    li   $a0, '\n'      #   printf("%c", '\n');
    li   $v0, 11
    syscall

    add $t0, $t0, 1     #   i++
    b loop1             # }
end1:

    jr $31              # return

.data

numbers:
    .word 0 0 0 0 0 0 0 0 0 0  # int numbers[10] = {0};

