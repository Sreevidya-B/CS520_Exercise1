# COMPSCI 520 - Theory and Practice of Software Engineering - Fall 2025: In-Class Exercises


## 📌 Repository Overview

This repository contains the complete implementation and results for CS520 Exercise 1, Exercise 2 and Exercise 3, evaluating GPT-4o and Claude 3.5 Sonnet on code generation, automated testing and specification-guided test improvement tasks.

## 📋 Table of Contents
- [Exercise 1: Code Generation](#exercise-1-code-generation)
- [Exercise 2: Automated Testing & Coverage](#exercise-2-automated-testing--coverage)
- [Exercise 3: Specification-Guided Test Improvement](#exercise-3-specification-guided-test-improvement)
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

## 🧾 Exercise 3: Specification-Guided Test Improvement

This exercise generates and refines formal specifications with LLMs, then uses them to guide test generation and coverage analysis for selected problems.

- **Part 1:** Generate and evaluate specifications for target problems.
- **Part 2:** Use specifications to guide test generation and measure coverage improvements.

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

#### Exercise 3: Specification-Guided Test Improvement

This exercise generates and refines formal specifications with LLMs, then uses them to guide test generation and coverage analysis for selected problems.

- **Part 1:** Generate and evaluate specifications for target problems.  
- **Part 2:** Use specifications to guide test generation and measure coverage improvements.

**Tools:** pytest, pytest-cov, coverage.py

**How to run** (from repo root):
```bash
# Navigate to exercise3 directory
cd exercise3

# Step 1: Extract problem information from Exercise 2
python 1_extract_problem_info.py
# Output: problem_descriptions.json

# Step 2: Generate specification prompts
python 2_generate_spec_prompts.py
# Output: prompts/spec_generation_*.txt (4 files)

# Step 3: Manually obtain LLM specification responses
# - Use prompts from step 2 with GPT-4o and Claude 3.5 Sonnet
# - Save raw responses to: specifications/problem*_*_raw.py (4 files)

# Step 4: Evaluate and correct specifications (interactive CLI)
python 3_evaluate_specifications.py
# - Mark each assertion as correct/incorrect
# - Provide corrections and explanations for incorrect ones
# Output: evaluation_results.json + specifications/problem*_*_corrected.py (4 files)

# Step 5: Generate test generation prompts from corrected specs
python 4_generate_test_prompts.py
# - Reads corrected specifications from step 4
# - Creates prompts that include the corrected assertions
# Output: prompts/test_generation_*.txt (4 files)

# Step 6: Manually obtain LLM test generation responses
# - Use prompts from step 5 with GPT-4o and Claude 3.5 Sonnet
# - Save test code to: tests/test_spec_guided_problem*.py (4 files)

# Step 7: Run coverage analysis (baseline vs. spec-guided)
python 5_run_coverage_analysis.py
# - Runs pytest-cov on baseline HumanEval tests
# - Runs pytest-cov on baseline + spec-guided tests
# - Compares statement and branch coverage
# Output: coverage_comparison.json + coverage_reports/ (8 subdirectories)

# Step 8: Generate formatted report data
python 6_generate_report_data.py
# - Compiles data from evaluation_results.json (Part 1)
# - Compiles data from coverage_comparison.json (Part 2)
# - Generates markdown tables
# Output: REPORT_TEMPLATE.md (auto-generated summary tables)

```
---
