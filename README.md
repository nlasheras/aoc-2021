# aoc-2021
Advent of Code 2021

## Log

### Day 1

I've done two straight-forward implementations in Python. For **part 2** I improved the straightforward version caching previous value to avoid doing the sums twice. 

### Day 2 

First version of today's problem. Since it's only 3 commands to handle I didn't bother of implementing a better "switch". 

### Day 3 

First version using strings. My solution can be changed to operate with bits but since it ran pretty fast anyways didn't feel the need for it. For **part 1** I relied on just flipping the bits to get gamma, but for **part 2** I added a parameter to use the same logic with both versions. I'd like to clean it a bit later, since I got a bit stuck an off-by-one edge cases.

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
