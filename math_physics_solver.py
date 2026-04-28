"""
Math and Physics Problem Solver AI
Solves mathematical and physics problems using symbolic computation and LLM assistance
"""

import os
from typing import Dict, Any
import sympy as sp
from sympy import symbols, solve, diff, integrate, simplify, sqrt, sin, cos, tan, exp, log
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MathPhysicsSolver:
    """AI solver for math and physics problems"""
    
    def __init__(self):
        """Initialize the solver"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.problem_history = []
    
    def _preprocess_input(self, input_str: str) -> str:
        """Convert common math notation to Python syntax"""
        import re
        
        # Replace ^ with **
        result = input_str.replace('^', '**')
        
        # Add * between number and variable: 2x -> 2*x
        result = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', result)
        
        # Add * between ) and (: )( -> )*(
        result = result.replace(')(', ')*(')
        
        # Add * between variable and (: x( -> x*(
        result = re.sub(r'([a-zA-Z])\(', r'\1*(', result)
        
        # Add * between ) and variable: )x -> )*x
        result = re.sub(r'\)([a-zA-Z])', r')*\1', result)
        
        return result
    
    def _format_step_by_step(self, title: str, steps: list) -> str:
        """Format step-by-step solution for display"""
        output = f"\n{'='*60}\n{title}\n{'='*60}\n"
        for i, step in enumerate(steps, 1):
            output += f"\nStep {i}: {step}\n"
        output += f"{'='*60}\n"
        return output
        
    def solve_algebraic_equation(self, equation_str: str, variable: str = 'x') -> Dict[str, Any]:
        """
        Solve algebraic equations
        
        Args:
            equation_str: Equation string (e.g., "x**2 - 5*x + 6 = 0")
            variable: Variable to solve for
            
        Returns:
            Dictionary with solution and steps
        """
        try:
            equation_str = self._preprocess_input(equation_str)
            var = symbols(variable)
            # Parse the equation (assuming format "lhs = rhs")
            if '=' in equation_str:
                lhs, rhs = equation_str.split('=')
                equation = sp.sympify(lhs) - sp.sympify(rhs)
            else:
                equation = sp.sympify(equation_str)
            
            solutions = solve(equation, var)
            
            # Generate step-by-step solution
            steps = [
                f"Original equation: {equation_str}",
                f"Rearrange to standard form: {equation} = 0",
                f"Using SymPy solver to find all roots",
                f"Found {len(solutions)} solution(s)"
            ]
            
            # Add factorization info if quadratic
            try:
                factored = sp.factor(equation)
                if factored != equation:
                    steps.insert(2, f"Factored form: {factored} = 0")
            except:
                pass
            
            for i, sol in enumerate(solutions, 1):
                steps.append(f"Solution {i}: {variable} = {sol}")
            
            return {
                "type": "algebraic",
                "equation": equation_str,
                "variable": variable,
                "solutions": solutions,
                "simplified": [simplify(sol) for sol in solutions],
                "steps": steps,
                "formatted": self._format_step_by_step(f"Solving: {equation_str}", steps)
            }
        except Exception as e:
            return {"error": str(e), "type": "algebraic"}
    
    def solve_calculus_derivative(self, function_str: str, variable: str = 'x') -> Dict[str, Any]:
        """
        Find derivative of a function
        
        Args:
            function_str: Function string (e.g., "x**3 + 2*x**2 - 5*x + 3")
            variable: Variable to differentiate with respect to
            
        Returns:
            Dictionary with derivative and steps
        """
        try:
            function_str = self._preprocess_input(function_str)
            var = symbols(variable)
            func = sp.sympify(function_str)
            derivative = diff(func, var)
            simplified_derivative = simplify(derivative)
            
            # Generate step-by-step solution
            steps = [
                f"Original function: f({variable}) = {func}",
                f"We need to find: df/d{variable}",
                "Applying differentiation rules:",
            ]
            
            # Parse the function and explain rules
            if '+' in function_str or '-' in function_str:
                steps.append("  • Sum/difference rule: d/dx[f(x) ± g(x)] = df/dx ± dg/dx")
            if '**' in function_str:
                steps.append("  • Power rule: d/dx[x^n] = n·x^(n-1)")
            
            steps.extend([
                f"Computing the derivative term by term:",
                f"Result: df/d{variable} = {derivative}",
                f"Simplified: df/d{variable} = {simplified_derivative}"
            ])
            
            return {
                "type": "derivative",
                "function": function_str,
                "variable": variable,
                "derivative": derivative,
                "simplified": simplified_derivative,
                "steps": steps,
                "formatted": self._format_step_by_step(f"Finding derivative of: {function_str}", steps)
            }
        except Exception as e:
            return {"error": str(e), "type": "derivative"}
    
    def solve_calculus_integral(self, function_str: str, variable: str = 'x') -> Dict[str, Any]:
        """
        Find indefinite integral of a function
        
        Args:
            function_str: Function string (e.g., "x**3 + 2*x**2 - 5*x + 3")
            variable: Variable to integrate with respect to
            
        Returns:
            Dictionary with integral and steps
        """
        try:
            function_str = self._preprocess_input(function_str)
            var = symbols(variable)
            func = sp.sympify(function_str)
            integral = integrate(func, var)
            simplified_integral = simplify(integral)
            
            # Generate step-by-step solution
            steps = [
                f"Original function: f({variable}) = {func}",
                f"We need to find: ∫ f({variable}) d{variable}",
                "Applying integration rules:",
            ]
            
            # Parse the function and explain rules
            if '+' in function_str or '-' in function_str:
                steps.append("  • Sum/difference rule: ∫[f(x) ± g(x)]dx = ∫f(x)dx ± ∫g(x)dx")
            if '**' in function_str:
                steps.append("  • Power rule: ∫x^n dx = x^(n+1)/(n+1) + C")
            
            steps.extend([
                f"Integrating term by term:",
                f"Result: ∫ f({variable}) d{variable} = {integral} + C",
                f"Simplified: {simplified_integral} + C",
                "(where C is the constant of integration)"
            ])
            
            return {
                "type": "integral",
                "function": function_str,
                "variable": variable,
                "integral": integral,
                "simplified": simplified_integral,
                "steps": steps,
                "formatted": self._format_step_by_step(f"Finding integral of: {function_str}", steps)
            }
        except Exception as e:
            return {"error": str(e), "type": "integral"}
    
    def solve_physics_problem(self, problem_description: str) -> Dict[str, Any]:
        """
        Solve physics problems using formulas
        Common physics formulas for kinematics, dynamics, energy, etc.
        
        Args:
            problem_description: Description of the physics problem
            
        Returns:
            Dictionary with solution approach and guidance
        """
        # This is a placeholder - would integrate with LLM for natural language understanding
        physics_formulas = {
            "kinematics": {
                "v = u + at": "Final velocity",
                "s = ut + 0.5*a*t**2": "Displacement",
                "v**2 = u**2 + 2*a*s": "Final velocity (no time)",
            },
            "dynamics": {
                "F = m*a": "Newton's second law",
                "F = G*m1*m2/r**2": "Gravitational force",
            },
            "energy": {
                "E_k = 0.5*m*v**2": "Kinetic energy",
                "E_p = m*g*h": "Potential energy",
                "W = F*d*cos(theta)": "Work done",
            }
        }
        
        return {
            "type": "physics",
            "problem": problem_description,
            "formulas": physics_formulas,
            "message": "Physics problem detected. Provide specific values for calculation."
        }
    
    def solve_system_of_equations(self, equations: list, variables: list) -> Dict[str, Any]:
        """
        Solve system of linear or nonlinear equations
        
        Args:
            equations: List of equations (e.g., ["x + y = 5", "2*x - y = 1"])
            variables: List of variables to solve for (e.g., ["x", "y"])
            
        Returns:
            Dictionary with solutions
        """
        try:
            var_symbols = symbols(variables)
            if len(variables) == 1:
                var_symbols = [var_symbols]
            
            equations_sympified = []
            for eq in equations:
                eq = self._preprocess_input(eq)
                if '=' in eq:
                    lhs, rhs = eq.split('=')
                    equations_sympified.append(sp.sympify(lhs) - sp.sympify(rhs))
                else:
                    equations_sympified.append(sp.sympify(eq))
            
            solutions = solve(equations_sympified, var_symbols)
            
            # Generate step-by-step solution
            steps = [
                "System of equations:",
            ]
            for i, eq in enumerate(equations, 1):
                steps.append(f"  Equation {i}: {eq}")
            
            steps.extend([
                f"\nVariables to solve for: {', '.join(variables)}",
                "Using simultaneous equation solver (elimination/substitution method)",
                f"\nSolving the system...",
                f"Solution found:"
            ])
            
            if isinstance(solutions, dict):
                for var, val in solutions.items():
                    steps.append(f"  {var} = {val}")
            elif isinstance(solutions, list) and solutions and isinstance(solutions[0], tuple):
                for var, val in zip(variables, solutions[0]):
                    steps.append(f"  {var} = {val}")
            else:
                steps.append(f"  {solutions}")
            
            steps.append("\nVerification: Substitute back into original equations to verify")
            
            return {
                "type": "system",
                "equations": equations,
                "variables": variables,
                "solutions": solutions,
                "steps": steps,
                "formatted": self._format_step_by_step("Solving System of Equations", steps)
            }
        except Exception as e:
            return {"error": str(e), "type": "system"}


def main():
    """Main function to demonstrate the solver"""
    solver = MathPhysicsSolver()
    
    print("=" * 60)
    print("Math and Physics Problem Solver AI - Step-by-Step Solutions")
    print("=" * 60)
    
    # Example 1: Algebraic equation
    print("\n1. Solving algebraic equation: x**2 - 5*x + 6 = 0")
    result = solver.solve_algebraic_equation("x**2 - 5*x + 6 = 0")
    print(result['formatted'])
    
    # Example 2: Derivative
    print("\n2. Finding derivative of: x**3 + 2*x**2 - 5*x + 3")
    result = solver.solve_calculus_derivative("x**3 + 2*x**2 - 5*x + 3")
    print(result['formatted'])
    
    # Example 3: Integral
    print("\n3. Finding integral of: x**3 + 2*x")
    result = solver.solve_calculus_integral("x**3 + 2*x")
    print(result['formatted'])
    
    # Example 4: System of equations
    print("\n4. Solving system: x + y = 5, 2*x - y = 1")
    result = solver.solve_system_of_equations(["x + y = 5", "2*x - y = 1"], ["x", "y"])
    print(result['formatted'])
    
    # Example 5: Physics problem
    print("\n5. Physics problem analysis")
    result = solver.solve_physics_problem("A ball is thrown with initial velocity 20 m/s at 45 degrees")
    print(f"   Available formulas: {list(result['formulas'].keys())}")


if __name__ == "__main__":
    main()
