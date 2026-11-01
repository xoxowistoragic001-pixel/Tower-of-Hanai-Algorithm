# Tower-of-Hanai-Algorithm
The Tower of Hanoi is a mathematical puzzle that consists of three rods and a number of disks of different sizes, which can slide onto any rod. The puzzle starts with the disks in a neat stack in ascending order of size on one rod, the smallest at the top, thus making a conical shape.
Tower of Hanoi algorithm:

Move n−1 disks from source to auxiliary

Move disk n from source to destination

Move n−1 disks from auxiliary to destination

Key Properties
Minimum number of moves: 2ⁿ − 1. Moving 1 disk takes 1 move, 2 disks take 3, 3 disks take 7, 4 disks take 15, and so on — each additional disk roughly doubles the work.

Time complexity: O(2ⁿ), which grows exponentially. For 64 disks (the legendary version), it would take about 18.4 quintillion moves — far longer than the age of the universe at one move per second.

Space complexity: O(n) due to the recursion depth.
