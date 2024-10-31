Removes the unsupported & operator
Uses nested .if_else() calls to implement logical AND
Maintains the same logical behavior where both conditions must be true
The pattern is essentially:
If first condition is true, check second condition
If second condition is true, return 1, else return 0
If first condition is false, return 0
