"""
Gradio Chat Interface for AI Agent with Execution Log
"""

import gradio as gr
from datetime import datetime
from constants import ConfigurationError, AVAILABLE_TOOLS
from agent_manager import initialize_huggingface, create_agent


hf_initialized = False
execution_logs = []


def add_log(message, level="INFO"):
    """Add entry to execution log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    execution_logs.append(log_entry)
    return "\n".join(execution_logs)


def run_agent_chat(message, history, *tool_selections):
    """Run agent with chat interface."""
    global hf_initialized
    
    # Initialize history if None
    if history is None:
        history = []
    
    try:
        add_log(f"New query received: {message[:50]}...", "INFO")
        
        # Get selected tools
        selected_tools = [
            tool for tool, selected in zip(AVAILABLE_TOOLS.keys(), tool_selections) 
            if selected
        ]
        
        if not selected_tools:
            add_log("No tools selected", "WARNING")
            history.append((message, "⚠️ Please select at least one tool"))
            return history, "\n".join(execution_logs)
        
        add_log(f"Selected tools: {', '.join(selected_tools)}", "INFO")
        
        # Initialize HF once
        if not hf_initialized:
            add_log("Initializing Hugging Face...", "INFO")
            initialize_huggingface()
            hf_initialized = True
            add_log("Hugging Face initialized successfully", "SUCCESS")
        
        # Create and run agent
        add_log("Creating agent...", "INFO")
        agent = create_agent(selected_tools)
        add_log("Agent created successfully", "SUCCESS")
        
        add_log("Running agent...", "INFO")
        response = agent.run(task=message)
        add_log("Agent execution completed", "SUCCESS")
        
        # Add to history
        history.append((message, str(response)))
        
        return history, "\n".join(execution_logs)
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        add_log(error_msg, "ERROR")
        history.append((message, f"❌ {error_msg}"))
        return history, "\n".join(execution_logs)


def clear_chat():
    """Clear chat and logs."""
    global execution_logs
    execution_logs = []
    add_log("Chat and logs cleared", "INFO")
    return [], "\n".join(execution_logs)


def clear_logs_only():
    """Clear only the logs."""
    global execution_logs
    execution_logs = []
    add_log("Logs cleared", "INFO")
    return "\n".join(execution_logs)


# Create interface with custom CSS
custom_css = """
.log-container {
    font-family: 'Courier New', monospace;
    font-size: 12px;
    background-color: #1e1e1e;
    color: #d4d4d4;
    padding: 10px;
    border-radius: 5px;
    max-height: 400px;
    overflow-y: auto;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🤖 AI Agent Chat Interface")
    gr.Markdown("Select tools, chat with the AI agent, and monitor execution logs")
    
    with gr.Row():
        # Left column - Chat interface
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chat")
            chatbot = gr.Chatbot(
                height=500,
                show_label=False,
                avatar_images=(None, "🤖")
            )
            msg = gr.Textbox(
                label="Your Message",
                placeholder="Enter your query here... (Press Enter to send)",
                lines=3,
                show_label=False
            )
            
            with gr.Row():
                submit = gr.Button("📤 Send", variant="primary", scale=2)
                clear = gr.Button("🗑️ Clear", scale=1)
        
        # Right column - Tools and Logs
        with gr.Column(scale=1):
            gr.Markdown("### 🛠️ Select Tools")
            tool_checkboxes = [
                gr.Checkbox(label=tool, value=False) 
                for tool in AVAILABLE_TOOLS.keys()
            ]
            
            gr.Markdown("### 📋 Execution Log")
            log_output = gr.Textbox(
                label="",
                lines=15,
                max_lines=15,
                show_label=False,
                interactive=False,
                elem_classes="log-container"
            )
            
            clear_logs = gr.Button("🧹 Clear Logs", size="sm")
    
    # Event handlers
    def submit_message(message, history, *tools):
        if not message.strip():
            return history or [], "", "\n".join(execution_logs)
        
        updated_history, logs = run_agent_chat(message, history, *tools)
        return updated_history, "", logs
    
    submit.click(
        submit_message,
        inputs=[msg, chatbot] + tool_checkboxes,
        outputs=[chatbot, msg, log_output]
    )
    
    msg.submit(
        submit_message,
        inputs=[msg, chatbot] + tool_checkboxes,
        outputs=[chatbot, msg, log_output]
    )
    
    clear.click(
        clear_chat,
        inputs=None,
        outputs=[chatbot, log_output]
    )
    
    clear_logs.click(
        clear_logs_only,
        inputs=None,
        outputs=log_output
    )
    
    # Initialize log on load
    demo.load(
        lambda: add_log("Application started", "INFO"),
        inputs=None,
        outputs=log_output
    )


if __name__ == "__main__":
    print("=" * 60)
    print("Starting AI Agent Chat Interface with Execution Logs")
    print("=" * 60)
    demo.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )