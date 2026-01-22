"""
Web interface for running agent_generic.py with real-time output display.
"""
from flask import Flask, render_template, Response, jsonify
import subprocess
import threading
import queue
import json
import re
from pathlib import Path

app = Flask(__name__)

# Global variables to store output
output_queue = queue.Queue()
final_result = {"content": "", "status": "idle"}
process_lock = threading.Lock()

def extract_final_result(output_text):
    """Extract the final results section from the output."""
    # Look for the RESULTS section
    results_match = re.search(r'={60}\s*RESULTS:\s*={60}(.*?)(?:={60}|$)', output_text, re.DOTALL)
    if results_match:
        return results_match.group(1).strip()
    return ""

def run_agent():
    """Run agent_generic.py and capture output."""
    global final_result
    
    with process_lock:
        final_result = {"content": "", "status": "running"}
        output_queue.queue.clear()
    
    try:
        # Run the agent script with explicit UTF-8 encoding
        process = subprocess.Popen(
            ['python', 'agent_generic.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace problematic characters instead of crashing
            bufsize=1,
            universal_newlines=True,
            cwd=Path(__file__).parent
        )
        
        full_output = []
        
        # Stream output line by line
        for line in iter(process.stdout.readline, ''):
            if line:
                full_output.append(line)
                output_queue.put(json.dumps({
                    'type': 'output',
                    'data': line
                }) + '\n')
        
        process.wait()
        
        # Extract final result
        complete_output = ''.join(full_output)
        final_content = extract_final_result(complete_output)
        
        with process_lock:
            final_result = {
                "content": final_content if final_content else "No results found in output.",
                "status": "completed" if process.returncode == 0 else "error"
            }
        
        output_queue.put(json.dumps({
            'type': 'complete',
            'data': final_result
        }) + '\n')
        
    except Exception as e:
        error_msg = f"Error running agent: {str(e)}"
        with process_lock:
            final_result = {"content": error_msg, "status": "error"}
        output_queue.put(json.dumps({
            'type': 'error',
            'data': error_msg
        }) + '\n')

@app.route('/')
def index():
    """Render the main page."""
    return render_template('agent_runner.html')

@app.route('/start')
def start_agent():
    """Start the agent in a background thread."""
    thread = threading.Thread(target=run_agent, daemon=True)
    thread.start()
    return jsonify({"status": "started"})

@app.route('/stream')
def stream():
    """Stream the agent output to the client."""
    def generate():
        while True:
            try:
                message = output_queue.get(timeout=1)
                yield f"data: {message}\n\n"
            except queue.Empty:
                # Check if process is still running
                with process_lock:
                    if final_result["status"] in ["completed", "error"]:
                        break
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/status')
def status():
    """Get current status and final result."""
    with process_lock:
        return jsonify(final_result)

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
