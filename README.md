# Math & Physics Problem Solver AI

An AI-powered solver for mathematical and physics problems using symbolic computation and natural language processing.

## Features

- **Algebraic Equations**: Solve polynomial and algebraic equations
- **Calculus**: Find derivatives and integrals
- **Systems of Equations**: Solve linear and nonlinear systems
- **Physics Problems**: Structured physics problem solving with formula assistance
- **Natural Language**: AI-powered problem understanding and explanation

## Project Structure

```
.
├── math_physics_solver.py    # Core solver implementation
├── llm_integration.py        # LLM integration for NLP (to be created)
├── web_ui.py                 # Web interface (to be created)
├── requirements.txt          # Dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd Python
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage
```python
from math_physics_solver import MathPhysicsSolver

solver = MathPhysicsSolver()

# Solve algebraic equation
result = solver.solve_algebraic_equation("x**2 - 5*x + 6 = 0")
print(result['solutions'])

# Find derivative
result = solver.solve_calculus_derivative("x**3 + 2*x**2 - 5*x + 3")
print(result['derivative'])

# Find integral
result = solver.solve_calculus_integral("x**3 + 2*x")
print(result['integral'])

# Solve system of equations
result = solver.solve_system_of_equations(["x + y = 5", "2*x - y = 1"], ["x", "y"])
print(result['solutions'])
```

### Running Examples
```bash
python math_physics_solver.py
```

## Technologies Used

- **SymPy**: Symbolic mathematics
- **NumPy/SciPy**: Numerical computations
- **OpenAI API**: Natural language understanding and generation
- **Python 3.9+**: Core language

## Next Steps

- [ ] Create LLM integration for natural language problem input
- [ ] Build web UI for user-friendly interface
- [ ] Add support for more physics domains (optics, thermodynamics, quantum)
- [ ] Implement step-by-step solution generation
- [ ] Add graph plotting capabilities
- [ ] Create test suite

## License

MIT License

## Contributing

Feel free to fork and submit pull requests!
