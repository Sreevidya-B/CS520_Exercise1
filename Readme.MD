# CS520 Exercise 1: Prompting, Debugging and Innovation for Code Generation with LLMs

This repository contains the complete implementation and results for CS520 Exercise 1, evaluating GPT-4o and Claude 3.5 Sonnet on code generation tasks using different prompting strategies.

## 📋 Table of Contents
- [Overview](#overview)
- [How to Re-run Experiments](#how-to-re-run-experiments)

---

## 🎯 Overview

This project evaluates two LLMs (GPT-4o and Claude 3.5 Sonnet) on 10 HumanEval benchmark problems using:
- **Part 1:** Three prompting strategies (Chain-of-Thought, Self-Planning, Self-Debugging)
- **Part 2:** Refined prompts based on failure analysis
- **Part 3:** Novel iterative test-driven agent with real feedback loop

---

---

## 🏃 How to Re-run Experiments

### Complete Pipeline (All Parts)

**Configure API keys**
```bash
cp  .env
# Edit .env and add your API keys:
OPENAI_API_KEY="your-openai-key-here"
ANTHROPIC_API_KEY="your-anthropic-key-here"
```

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

---
