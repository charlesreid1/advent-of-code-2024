from collections import Counter, deque

# Example input file
with open("example", "r") as f:
    line = f.read()
line = line.strip()

# Real input file from AoC website
with open("input", "r") as f:
    line = f.read()
line = line.strip()


"""
Part 1:
You are given an input that is a dense format representing
files on disk. Digits alternate between indicating length
of file, and length of free space after that file.

12345 = 1-block file, then 2 free spaces, then 3-block file, &c.

Using one character for each block, where digits are file ID
and . is free space, this disk map represents these blocks:

0..111....22222

Now move file blocks one at a time from the right-most filled block
to the left-most empty block, until there are no more gaps between
the file blocks:

022111222......

Finally, calculate the checksum by multiplying each block's
fileid value by its position number:

top    0 2 2 1 1 1 2 2 2......
* bot: 0 1 2 3 4 5 6 7 8......

which yields 0*0 + 2*1 + 2*2 + 1*3 + 1*4 = checksum
"""

# Approach:
# - expand compact representation into block representation
# - populate deque with block representation
# - pop front while we don't see a '.', tack it on to a list
# - if we do see a '.', pop '.' & throw away, pop back and tack it on to list
# - stop if deque is empty
# - that gives us the compacted block representation
# - can easily calculate checksum from there


def compact_to_block(compact_repr: str):
    """
    Return block representation, but not as a string:
    as a list of elements, either fileid integers, or None for empty space
    """
    block = []
    fileid = 0
    for i, c in enumerate(compact_repr):
        n = int(compact_repr[i])
        if i % 2 == 0:
            # File
            block += [fileid,] * n
            fileid += 1
        else:
            # Free space
            block += [None,] * n
    return block


def block_to_str(block: list):
    """
    Return block representation as a string
    (necessary once you get more than 9 files)
    """
    s = []
    for i, b in enumerate(block):
        if b is None:
            s.append(".")
        else:
            if b > 9:
                s.append(f"({b})")
            else:
                s.append(str(b))
    return "".join(s)


def defrag(blocks: list):
    """
    0..111....22222
    02.111....2222.
    022111....222..
    0221112...22...
    02211122..2....
    022111222......
    """
    defragged = []
    d = deque(blocks)
    while len(d) > 0:
        front = d.popleft()
        if front != None:
            defragged.append(front)
        else:
            # I don't like all these if statements...
            # There ought to be a cleaner way to do this
            if len(d) > 0:
                back = d.pop()
                if back == None:
                    # Keep popping until we get a non-null
                    while back == None and len(d) > 0:
                        back = d.pop()
                if back != None:
                    defragged.append(back)
    empty_space = [
        None,
    ] * (len(blocks) - len(defragged))
    return defragged + empty_space


def checksum(defragged: list):
    checksum = 0
    for i, c in enumerate(defragged):
        if c != None:
            checksum += c * i
    return checksum


def test1():
    # This should print
    # 0..111....22222
    print(block_to_str(compact_to_block("12345")))

    # This should print
    # 022111222......
    print(block_to_str(defrag(compact_to_block("12345"))))

    # This should print
    # 1928
    print(checksum(defrag(compact_to_block("2333133121414131402"))))


def part1():
    print(checksum(defrag(compact_to_block(line))))


"""
Part 2:
Rewrite the defragment method so that it does not 
split them up when back-filling empty space.

    00...111...2...333.44.5555.6666.777.888899
    0099.111...2...333.44.5555.6666.777.8888..
    0099.1117772...333.44.5555.6666.....8888..
    0099.111777244.333....5555.6666.....8888..
    00992111777.44.333....5555.6666.....8888..

Attempt to move each file exactly once in order of decreasing file id,
start with the furthest file to the right (highest ID).

If there is no span of free space to the left of a file 
that is large enough to fit the file, the file does not move.
"""

# Approach:
# - use a nested loop:
# - first loop: over file IDs R2L (sizes: 2, 4, 3, 4, ...)
#   - second loop: over available spaces [reassemble each time]
#     looking for left-most (L2R) available open space


def block_to_streak(blocks: list):
    """
    Return streak representation as a list of tuples,
    with the element first, number of times it appears second:

    Block:  [0, 0, None, None, None, 1, 1, 1, ... ]
    Streak: [(0, 2), (None, 3), (1, 3), ... ]
    """
    streaks = []
    for i, b in enumerate(blocks):
        if i == 0:
            # Initialization
            current_item = b
            current_count = 1
        elif b == current_item:
            # Keep accumulating
            current_count += 1
        elif b != current_item:
            # Stash this streak and start a new one
            streaks.append((current_item, current_count))
            current_item = b
            current_count = 1

        if i == len(blocks) - 1:
            streaks.append((current_item, current_count))
    return streaks


def streak_to_block(streaks: list):
    blocks = []
    for i, (streakelem, streaklen) in enumerate(streaks):
        blocks += [
            streakelem,
        ] * streaklen
    return blocks


def defrag_smarter(blocks: list):
    """
    00...111...2...333.44.5555.6666.777.888899
    0099.111...2...333.44.5555.6666.777.8888..
    0099.1117772...333.44.5555.6666.....8888..
    0099.111777244.333....5555.6666.....8888..
    00992111777.44.333....5555.6666.....8888..
    """
    streaks = block_to_streak(blocks)
    allids = [j for j in streaks[::-1] if j[0] is not None]

    new_streaks = streaks[:]
    for fileid, filesize in allids:
        # Start looking for an open space of size filesize or more
        for j, s in enumerate(new_streaks):
            if s[0] == None and s[1] >= filesize:
                beginning = new_streaks[:j]

                middle = [(fileid, filesize)]
                if s[1] - filesize > 0:
                    middle += [(None, s[1] - filesize)]

                # We inserted new blocks, have to get rid of old blocks
                end = [
                    z if z[0] != fileid else (None, z[1]) for z in new_streaks[j + 1 :]
                ]

                new_streaks = beginning + middle + end
                break

            if s[0] == fileid:
                # This is here because, at some point,
                # we could end up trying to insert a file
                # at a space past its current position.
                # This conditional short-circuits that.
                break

    return streak_to_block(new_streaks)


def test2():
    # # Verify these are consistent
    # print(compact_to_block("2333133121414131402"))
    # print(block_to_streak(compact_to_block("2333133121414131402")))

    # These should both print the same thing:
    # 00...111...2...333.44.5555.6666.777.888899
    print(block_to_str(compact_to_block("2333133121414131402")))
    print(
        block_to_str(
            streak_to_block(block_to_streak(compact_to_block("2333133121414131402")))
        )
    )

    # This should return:
    # 00992111777.44.333....5555.6666.....8888..
    print(block_to_str(defrag_smarter(compact_to_block("2333133121414131402"))))


def part2():
    print(checksum(defrag_smarter(compact_to_block(line))))


part2()
