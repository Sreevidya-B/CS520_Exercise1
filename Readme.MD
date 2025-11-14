# COMPSCI 520 - Theory and Practice of Software Engineering - Fall 2025: In-Class Exercises


## 📌 Repository Overview

This repository contains the complete implementation and results for CS520 Exercise 1 and Exercise 2, evaluating GPT-4o and Claude 3.5 Sonnet on code generation and automated testing tasks.

## 📋 Table of Contents
- [Exercise 1: Code Generation](#exercise-1-code-generation)
- [Exercise 2: Automated Testing & Coverage](#exercise-2-automated-testing--coverage)
- [How to Re-run Experiments](#how-to-re-run-experiments)

---

## 🎯 Exercise 1: Prompting, Debugging and Innovation for Code Generation with LLMs

This exercise evaluates two LLMs (GPT-4o and Claude 3.5 Sonnet) on 10 HumanEval benchmark problems using:
- **Part 1:** Three prompting strategies (Chain-of-Thought, Self-Planning, Self-Debugging)
- **Part 2:** Refined prompts based on failure analysis
- **Part 3:** Novel iterative test-driven agent with real feedback loop

---

## 🧪 Exercise 2: Automated Testing & Coverage

Using the programs from Exercise 1, this exercise focuses on:
- **Part 1 (30%):** Baseline coverage measurement for all solutions
- **Part 2 (50%):** LLM-assisted test generation to improve coverage (focus on 2 problems)
- **Part 3 (20%):** Fault detection through bug injection and verification

**Tools:** pytest, pytest-cov, coverage.py

---

## 🏃 How to Re-run Experiments

### Setup

**1. Configure API keys**
```bash
cp .env.example .env
# Edit .env and add your API keys:
OPENAI_API_KEY="your-openai-key-here"
ANTHROPIC_API_KEY="your-anthropic-key-here"
```

#### Exercise 1: Complete Pipeline

Run all scripts in sequence to reproduce the entire experiment:

```bash
# Part 1: Initial Evaluation
python 1_select_problems.py
python 2_generate_prompts.py
python 3_llm_code_generation.py
python 4_evaluate.py

# Part 2: Debugging & Refinement
python 5_analyze_failures.py
python 6_create_refined_prompts.py
python 3_llm_code_generation.py  # Re-run with refined prompts
python 4_evaluate.py  # Re-evaluate
python 7_compare_results.py

# Part 3: Novel Strategy
python 8_novel_strategy.py
python 9_analyze_novel_strategy.py
```

#### Exercise 2: Testing & Coverage Pipeline

```bash
# Part 1: Baseline Coverage
python exercise2/part1_baseline_coverage.py

# Part 2: LLM-Assisted Test Generation
python exercise2/part2_llm_test_improvement.py

# Part 3: Fault Detection
python exercise2/part3_fault_detection.py
```
---

