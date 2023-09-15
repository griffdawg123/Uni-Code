########################################################################
# COMP1521 20T2 --- assignment 1: a cellular automaton renderer
#
# Written by <z5311098>, July 2020.


# Maximum and minimum values for the 3 parameters.

MIN_WORLD_SIZE	=    1
MAX_WORLD_SIZE	=  128
MIN_GENERATIONS	= -256
MAX_GENERATIONS	=  256
MIN_RULE	=    0
MAX_RULE	=  255

# Characters used to print alive/dead cells.

ALIVE_CHAR	= '#'
DEAD_CHAR	= '.'

# Maximum number of bytes needs to store all generations of cells.

MAX_CELLS_BYTES	= (MAX_GENERATIONS + 1) * MAX_WORLD_SIZE

	.data

# `cells' is used to store successive generations.  Each byte will be 1
# if the cell is alive in that generation, and 0 otherwise.

cells:	.space MAX_CELLS_BYTES


# Some strings you'll need to use:

prompt_world_size:	.asciiz "Enter world size: "
error_world_size:	.asciiz "Invalid world size\n"
prompt_rule:		.asciiz "Enter rule: "
error_rule:		.asciiz "Invalid rule\n"
prompt_n_generations:	.asciiz "Enter how many generations: "
error_n_generations:	.asciiz "Invalid number of generations\n"
new_line:	.asciiz "\n"

	.text

	# $s1 --> world size
	# $s2 --> rule
	# $s3 --> n_generations
	# $s4 --> reverse
	# $s5 --> counters
main:
	sub $sp, $sp, 4     # move stack pointer down to make room
    sw $ra, 0($sp)      # save $ra on $stack

	li $s1, 0	# world_size = 0;
	li $s2, 0	# rule = 0;
	li $s3, 0	# n_generations = 0;
	li $s4, 0	# reverse = 0;

	##### INTAKE WORLD SIZE #####
	la $a0, prompt_world_size	# printf("Enter world size: ");
	li $v0, 4
	syscall

	li $v0, 5					# scanf("%d", &world_size);
	syscall
	move $s1, $v0

	blt $s1, MIN_WORLD_SIZE, invalid_world	# if (world_size < MIN_WORLD_SIZE || world_size > MAX_WORLD_SIZE) {
	bgt $s1, MAX_WORLD_SIZE, invalid_world
	#############################

	##### INTAKE RULE #####
	la $a0, prompt_rule	# printf("Enter rule: ");
	li $v0, 4
	syscall

	li $v0, 5			# scanf("%d", &rule);
	syscall
	move $s2, $v0

	blt $s2, MIN_RULE, invalid_rule	# if (rule < MIN_RULE || rule > MAX_RULE) {
	bgt $s2, MAX_RULE, invalid_rule
	#######################

	##### INTAKE GENERATIONS #####
	la $a0, prompt_n_generations	# printf("Enter how many generations: ");
	li $v0, 4
	syscall

	li $v0, 5			# scanf("%d", &n_generations);
	syscall
	move $s3, $v0

	blt $s3, MIN_GENERATIONS, invalid_gen	# if (n_generations < MIN_GENERATIONS || n_generations > MAX_GENERATIONS) {
	bgt $s3, MAX_GENERATIONS, invalid_gen
	j start
	##############################

invalid_world:
	la $a0, error_world_size
	li $v0, 4
	syscall
	j exit

invalid_rule:
	la $a0, error_rule
	li $v0, 4
	syscall
	j exit

invalid_gen:
	la $a0, error_n_generations
	li $v0, 4
	syscall
	j exit

exit:
	li $v0, 0
	jr $ra

start:
	

	la $a0, new_line # "\n"
	li $v0, 4
	syscall

	

	bge $s3, 0, notreverse # if gens > 0, not reverse
	# if reverse
	li $s4, 1 	# reverse = 1
	mul $s3, $s3, -1 # make n_generations +ve
notreverse:	# if gens >= 0
	
	la $t1, cells # load address of start of array
	
	li $t2, 2
	div $t2, $s1, $t2	# add world_size / 2
	add $t1, $t1, $t2
	li $t3, 1 
	
	sb $t3, ($t1) # save 1 at cells[0][world_size/2]
	

	li $s5, 1 #    for (int g = 1; g <= n_generations; g++) {
runloop:
	bgt $s5, $s3, runend
	move $a0, $s1 #     run_generation(world_size, g, rule);
	move $a1, $s5
	move $a2, $s2
	jal run_generation
	
	# 	}
	add $s5, $s5, 1
	j runloop
runend:
	li $s5, 0
	beq $s4, 0, regularloop
	move $s5, $s3

reverseloop:
	blt $s5, 0, loopend

	move $a0, $s1 # world size
	move $a1, $s5 # which generation
	jal print_generation

	sub $s5, $s5, 1
	j reverseloop


regularloop:
	bgt $s5, $s3, loopend

	move $a0, $s1 # world size
	move $a1, $s5 # which generation
	jal print_generation
	
	add $s5, $s5, 1
	j regularloop

