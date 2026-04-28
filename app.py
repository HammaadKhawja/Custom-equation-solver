"""
Flask web application for the Math/Physics Problem Solver
Provides a GUI interface with text and image input
"""

import sys
import os
from flask import Flask, render_template, request, jsonify

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from math_physics_solver import MathPhysicsSolver

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize solver
solver = MathPhysicsSolver()

# Ensure uploads folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve():
    """API endpoint to solve problems"""
    try:
        data = request.json
        problem_type = data.get('type')
        input_text = data.get('input', '').strip()
        
        if not input_text:
            return jsonify({'error': 'No input provided'}), 400
        
        result = {}
        
        if problem_type == 'equation':
            result = solver.solve_algebraic_equation(input_text)
        elif problem_type == 'derivative':
            result = solver.solve_calculus_derivative(input_text)
        elif problem_type == 'integral':
            result = solver.solve_calculus_integral(input_text)
        elif problem_type == 'system':
            equations = [eq.strip() for eq in input_text.split('\n') if eq.strip()]
            variables_input = data.get('variables', 'x,y,z')
            variables = [v.strip() for v in variables_input.split(',')]
            result = solver.solve_system_of_equations(equations, variables)
        else:
            return jsonify({'error': 'Unknown problem type'}), 400
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        
        # Ensure steps are serializable strings
        steps = result.get('steps', [])
        steps = [str(step) for step in steps]
        
        # Extract solution forms for better display
        solution_data = {
            'expanded': None,
            'simplified': None,
            'final': None
        }
        
        # For integrals and derivatives, provide both forms
        if problem_type == 'integral':
            solution_data['expanded'] = str(result.get('integral', ''))
            solution_data['simplified'] = str(result.get('simplified', ''))
            solution_data['final'] = f"{solution_data['simplified']} + C"
        elif problem_type == 'derivative':
            solution_data['expanded'] = str(result.get('derivative', ''))
            solution_data['simplified'] = str(result.get('simplified', ''))
            solution_data['final'] = solution_data['simplified']
        elif problem_type == 'equation':
            solutions = result.get('solutions', [])
            solution_data['final'] = str(solutions) if solutions else 'No real solutions'
        elif problem_type == 'system':
            solution_data['final'] = str(result.get('solutions', {}))
        
        return jsonify({
            'success': True,
            'steps': steps,
            'formatted': result.get('formatted', ''),
            'type': result.get('type', problem_type),
            'solutions': solution_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect-type', methods=['POST'])
def detect_type():
    """Detect problem type from user input"""
    try:
        data = request.json
        input_text = data.get('input', '').lower()
        
        if 'integral' in input_text or '∫' in input_text:
            return jsonify({'type': 'integral', 'suggestion': 'Integral'})
        elif 'deriv' in input_text or 'd/d' in input_text or "'" in input_text:
            return jsonify({'type': 'derivative', 'suggestion': 'Derivative'})
        elif 'system' in input_text or ('\n' in input_text and '=' in input_text):
            return jsonify({'type': 'system', 'suggestion': 'System of Equations'})
        else:
            return jsonify({'type': 'equation', 'suggestion': 'Equation'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Math & Physics Solver is starting...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("="*60 + "\n")
    app.run(debug=False, port=8000, use_reloader=False)
