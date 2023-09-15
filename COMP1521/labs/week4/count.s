# read a number n and print the integers 1..n one per line

main:                           # int main(void)
    la  $a0, prompt             # printf("Enter a number: ");
    li  $v0, 4
    syscall

    li  $v0, 5                  # scanf("%d", number);
    syscall

    move $t1, $v0

    li $t0, 1                   # int i = 0;
loop:
    bgt $t0, $t1 end             # while (i < 10)          # j = i + 1;
    move  $a0, $t0                # printf("%d", $t1);
    li  $v0, 1
    syscall

    li   $a0, '\n'      # printf("%c", '\n');
    li   $v0, 11
    syscall

    add $t0, $t0 1

    b loop

end:
    jr  $ra                     # return

    .data
prompt:
    .asciiz "Enter a number: "
