#!/usr/bin/env python3
"""
Code Generation Tool

This script takes a coding problem description as input and generates a solution
using an AI agent-based system.

Usage:
    python check.py "Write a function that calculates the factorial of a number"
    python check.py --file problem.txt

Options:
    --file FILE       Read the problem description from a file
    --output FILE     Save the generated code to a file
"""

from main import solve
import argparse
import sys

def main():
    """Main function to run the code generation tool."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate code solutions for coding problems')
    parser.add_argument('problem', nargs='?', help='The coding problem description')
    parser.add_argument('--file', help='Read the problem description from a file')
    parser.add_argument('--output', help='Save the generated code to a file')
    args = parser.parse_args()
    
    # Get the problem description
    problem_description = ""
    if args.file:
        try:
            with open(args.file, 'r') as f:
                problem_description = f.read()
        except FileNotFoundError:
            print(f"Error: Could not find file {args.file}")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    elif args.problem:
        problem_description = args.problem
    else:
        # Read from stdin if no problem is provided
        print("Enter the coding problem description (Ctrl+D to finish):")
        problem_description = sys.stdin.read()
    
    if not problem_description.strip():
        print("Error: No problem description provided")
        return
    
    try:
        # Generate the solution
        print("Generating solution...")
        solution = solve(problem_description)
        
        # Output the solution
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    f.write(solution)
                print(f"Solution saved to {args.output}")
            except Exception as e:
                print(f"Error saving solution: {e}")
                print("\nGenerated solution:")
                print("="*50)
                print(solution)
                print("="*50)
        else:
            print("\nGenerated solution:")
            print("="*50)
            print(solution)
            print("="*50)
            
    except Exception as e:
        print(f"Error generating solution: {e}")
        return


if __name__ == "__main__":
    main()
        