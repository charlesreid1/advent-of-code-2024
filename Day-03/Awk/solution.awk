#!/usr/local/bin/gawk -f

function solve(part1) {
    total = 0
    active = 1
    
    # Reset line position and vars for second pass
    NR = 0
    FNR = 0
    
    while ((getline line) > 0) {

        # Check for control operations
		while (match(line, /mul\(([0-9]+),([0-9]+)\)|do\(\)|don't\(\)/, ops)) {
		    if (ops[0] == "don't()") {
		        active = 0
            } else if (ops[0] == "do()") {
		        active = 1
            } else if (active || part1) {
                total += ops[1] * ops[2]
            }
            line = substr(line, RSTART + RLENGTH)
		}
    }
    return total
}

BEGIN {
    if (part==1) {
        # Part 1
        print solve(1)
    } else if (part==2) { 
        # Part 2
        print solve(0)
    } else {
        print "Please provide awk with instructions on which part to run"
        print "by adding -v part=1 or -v part=2 to your invocation"
    }
}
