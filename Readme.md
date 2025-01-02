# Advent of Code 2024

My solutions to Advent of Code problems.

Link: <https://adventofcode.com/2024>


## Python

To run, go to the folder for the corresponding day,
go to the `Python/` subfolder,
modify `input` to match your input provided on the
Advent of Code site (or modify `solution.py` to use
the example input), and run it like so:

```
python3 solution.py
```

If alternative instructions are required, they will be
covered in a Readme in that day's folder.


## Bash

To run, go to the folder for the corresponding day,
go to the `Bash/` subfolder,
modify the `input` to match your input, and run
the solution like so:

```
./solution.sh
```

If alternative instructions are required, they will be
covered in a Readme in that day's folder.

## Awk

To run, go to the folder for the corresponding day,
go to the `Awk/` subfolder,
modify the `input` to match your input, and use `cat`
to pass the file to awk via stdin:

```
cat example | ./solution.awk
```

If any input variables are required (for example, to
run part 1 or part 2 separately), pass them using the
`-v <var_name>=<var_value>` syntax:

```
cat example | ./solution.awk -v part=1
cat example | ./solution.awk -v part=2
```

## Rust

To run, go to the folder for the corresponding day,
go to the `Rust/` subfolder,
modify the `input` to match your input, and run the
Rust program in `src/main.rs` by using the `cargo run`
command:

```
# Run the debug version with no optimization
cargo run

# Run the optimized version
cargo run --release
```

## Java

To run, go to the folder for the corresponding day,
go to the `Java/` subfolder,
modify the `input` to match your input, and compile
and run the Java program in `Solution.java` with
these two steps:

```
javac Solution.java && java Solution
```
