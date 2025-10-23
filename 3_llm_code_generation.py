#!/usr/bin/env python3
"""
Script 3: Automated Code Generation using OpenAI & Claude APIs
Generates code for all combinations: 10 problems × 2 LLMs × 3 strategies × k solutions
Loads API keys from .env file

According to Exercise 1 requirements, I used:
- 2 LLMs from different families: GPT-4o (OpenAI) and Claude 3.7 Sonnet (Anthropic)
- 3 prompting strategies: CoT, Self-Planning, Self-Debugging
- Generate k solutions per problem for pass@k evaluation
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI
import time

# Load environment variables from .env
load_dotenv()

# Set your API keys from .env
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Verify keys are loaded
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# Initialize clients
openai_client = OpenAI(api_key=openai_api_key)
claude_client = Anthropic(api_key=anthropic_api_key)


def load_prompts(strategy):
    """Load prompts for a given strategy"""
    prompt_file = f"prompts/{strategy}_prompts.json"
    try:
        with open(prompt_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {prompt_file} not found. Generate prompts by running 2_generate_prompts.py first.")
        return {}


def generate_with_gpt4o(prompt, k=1):
    """
    Generate code using GPT-4o via OpenAI API
    
    Args:
        prompt: The prompt to send to GPT-4o
        k: Number of different solutions to generate
    
    Returns:
        List of k generated code strings
    """
    results = []
    
    for i in range(k):
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert Python programmer. Generate clean, efficient and correct code. Return only the Python code without markdown formatting or explanations unless necessary."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7 if k > 1 else 0.0, 
                max_tokens=2048,
                timeout=30
            )
            code = response.choices[0].message.content
            results.append(code)
            
            if i < k - 1:
                time.sleep(0.5)
                
        except Exception as e:
            print(f"\n  Error with GPT-4o (attempt {i+1}/{k}): {e}")
            results.append(f"# Error generating code: {str(e)}")
    
    return results


def generate_with_claude(prompt, k=1):
    """
    Generate code using Claude via Anthropic API
    
    Args:
        prompt: The prompt to send to Claude
        k: Number of different solutions to generate
    
    Returns:
        List of k generated code strings
    """
    results = []
    
    for i in range(k):
        try:
            response = claude_client.messages.create(
                model="claude-3-7-sonnet-20250219",  
                max_tokens=2048,
                temperature=0.7 if k > 1 else 0.0,
                system="You are an expert Python programmer. Generate clean, efficient and correct code. Return only the Python code without markdown formatting or explanations unless necessary.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            code = response.content[0].text
            results.append(code)
            
            if i < k - 1:
                time.sleep(0.5)
                
        except Exception as e:
            print(f"\nError with Claude (attempt {i+1}/{k}): {e}")
            results.append(f"Error generating code: {str(e)}")
    
    return results


def setup_directories():
    """Create output directory structure"""
    models = ['gpt4o', 'claude']
    # strategies = ['cot', 'self_planning', 'self_debugging'] # uncomment this line to run for part-1 only
    strategies = [
        'cot', 'self_planning', 'self_debugging',
        'cot_refined', 'self_planning_refined', 'self_debugging_refined'
    ] # uncomment this line to run for part-2 only
    
    base = Path("generated_code")
    for model in models:
        for strategy in strategies:
            (base / model / strategy).mkdir(parents=True, exist_ok=True)
    
    print("Directory structure created")


def extract_python_code(text):
    """
    Extract Python code from LLM response that might contain markdown formatting
    """
    # Remove markdown code blocks if present
    if "```python" in text:
        start = text.find("```python") + 9
        end = text.find("```", start)
        if end != -1:
            return text[start:end].strip()
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        if end != -1:
            code = text[start:end].strip()
            # Remove language identifier if present
            if code.startswith("python\n"):
                code = code[7:]
            return code
    
    return text.strip()


def run_generation(k=3):
    """
    Run full generation pipeline
    
    Args:
        k: Number of solutions to generate per (problem, model, strategy) combination
    """
    setup_directories()
    
    models = {
        'gpt4o': generate_with_gpt4o,
        'claude': generate_with_claude
    }
    # strategies = ['cot', 'self_planning', 'self_debugging'] # uncomment this line to run for part-1 only
    strategies = [
        'cot', 'self_planning', 'self_debugging',
        'cot_refined', 'self_planning_refined', 'self_debugging_refined'
    ] # uncomment this line to run for part-2 only
    
    total_tasks = 10 * 2 * len(strategies) * k  # 10 problems × 2 models × 6 strategies × k solutions
    completed = 0
    
    print("\n" + "="*70)
    print(f"GENERATING CODE FOR ALL CONFIGURATIONS (k={k})")
    print("="*70)
    print(f"Total experiments: 10 problems × 2 LLMs × {len(strategies)} strategies × {k} solutions = {total_tasks}")
    print("="*70 + "\n")
    
    for strategy in strategies:
        print(f"\n{'='*70}")
        print(f"STRATEGY: {strategy.upper()}")
        print(f"{'='*70}")
        
        prompts = load_prompts(strategy)
        if not prompts:
            print(f"Skipping {strategy} - no prompts found")
            continue
        
        for model_name, gen_func in models.items():
            print(f"\n  Model: {model_name.upper()}")
            print(f"  {'-'*60}")
            
            for task_id, prompt_data in sorted(prompts.items()):
                file_name = task_id.replace('/', '_')
                
                # Check if all k solutions already exist
                all_exist = True
                for i in range(k):
                    save_path = Path(f"generated_code/{model_name}/{strategy}/{file_name}_{i}.py")
                    if not save_path.exists() or save_path.stat().st_size < 50:
                        all_exist = False
                        break
                
                if all_exist:
                    print(f"  ✓ {task_id} (already generated {k} solutions)")
                    completed += k
                    continue
                
                print(f"  Generating {task_id} (k={k})...", end=" ", flush=True)
                
                # Generate k solutions
                codes = gen_func(prompt_data['prompt'], k=k)
                
                if codes:
                    # Save all k solutions
                    for i, code in enumerate(codes):
                        save_path = Path(f"generated_code/{model_name}/{strategy}/{file_name}_{i}.py")
                        save_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Extract clean Python code
                        clean_code = extract_python_code(code)
                        
                        with open(save_path, 'w') as f:
                            f.write(clean_code)
                        
                        completed += 1
                    
                    print(f"({len(codes)} solutions, avg {sum(len(c) for c in codes)//len(codes)} chars)")
                else:
                    print("Failed")
    
    print("\n" + "="*70)
    print(f"GENERATION COMPLETE: {completed}/{total_tasks} solutions generated")
    print("="*70)
    print(f"\nGenerated code saved to: generated_code/")
    print("="*70)

def main():
    """Main function"""
    import sys
    
    # Generate k solutions per problem for pass@k evaluation
    k = 1
    
    # Allow k override from command line
    if len(sys.argv) > 1 and sys.argv[1].startswith('k='):
        k = int(sys.argv[1].split('=')[1])
        print(f"Using k={k} (overridden from command line)")
    
       
    run_generation(k=k)


if __name__ == "__main__":
    main()