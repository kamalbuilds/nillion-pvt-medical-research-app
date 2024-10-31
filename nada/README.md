Removed the & operator since it's not supported in NADA
Split the age range check into two separate conditions for clarity
Used nested if_else() calls to implement the logical AND behavior
The logic works like this:
If first_condition (age >= min) is true:
Check second_condition (age <= max)
If true: return one
If false: return zero
If first_condition is false:
Return zero