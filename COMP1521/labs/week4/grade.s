# read a mark and print the corresponding UNSW grade

main:
    la $a0, prompt      # printf("Enter a mark: ");
    li $v0, 4
    syscall

    li $v0, 5           # scanf("%d", mark);
    syscall

    bge $v0, 85, high_distinction
    bge $v0, 75, distinction
    bge $v0, 65, credit
    bge $v0, 50, pass
    la $a0, fl
    j print
high_distinction:
    la $a0, hd
    j print
distinction:
    la $a0, dn
    j print
credit:
    la $a0, cr
    j print
pass:
    la $a0, ps
    j print
print:         # printf("FL\n");
    li $v0, 4
    syscall


    jr $ra              # return

    .data
prompt:
    .asciiz "Enter a mark: "
fl:
    .asciiz "FL\n"
ps:
    .asciiz "PS\n"
cr:
    .asciiz "CR\n"
dn:
    .asciiz "DN\n"
hd:
    .asciiz "HD\n"
