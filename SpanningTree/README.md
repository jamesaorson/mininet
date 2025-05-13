# Example

## First attempt

```plaintext
SimpleLoopTopo is incorrect (+0)
Expected: 1 - 2, 1 - 3 2 - 1, 2 - 4 3 - 1 4 - 2
Student: 1 - 2, 1 - 3 2 - 4
```

```plaintext
NoLoopTopo is incorrect (+0)
Expected: 1 - 2, 1 - 5 2 - 1, 2 - 3 3 - 2, 3 - 4, 3 - 7 4 - 3 5 - 1, 5 - 9 6 - 7, 6 - 10 7 - 3, 7 - 6, 7 - 8 8 - 7, 8 - 12 9 - 5 10 - 6, 10 - 13 12 - 8 13 - 10
Student: 1 - 2, 1 - 5 2 - 3 3 - 4, 3 - 7 5 - 9 6 - 10 7 - 6, 7 - 8 8 - 12 10 - 13
```

```plaintext
ComplexLoopTopo is incorrect (+0)
Expected: 1 - 2, 1 - 5 2 - 1, 2 - 6 4 - 8 5 - 1, 5 - 9 6 - 2, 6 - 10 8 - 4, 8 - 12 9 - 5 10 - 6, 10 - 11, 10 - 13 11 - 10, 11 - 12 12 - 8, 12 - 11 13 - 10
Student: 1 - 2, 1 - 5 2 - 6 5 - 9 6 - 10 8 - 4 10 - 11, 10 - 13 11 - 12 12 - 8
```

## Second attempt

Switch.py submitted (+10)
SimpleLoopTopo is correct (+10)
NoLoopTopo is correct (+10)
ComplexLoopTopo is incorrect (+0)
Expected: 1 - 2, 1 - 5 2 - 1, 2 - 6 4 - 8 5 - 1, 5 - 9 6 - 2, 6 - 10 8 - 4, 8 - 12 9 - 5 10 - 6, 10 - 11, 10 - 13 11 - 10, 11 - 12 12 - 8, 12 - 11 13 - 10
Student: 1 - 2, 1 - 5 2 - 1, 2 - 3, 2 - 6 3 - 2, 3 - 4, 3 - 7 4 - 3, 4 - 8 5 - 1, 5 - 9 6 - 2, 6 - 10 7 - 3, 7 - 11 8 - 4, 8 - 12 9 - 5 10 - 6, 10 - 13 11 - 7 12 - 8 13 - 10

EvalTopo1 is correct (+15)
EvalTopo2 is correct (+15)
EvalTopo3 is correct (+15)
EvalTopo4 is incorrect (+0)
Hidden topology: No feedback provided

## Third attempt

Switch.py submitted (+10)
SimpleLoopTopo is correct (+10)
NoLoopTopo is correct (+10)
ComplexLoopTopo is incorrect (+0)
Expected: 1 - 2, 1 - 5 2 - 1, 2 - 6 4 - 8 5 - 1, 5 - 9 6 - 2, 6 - 10 8 - 4, 8 - 12 9 - 5 10 - 6, 10 - 11, 10 - 13 11 - 10, 11 - 12 12 - 8, 12 - 11 13 - 10
Student: 1 - 2, 1 - 5 2 - 1, 2 - 3, 2 - 6 3 - 2, 3 - 4, 3 - 7 4 - 3, 4 - 8 5 - 1, 5 - 9 6 - 2, 6 - 10 7 - 3, 7 - 11 8 - 4, 8 - 12 9 - 5 10 - 6, 10 - 13 11 - 7 12 - 8 13 - 10

EvalTopo1 is correct (+15)
EvalTopo2 is correct (+15)
EvalTopo3 is correct (+15)
EvalTopo4 is correct (+15)
