# read a line and print whether it is a palindrom

main:
    la   $a0, str0       # printf("Enter a line of input: ");
    li   $v0, 4
    syscall

    la   $a0, line
    la   $a1, 256
    li   $v0, 8          # fgets(buffer, 256, stdin)
    syscall              #

    li $t0 0             # int i = 0;
    la $t1 line
loop1:
    lb $t2, ($t1)
    beqz $t2, loop1end
    add $t0, $t0, 1
    add $t1, $t1, 1
    j loop1
loop1end:
    li $t2 0          # int j = 0;
    move $t3, $t0
    sub $t3, $t3, 2     # int k = i-2;

loop2:
    bge $t2, $t3, ispal
    la $t4, line
    la $t5, line
    add $t4, $t4, $t2
    add $t5, $t5, $t3
    lb $t6 ($t4)
    lb $t7 ($t5)
    bne $t6, $t7, isnotpal

    add $t2, $t2, 1
    sub $t3, $t3, 1
    j loop2
ispal:
    la   $a0, palindrome
    li   $v0, 4
    syscall
    j end

isnotpal:
    la   $a0, not_palindrome
    li   $v0, 4
    syscall
 
end:
    li   $v0, 0          # return 0
    jr   $31


.data
str0:
    .asciiz "Enter a line of input: "
palindrome:
    .asciiz "palindrome\n"
not_palindrome:
    .asciiz "not palindrome\n"


# line of input stored here
line:
    .space 256

