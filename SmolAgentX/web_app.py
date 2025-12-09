"""
Web Application for AI Agent
Flask-based interface for entering prompts and selecting tools.
"""

from flask import Flask, render_template, request, jsonify, session
import secrets
from pathlib import Path

from constants import ConfigurationError, CONFIG_FILE, AVAILABLE_TOOLS
from config_loader import YAMLConfigLoader
from agent_manager import initialize_huggingface, create_agent


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Global config loader
config_loader = YAMLConfigLoader()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', tools=list(AVAILABLE_TOOLS.keys()))


@app.route('/run_agent', methods=['POST'])
def run_agent():
    """Run the agent with provided prompt and tools."""
    try:
        data = request.json
        prompt_text = data.get('prompt', '').strip()
        selected_tools = data.get('tools', [])
        
        # Validate inputs
        if not prompt_text:
            return jsonify({'error': 'Please enter a prompt'}), 400
        
        if not selected_tools:
            return jsonify({'error': 'Please select at least one tool'}), 400
        
        # Load configuration
        #token = config_loader.get_config_value(CONFIG_FILE, "HF_TOKEN")
        #model_name = config_loader.get_config_value(CONFIG_FILE, "MODEL_NAME")
        #search_provider = config_loader.get_config_value(CONFIG_FILE, "SEARCH_PROVIDER")
        
        # Initialize HuggingFace (only once)
        if 'hf_initialized' not in session:
            initialize_huggingface()
            session['hf_initialized'] = True
        
        # Create and run agent
        agent = create_agent(selected_tools)
        response = agent.run(task=prompt_text)
        
        return jsonify({
            'success': True,
            'result': str(response)
        })
        
    except ConfigurationError as e:
        return jsonify({'error': f'Configuration Error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    Path('templates').mkdir(exist_ok=True)
    
    print("=" * 60)
    print("Starting AI Agent Web Application")
    print("=" * 60)
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)