loopend:

	lw $ra, 0($sp)      # recover $ra from $stack
    add $sp, $sp, 4     # move stack pointer back up to what it was when main called

	li $v0, 0
	jr $ra

	li	$v0, 10
	syscall

# #################################################

	# $t1 --> x
	# $a0 --> world_size
	# $a1 --> which_generation
	# $a2 --> rule
	# $t2 --> left
	# $t3 --> centre
	# $t4 --> right
	# $t5 --> state
	# $t6 --> bit
	# $t7 --> set
run_generation:
	sub  $sp, $sp, 16   # move stack pointer down to make room
    sw   $ra, 12($sp)    # save $ra on $stack
    sw   $a2, 8($sp)    # save $a2 on $stack
    sw   $a1, 4($sp)    # save $a1 on $stack
	sw   $a0, 0($sp)    # save $a0 on $stack

	li $t1, 0 # x = 0

genloop:
	bge $t1,  $a0, genloopend # while x < world size

	li $t2, 0 # left = 0
	ble $t1, 0 notzero # if x<= 0 goto notzero
	# left
	la $t3, cells # load cells --> $t3
	move $t4, $a1 # a1 --> which_generation --> $t4
	sub $t4, $t4, 1 # whichgenerations - 1
	li $t5, MAX_WORLD_SIZE
	mul $t4, $t4, $t5
	add $t3, $t3, $t4

	move $t4, $t1 # $t4 --> x
	sub $t4, $t4, 1 # x-1
	add $t3, $t3, $t4

	lb $t2, 0($t3)

notzero:

	# centre
	la $t4, cells # load cells --> $t4
	move $t5, $a1 # $a1 --> which_generations --> $t5
	sub $t5, $t5, 1 # which_generations - 1
	li $t6, MAX_WORLD_SIZE
	mul $t5, $t5, $t6 
	add $t4, $t4, $t5

	move $t5, $t1
	add $t4, $t4, $t5

	lb $t3, 0($t4)

	li $t4, 0
	move $t5, $a0
	sub $t5, $t5, 1
	bge $t1, $t5, overflow
	# right
	la $t5, cells
	move $t6, $a1
	sub $t6, $t6, 1
	li $t7, MAX_WORLD_SIZE
	mul $t6, $t6, $t7
	add $t5, $t5, $t6

	move $t6, $t1
	add $t6, $t6, 1
	add $t5, $t5, $t6

	lb $t4, 0($t5)

overflow:
	# $t2 --> left
	# $t3 --> centre
	# $t4 --> right
	sll $t2, $t2, 2
	sll $t3, $t3, 1
	sll $t4, $t4, 0
	or $t5, $t2, $t3
	or $t5, $t5, $t4 # state = left << 2 | centre << 1 | right << 0;

	li $t6, 1 # bit = 1 << state
	sllv $t6, $t6, $t5
	and $t6, $a2, $t6 # set = rule & bit;

	la $t2, cells
	move $t3, $a1 # --> which_generation
	mul $t3, $t3, MAX_WORLD_SIZE
	add $t2, $t2, $t3
	add $t2, $t2, $t1

	bne $t6, 0, notdead

	li $t3 0
	sb $t3, 0($t2)
	add $t1, $t1, 1
	j genloop

notdead:
	li $t3, 1
	sb $t3, 0($t2)
	add $t1, $t1, 1
	j genloop

genloopend:
	
	lw   $ra, 12($sp)    # restore $ra from $stack
    add  $sp, $sp, 16   # move stack pointer back up to what it was when main called

	jr	$ra

	#########################################

	# $a0-->$t0 - world size
	# $a1-->$t1 - which generation
print_generation:

	sub  $sp, $sp, 12   # move stack pointer down to make room
    sw   $ra, 8($sp)    # save $ra on $stack
    sw   $a1, 4($sp)    # save $a1 on $stack
    sw   $a0, 0($sp)    # save $a0 on $stack

	move $t0, $a0
	move $t1, $a1
	
	move $a0, $t1 
	li $v0, 1
	syscall
	li $a0, '\t'
	li $v0, 11
	syscall
	
	li $t2, 0 # x = 0
forloop:
	bge $t2, $t0, forloopend # while x < world_size
	
	la $t3, cells
	move $t4, $t1 # which_generation
	mul $t4, $t4, MAX_WORLD_SIZE
	add $t3, $t3, $t4
	move $t4, $t2 # x
	add $t3, $t3, $t4
	
	lb $t4, ($t3)
	
	bne $t4, 0, alive
	li $a0, DEAD_CHAR
	j ender
alive:
	li $a0, ALIVE_CHAR
ender:
	li $v0, 11
	syscall
	add $t2, $t2, 1
	j forloop
forloopend:
	li $a0, '\n'
	li $v0, 11
	syscall

	lw   $ra, 8($sp)    # restore $ra from $stack
    add  $sp, $sp, 12   # move stack pointer back up to what it was when main called

	jr	$ra

	#######################################




