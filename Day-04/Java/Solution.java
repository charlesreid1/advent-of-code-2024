import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

public class Solution {
    private static final String MAGIC_WORD_PART1 = "XMAS";
    private static final String MAGIC_WORD_PART2 = "MAS";
    private final char[][] grid;
    private final int rows;
    private final int cols;

    ////////////////////////////////////////
    // Driver

    public static void main(String[] args) {
        try {
            // // Should return 18 occurrences of XMAS
            // Solution s = new Solution("example");

            // // Should return 9 occurrences of X-MAS
            // Solution s = new Solution("example2");

            // Real deal
            Solution s = new Solution("input");

            int p1 = s.solvePart1();
            System.out.println("Part 1: number of XMAS strings found: " + p1);

            int p2 = s.solvePart2();
            System.out.println("Part 2: number of X-MAS occurrences: " + p2);

        } catch (IOException e) {
            System.err.println("Error reading input file: " + e.getMessage());
        }
    }

    ////////////////////////////////////////
    // Solution class and logic

    public Solution(String filename) throws IOException {

        // Read all lines into ArrayList
        List<String> lines = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                lines.add(line);
            }
        }

        // Convert to 2D grid of integers
        this.rows = lines.size();
        this.cols = lines.get(0).length();
        this.grid = new char[this.rows][this.cols];

        for (int i = 0; i < this.rows; i++) {
            String line = lines.get(i).toUpperCase();
            for (int j = 0; j < this.cols; j++) {
                this.grid[i][j] = line.charAt(j);
            }
        }
    }

    /*
     * Part 1:
     * Call the generateAllWords() method to generate all words
     * using a moving stencil, and put them in a counter map.
     * This will yield the number of occurrences of the magic word
     * in all of the different orientations requested.
     */
    public int solvePart1() {
        List<String> words = generateAllWords();
        return (int) words.stream()
                         .filter(word -> word.equals(MAGIC_WORD_PART1))
                         .count();
    }

    /*
     * Part 2:
     * Change the search methodology to look for two MAS occurrences
     * in an X shape. Use the same approach of a moving stencil,
     * but this time check for a center A, then check for the
     * telltale signs of an X-MAS pattern.
     */
    public int solvePart2() {
        int xCount = 0;
        int wordLength = MAGIC_WORD_PART2.length();

        for (int i = 0; i <= rows - wordLength; i++) {
            for (int j = 0; j <= cols - wordLength; j++) {
                if (grid[i + 1][j + 1] == MAGIC_WORD_PART2.charAt(1)) {  // Center 'A'
                    // Check both X patterns
                    if (isValidXPattern(i, j)) {
                        xCount++;
                    }
                }
            }
        }
        return xCount;
    }

    /*
     * Utility method for Part 1: 
     * Generate all possible words in all possible directions:
     * going forward/backward, up/down, forward/reverse,
     * diagonal up-left/down-right, diagonal up-right/down-left.
     */
    private List<String> generateAllWords() {
        List<String> words = new ArrayList<>();
        int wordLength = MAGIC_WORD_PART1.length();

        // Diagonal up-left/down-right
        for (int i = 0; i <= rows - wordLength; i++) {
            for (int j = 0; j <= cols - wordLength; j++) {
                StringBuilder forward = new StringBuilder();
                StringBuilder backward = new StringBuilder();
                for (int c = 0; c < wordLength; c++) {
                    forward.append(grid[i + c][j + c]);
                }
                backward.append(forward.reverse());
                words.add(forward.toString());
                words.add(backward.toString());
            }
        }

        // Diagonal up-right/down-left
        for (int i = wordLength - 1; i < rows; i++) {
            for (int j = 0; j <= cols - wordLength; j++) {
                StringBuilder forward = new StringBuilder();
                StringBuilder backward = new StringBuilder();
                for (int c = 0; c < wordLength; c++) {
                    forward.append(grid[i - c][j + c]);
                }
                backward.append(forward.reverse());
                words.add(forward.toString());
                words.add(backward.toString());
            }
        }

        // Vertical
        for (int i = 0; i <= rows - wordLength; i++) {
            for (int j = 0; j < cols; j++) {
                StringBuilder forward = new StringBuilder();
                StringBuilder backward = new StringBuilder();
                for (int c = 0; c < wordLength; c++) {
                    forward.append(grid[i + c][j]);
                }
                backward.append(forward.reverse());
                words.add(forward.toString());
                words.add(backward.toString());
            }
        }

        // Horizontal
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j <= cols - wordLength; j++) {
                StringBuilder forward = new StringBuilder();
                StringBuilder backward = new StringBuilder();
                for (int c = 0; c < wordLength; c++) {
                    forward.append(grid[i][j + c]);
                }
                backward.append(forward.reverse());
                words.add(forward.toString());
                words.add(backward.toString());
            }
        }

        return words;
    }

    /*
     * Utility method for Part 2: 
     * Check if the given location has a valid
     * X-MAS pattern (MAS going either direction
     * on the diagonals).
     */
    private boolean isValidXPattern(int i, int j) {
        char m = MAGIC_WORD_PART2.charAt(0);  // M
        char s = MAGIC_WORD_PART2.charAt(2);  // S

        // Check first diagonal (top-left to bottom-right)
        boolean pattern1 = (grid[i][j] == m && grid[i + 2][j + 2] == s) ||
                          (grid[i][j] == s && grid[i + 2][j + 2] == m);

        // Check second diagonal (top-right to bottom-left)
        boolean pattern2 = (grid[i][j + 2] == m && grid[i + 2][j] == s) ||
                          (grid[i][j + 2] == s && grid[i + 2][j] == m);

        return pattern1 && pattern2;
    }

}
