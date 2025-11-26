# Exercise 3: Specification-Guided Test Improvement

---

## Part 1: Generate, Evaluate and Refine Specifications - Specification Accuracy

### Summary

| Problem | Model  | Correct | Total | Accuracy |
|---------|--------|---------|-------|----------|
|    10   | claude |    4    |   5   |   80.0%  |
|    10   | gpt4o  |    3    |   5   |   60.0%  |
|    20   | claude |    4    |   5   |   80.0%  |
|    20   | gpt4o  |    4    |   5   |   80.0%  |
| **Overall** |        | ** 15 ** | **20** | **  75.0%** |

---

## Part 2: Use Specifications to Guide Test Improvement - Coverage Comparison

### Statement and Branch Coverage

| Problem | Model | Baseline Stmt | Improved Stmt | Change | Baseline Branch | Improved Branch | Change  |
|---------|-------|---------------|---------------|--------|-----------------|-----------------|---------|
|   10    |  claude |       88.89% |       86.67% | -2.22% |          83.33% |          83.33% |  +0.00% |
|   10    |  gpt4o  |       88.89% |       88.89% | +0.00% |          83.33% |          83.33% |  +0.00% |
|   20    |  claude |       90.48% |       100.00% | +9.52% |          83.33% |          100.00% | +16.67% |
|   20    |  gpt4o  |       90.48% |       90.48% | +0.00% |          83.33% |          83.33% |  +0.00% |