# aoc-2021
Advent of Code 2021

## Log

### Day 1

I've done two straight-forward implementations in Python. For **part 2** I improved the straightforward version caching previous value to avoid doing the sums twice. 

### Day 2 

First version of today's problem. Since it's only 3 commands to handle I didn't bother of implementing a better "switch". 

### Day 3 

First version using strings. My solution can be changed to operate with bits but since it ran pretty fast anyways didn't feel the need for it. For **part 1** I relied on just flipping the bits to get gamma, but for **part 2** I added a parameter to use the same logic with both versions. I'd like to clean it a bit later, since I got a bit stuck an off-by-one edge cases.

After finishing Day 4 I added some unit tests and did the implemented the version using bits and masks.

### Day 4 

I had a bit of time today to play around with the solution. My first solution was working well enough for the input, but playing around with `cProfile` I noticed that most of the calls were on the `bingo_check` function. I optimized to only check changed bingos and god rid of half of the calls. Then I stumbled with another good optimization. I can only check the row and column that were marked. 

### Day 5

For todays solution I opted for implementing a `Point` class since it was much easier to write a line renderer with a bit of vector math. My renderer implementation worked without a change for part 2. I used a bit of time playing around with functional library. 

### Day 6 

After implementing the straightforward solution for the first part, I tried inmediatelly trying to get the second solution using that implementation. In my computer the program started advancing slower around day 180 (where theres is about 35 million fishes). Then I figured there would be a smarter way of simulating the fishes and I think I found the intended way to do it. 

### Day 7

After finishing it and playing with the input data, I got the impression that the brute force solution would have worked also (took around 20secs to compute the costs for all positions for part 2), but anyway I implemented a simple binary search which needs much less calls to the `fuel_cost` function. 

### Day 8

Today's was quite fun. First part was pretty straight-forward. Figuring the proper bitwise operations to use was a bit tricky. I was banging my head against them until I figured out my issues: I had an off by one error with the first `mask` function that gave masks shifted 1 bit to the left and, after solving that I realized that I had sketched 9 as `abdef` so my approach wasn't working as I thought. But today's was a great one to practice my bit manipulation skills. 

Just for fun, I tried implementing a straight-forward brute force solution. Manages to solve puzzle for my input in less than 1 second.

### Day 9

I struggled a bit with Part 2. My initial implementation was not reaching all non-9 points in the grid since I was strictly looking for increases of 1. I made the code to handle the case of a higher slope and I got the right answer.

### Day 10

Today was easier than yesterday for me. I spent a bit of time cleaning up generating the `closing_map` using a dictionary comprehension but nothing else special on the solution for today. 

### Day 11

I spent a bit longer today making a `Grid` class since it seems that many problems need some sort of grid of rows and columns. Understanding the flash logic was a bit tricky but luckily the problem provides good example cases so I could test and find the issues simulating only the first couple of steps. After Step 2 was correct the rest of the problem was easy. 

### Day 12

Forgot to comment on the log yesterday. Main issue I had was understanding the condition for part 2. My current solution takes ~20 secs in the old laptop so I want to test some optimizations after doing day 13 today. 

### Day 13

I stumbled on a good approach today. Instead of using a grid I just use a `set` to store the dots and just apply a function to transform the dots to the folded positions. 

### Day 14

Today it was one of those days when the straight forward version solution doesn't scale properly. I got the version counting pairs working relatively fast, but then it didn't gave me a correct answer with my input although looking correct. After a lot of debugging I realized that the issue was on initializing the pairs for the input (I didn't account for repeated pairs on the original polymer). 

### Day 15

Today's problem seemed like an obvious application of the A* algorithm. My first implementation needed a bit less than 2 minutes for **part 2** so there was some optimization still missing. I added a *closed set* to not process a node multiple times and also i switched the *open set* to a `PriorityQueue` because I realized that most of the time of getting the best node from the set.

### Day 16

Todays main difficulty was understanding the format of the packets, but after figuring that out the rest was pretty easy. I made my own `BITStream` and implemented it with a string of 0s and 1s using `StringIO` for simplicity, but then switched the implementation to read the input bits directly.

### Day 17

Didn't have much time today so I implemented a simple bruteforce solution. I got the puzzle solution by just letting the brute force solution to run for about 10 seconds. Afterwards, I did a bit of thinking to try to do some pruning to speedup the program. I got it to 0,3 seconds by just using the easiest possible ranges. 

### Day 18

I'd like to optimize today's solution further. I implemented it using a tree, but doing all permutations of the 100 numbers takes about half a minute. Optimizing the data structure to get the leaf inmediately to the left and to the right would get me a decent speedup.

### Day 19

That was the hardest day so far. I added a `Point` to my utils since it was much easier to code it by being able to do vector math. I had quite a lot of stumbles figuring out the rotations initially, my current implementation isn't perfect but at least it's "complete". I want to polish my solution figuring out, at least, the proper space. 

After finishing the event I cleaned up the orientations to use rotations around x, y and z axis. Now I'm only exploring the 24 orientations not the mirrored ones. Also while cleaning the code I learned about the `all` and `any` functions.

### Day 20 

Today I got bitten by having my utility grid class. In the end it was much easier to rework the problem with a set of points than trying to handle the bounds cleanly. 

### Day 21

For today I had to learn how to apply the `functools.cache` using object parameters (I needed to implement `__hash__` and `__eq__`). I had implemented the game using a class and I didn't want to rewrite it just to use memoization. For further optimization I implemented a custom `__copy__` function to avoid using the more expensive `copy.deepcopy`.

### Day 22

Part 1 was really easy today, since the *simulation* approach was enough to get the result. For part 2 I had to fully rework my approach. First I thought on splitting the Cuboids, but it seemed quite complex and it wasn't until I had drew a 2D version using rectangles that I visualized how to implement the *substract* method using recursive *cuboids*.

### Day 23

Managed to get the *part 1* answer using the A* implementation but my approach doesn't seem to work for part 2. 

After cleaning up the implementation I spotted some wrong assumptions I made and got the correct answer for both.  

### Day 24

Did some analysis of the bits of the input but that didn't go anywhere.

My second attempt was trying to convert the code to Python, while analyzing and understanding the code I stumbled on the good approach trying to solve the pairs of blocks.

### Day 25

Nothing fancy today, just a simple implementation of the problem to get the star and keep working on the previous days. 