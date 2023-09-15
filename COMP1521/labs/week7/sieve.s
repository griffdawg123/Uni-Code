# Sieve of Eratosthenes
# https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
main:

    li $s0, 0 # int i = 0
    loopset:
    bge $s0, 1000, loopsetend

    la $t0, prime
    add $t0, $t0, $s0
    li $t1, 1
    sb $t1 0($t0)

    add $s0, $s0, 1
    j loopset
loopsetend:
    li $s0, 2 # int i = 2

loopouter:
    bge $s0, 1000, loopouterend
    la $t0, prime
    add $t0, $t0, $s0
    lb $t1 0($t0)
    beq $t1, 0 loopinnerend

    move $a0, $s0
    li $v0, 1
    syscall

    li $a0, '\n'
    li $v0, 11
    syscall

    mul $s1, $s0, 2 # int j = 2 * i 
loopinner:
    bge $s1, 1000, loopinnerend
    la $t0, prime
    add $t0, $t0, $s1
    sb $zero 0($t0)
    add $s1, $s1, $s0
    j loopinner
loopinnerend:
    add $s0, $s0, 1
    j loopouter
loopouterend:
    li $v0, 0           # return 0
    jr $31

.data
prime:
    .space 1000