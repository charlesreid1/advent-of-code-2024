import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.io.File;

/*
 * Advent of Code: Day 10 Solution
 */
public class Solution {

    /*
     * Main driver to run Part 1 and Part 2
     */
    public static void main(String[] args) {
        Solution solution = new Solution();

        try {
            // // This should return 1 trailhead, score of 2
            // String filename = "example";

            // // This should return 1 trailhead, score of 4
            // String filename = "example2";

            // // This should return 2 trailheads, scores of 1 and 2
            // String filename = "example3";

            // // This should return 9 trailheads, score of 36
            // String filename = "example4";

            // This uses the real input from AoC website
            String filename = "input";

            int[][] grid = solution.readInput(filename);

            // Solve part 1
            long result1 = solution.solvePart1(grid);
            System.out.println("Part 1 Solution: " + result1);

        } catch (IOException e) {
            System.err.println("Error reading input file: " + e.getMessage());
        }

    }

    /*
     * Part 1:
     * Given a topological map consisting of a grid of
     * integers (0=trailhead, 1=low, 9=high),
     * determine the score of each trailhead.
     *
     * The score of a trailhead is the number of 9 squares
     * that can be reached from that trailhead, by only
     * following horizontal/vertical step changes of 1.
     */
    private long solvePart1(int[][] grid) {
        // Solution Approach:
        // - get trailhead locations
        // - call recursive method doing breadth-first search
        // - pass along accumulated list of locations in this trail
        // - return the sum of the breadth-first calls
        // - base case is 8, return 1 if 9 there, return 0 otherwise
        // - also need to accumulate a list of grid points in this path

        // To store grid locations, use ArrayList of 2-element int arrays

        // Stash trailhead locations
        ArrayList<int[]> trailheads = new ArrayList<>();
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j]==0) {
                    trailheads.add(new int[]{i, j});
                }
            }
        }
        System.out.println("Found " + trailheads.size() + " trailhead(s)");

        // Accumulate trailhead scores
        long scores = 0;
        for (int i = 0; i < trailheads.size(); i++) {
            ArrayList<int[]> breadcrumbs = new ArrayList<>();
            ArrayList<int[]> nines = new ArrayList<>();
            long score = getTrailheadScore(grid, trailheads.get(i), breadcrumbs, nines);
            // System.out.println("Trailhead at " + trailheads.get(i)[0] + ", " + trailheads.get(i)[1] + " has score " + score);
            scores += score;
        }

        return scores;
    }

    /*
     * Recursive method:
     * For the given trailhead, for the given breadcrumb of points on this trail,
     * call this recursive method for any subsequent trail steps that can be taken,
     * and return the sums of their scores. 
     *
     * The base case is when there are 8 breadcrumb steps, there is either
     * a 9 square available (score = 1) or not (score = 0).
     *
     * Have to keep track of the locations part of this current trail (breadcrumbs),
     * but also have to keep track of the 9 peaks that we have already seen
     * independent of the current trail.
     */
    private long getTrailheadScore(int[][] grid, int[] currentLoc, ArrayList<int[]> breadcrumbs, ArrayList<int[]> nines) {
        // Temporarliy add this location to the breadcrumb trail
        breadcrumbs.add(currentLoc);

        // These will be useful for both base case and recursive case
        int[] n = new int[]{currentLoc[0]-1, currentLoc[1]};
        int[] e = new int[]{currentLoc[0], currentLoc[1]+1};
        int[] s = new int[]{currentLoc[0]+1, currentLoc[1]};
        int[] w = new int[]{currentLoc[0], currentLoc[1]-1};

        // Determine the score for the current location
        long score = 0;
        if (breadcrumbs.size()==10) {
            // Base case
            if (grid[currentLoc[0]][currentLoc[1]]==9) {
                // Check if this nine has already been reached (for some reason, .contains() doesn't work here)
                boolean reached = false;
                for (int i = 0; i < nines.size(); i++) {
                    if (nines.get(i)[0] == currentLoc[0] && nines.get(i)[1] == currentLoc[1]) {
                        reached = true;
                    }
                }
                if (!reached) {
                    // This nine has not been reached before
                    score = 1;
                    nines.add(currentLoc);
                }
            }
        } else {
            // North
            if (n[0]>=0 && n[0]<grid.length && n[1]>=0 && n[1]<grid[0].length) {
                if (grid[n[0]][n[1]]==breadcrumbs.size()) {
                    if (!breadcrumbs.contains(n)) {
                        score += getTrailheadScore(grid, n, breadcrumbs, nines);
                    }
                }
            }
            // East
            if (e[0]>=0 && e[0]<grid.length && e[1]>=0 && e[1]<grid[0].length) {
                if (grid[e[0]][e[1]]==breadcrumbs.size()) {
                    if (!breadcrumbs.contains(e)) {
                        score += getTrailheadScore(grid, e, breadcrumbs, nines);
                    }
                }
            }
            // South
            if (s[0]>=0 && s[0]<grid.length && s[1]>=0 && s[1]<grid[0].length) {
                if (grid[s[0]][s[1]]==breadcrumbs.size()) {
                    if (!breadcrumbs.contains(s)) {
                        score += getTrailheadScore(grid, s, breadcrumbs, nines);
                    }
                }
            }
            // West
            if (w[0]>=0 && w[0]<grid.length && w[1]>=0 && w[1]<grid[0].length) {
                if (grid[e[0]][w[1]]==breadcrumbs.size()) {
                    if (!breadcrumbs.contains(w)) {
                        score += getTrailheadScore(grid, w, breadcrumbs, nines);
                    }
                }
            }
        }
        breadcrumbs.remove(currentLoc);
        return score;
    }

    /*
     * Utility: load data from file
     */
    private int[][] readInput(String filename) throws IOException {
        // Read all lines into ArrayList
        List<String> lines = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                lines.add(line);
            }
        }

        // Convert to 2D grid of integers
        int rows = lines.size();
        int cols = lines.get(0).length();
        int[][] grid = new int[rows][cols];
        for (int i = 0; i < rows; i++) {
            String line = lines.get(i);
            for (int j = 0; j < cols; j++) {
                grid[i][j] = Character.getNumericValue(line.charAt(j));
            }
        }

        return grid;
    }

    /*
     * Utility: print the grid (debugging method)
     */
    private void printGrid(int[][] grid) {
        for (int[] row : grid) {
            for (int val : row) {
                System.out.print(val + " ");
            }
            System.out.println();
        }
    }
}
