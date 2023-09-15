# Read a number and print positive multiples of 7 or 11 < n

main:                  # int main(void) {

    la $a0, prompt     # printf("Enter a number: ");
    li $v0, 4
    syscall

    li $v0, 5           # scanf("%d", number);
    syscall

    move $t0, $v0 
    li $t1, 1   # i = 1
    li $t4, 7
    li $t5, 11
loop:
    
    beq $t1, $t0, end # if i = number, exit loop

    move $t6, $t1

    div $t6, $t4
    mfhi $t3
    beq $t3, 0, print # if i%7 = 0, print

    div $t6, $t5
    mfhi $t3
    beq $t3, 0, print # if i%11 = 0, print

    add $t1, $t1, 1
    j loop

print:
    move $a0, $t1          #   printf("%d", i);
    li   $v0, 1
    syscall

    li   $a0, '\n'      # printf("%c", '\n');
    li   $v0, 11
    syscall

    
    add $t1, $t1, 1
    j loop

end:
    jr   $ra           # return

    .data
prompt:
    .asciiz "Enter a number: "
