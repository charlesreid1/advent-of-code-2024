#!/bin/bash

# Example input file
# Should return distance = 11 and similarity = 31
FILE="example"

# # Real input file (provided on advent of code website)
# FILE="input"

# tr -s ' ' will squeeze repeated spaces, so that we can use cut
# LEFT and RIGHT are now space-delimited lists of numbers
LEFT=$( cat ${FILE} | tr -s ' ' | cut -d' ' -f1 | xargs)
RIGHT=$(cat ${FILE} | tr -s ' ' | cut -d' ' -f2 | xargs)


# Part 1: Compute distance between two lists

# Space-delimited string lists
SORTED_LEFTS=$( cat ${FILE} | tr -s ' ' | cut -d' ' -f1 | sort | xargs)
SORTED_RIGHTS=$(cat ${FILE} | tr -s ' ' | cut -d' ' -f2 | sort | xargs)

# Bash arrays
SORTED_LEFT=(${SORTED_LEFTS})
SORTED_RIGHT=(${SORTED_RIGHTS})

# Loop pairwise over the left and right lists
count=${#SORTED_LEFT[@]}
total=0
for i in `seq 1 $count`
do
	# Compute difference using bc
	result=$(echo ${SORTED_LEFT[$i-1]} "-" ${SORTED_RIGHT[$i-1]} | bc)
	# Accumulate total (the #- syntax uses absolute value)
	total=$(echo ${total} "+" ${result#-} | bc)
done

echo "Part 1: Distance: ${total}"


# Part 2: Compute similarity between two lists

# Space-delimited string lists
ELEMENTS=$(cat ${FILE} | xargs -n1 | sort | uniq | xargs)

# Bash array
SET=(${ELEMENTS})

# Loop pairwise over the left and right lists
count=${#SET[@]}
similarity=0
for i in `seq 1 $count`
do

	# NOTE: At a high level, this is insane.
	# Bash is not meant to do math calculations,
	# the overhead of assembling strings and evaluating them
	# is massive and makes the runtime of this script
	# thousands of times the runtime of the Python script.
	#
	# We mainly wrote this script to prove to ourselves that
	# we can, in fact, accomplish this task in pure bash.

	e=${SET[$i-1]}

	# Use xargs to split string-delmited list to one element per line,
	# then use grep to get the nubmer of lines that match this elem
	left_count=$(echo ${SORTED_LEFTS} | xargs -n1 | grep -c "${e}")
	right_count=$(echo ${SORTED_RIGHTS} | xargs -n1 | grep -c "${e}")

	# Similarity is product of element, left list count, right list count
	s=$(echo ${e} "*" ${left_count} "*" ${right_count} | bc)

	# Accumulate
	similarity=$(echo ${similarity} "+" ${s} | bc)
done

echo "Part 2: Similarity: ${similarity}"

