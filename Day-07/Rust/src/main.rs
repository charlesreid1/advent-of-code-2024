use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;

// Read a file into a vector of strings
fn read_lines(filename: &str) -> io::Result<Vec<String>> {
    let file = File::open(filename)?;
    io::BufReader::new(file).lines().collect()
}

// Recursive function that attempts to try every possible operator
fn find_valid_operators(
    target_value: i64,
    sum_nums: &Vec<i64>,
    operator_list: Vec<&str>,
    part2: bool
) -> bool {
    if operator_list.len() == sum_nums.len() - 1 {
        // Base case, picked all operators, now check if they yield target value
        let mut accumulator = sum_nums[0];
        
        for (i, &op) in operator_list.iter().enumerate() {
            match op {
                "*" => accumulator *= sum_nums[i + 1],
                "+" => accumulator += sum_nums[i + 1],
                "||" if part2 => {
                    let concat = format!("{}{}", accumulator, sum_nums[i + 1]);
                    accumulator = concat.parse().unwrap();
                }
                _ => panic!("Unknown operator {}", op)
            }
        }
        
        accumulator == target_value
    } else {
        // Recursive case
        let mut operators = vec!["+", "*"];
        if part2 {
            operators.push("||");
        }

        // Push the new operator onto the operator list and make recursive call
        operators.iter().any(|&op| {
            let mut new_list = operator_list.clone();
            new_list.push(op);
            find_valid_operators(target_value, sum_nums, new_list, part2)
        })
    }
}

fn main() -> io::Result<()> {
    // Read input file
    let lines = read_lines("input")?;
    
    // Parse input into map (Note: could use i64 instead of String for key)
    let mut test_map: HashMap<String, Vec<i64>> = HashMap::new();
    
    for line in lines {
        if line.is_empty() {
            continue;
        }
        
        let parts: Vec<&str> = line.split(':').collect();
        let test_value = parts[0].trim().to_string();
        let right_values: Vec<i64> = parts[1]
            .trim()
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
            
        test_map.insert(test_value, right_values);
    }
    
    // Part 1
    let mut accumulator = 0;
    for (k, right_values) in &test_map {
        let test_value: i64 = k.parse().unwrap();
        if find_valid_operators(test_value, right_values, vec![], false) {
            accumulator += test_value;
        }
    }
    println!("Part 1: accumulated value: {}", accumulator);
    
    // Part 2
    let mut accumulator2 = 0;
    for (k, right_values) in &test_map {
        let test_value: i64 = k.parse().unwrap();
        if find_valid_operators(test_value, right_values, vec![], true) {
            accumulator2 += test_value;
        }
    }
    println!("Part 2: accumulated value: {}", accumulator2);
    
    Ok(())
}
