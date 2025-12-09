"""
GUI for AI Agent Application
Allows users to enter prompts and select tools.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
import yaml
from typing import Dict, Any

from constants import ConfigurationError, CONFIG_FILE, PROMPT_FILE, AVAILABLE_TOOLS
from config_loader import YAMLConfigLoader
from agent_manager import initialize_huggingface, create_agent


class AgentGUI:
    """GUI for the AI Agent application."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Agent Application")
        self.root.geometry("900x700")
        
        self.config_loader = YAMLConfigLoader()
        self.agent = None
        
        self._setup_ui()
        self._load_initial_config()
    
    def _setup_ui(self):
        """Setup the user interface."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # === PROMPT SECTION ===
        prompt_label = ttk.Label(main_frame, text="Enter Your Prompt:", font=("Arial", 12, "bold"))
        prompt_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.prompt_text = scrolledtext.ScrolledText(
            main_frame, 
            height=10, 
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.prompt_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # === TOOLS SECTION ===
        tools_label = ttk.Label(main_frame, text="Select Tools:", font=("Arial", 12, "bold"))
        tools_label.grid(row=2, column=0, sticky="w", pady=(10, 5))
        
        # Tools frame with checkboxes
        tools_frame = ttk.LabelFrame(main_frame, text="Available Tools", padding="10")
        tools_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        self.tool_vars = {}
        for idx, tool_name in enumerate(AVAILABLE_TOOLS.keys()):
            var = tk.BooleanVar(value=False)
            self.tool_vars[tool_name] = var
            
            cb = ttk.Checkbutton(
                tools_frame, 
                text=tool_name, 
                variable=var
            )
            cb.grid(row=idx // 2, column=idx % 2, sticky="w", padx=5, pady=2)
        
        # === BUTTONS ===
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=10)
        
        self.run_button = ttk.Button(
            button_frame, 
            text="Run Agent", 
            command=self._run_agent,
            width=15
        )
        self.run_button.grid(row=0, column=0, padx=5)
        
        save_button = ttk.Button(
            button_frame, 
            text="Save Prompt", 
            command=self._save_prompt,
            width=15
        )
        save_button.grid(row=0, column=1, padx=5)
        
        clear_button = ttk.Button(
            button_frame, 
            text="Clear", 
            command=self._clear_all,
            width=15
        )
        clear_button.grid(row=0, column=2, padx=5)
        
        # === RESULTS SECTION ===
        results_label = ttk.Label(main_frame, text="Results:", font=("Arial", 12, "bold"))
        results_label.grid(row=5, column=0, sticky="w", pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(
            main_frame, 
            height=15, 
            wrap=tk.WORD,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.results_text.grid(row=6, column=0, sticky="nsew")
        
        # === STATUS BAR ===
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor="w"
        )
        status_bar.grid(row=7, column=0, sticky="ew", pady=(10, 0))
    
    def _load_initial_config(self):
        """Load initial configuration and prompt."""
        try:
            # Load existing prompt if available
            if PROMPT_FILE.exists():
                with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                    prompt_data = yaml.safe_load(f)
                    if isinstance(prompt_data, dict):
                        # Combine all fields into display text
                        prompt_display = self._format_prompt_for_display(prompt_data)
                        self.prompt_text.insert("1.0", prompt_display)
            
            # Load enabled tools from config
            if CONFIG_FILE.exists():
                enabled_tools = self.config_loader.get_config_list(CONFIG_FILE, "enabled_tools")
                for tool_name in enabled_tools:
                    if tool_name in self.tool_vars:
                        self.tool_vars[tool_name].set(True)
            
            self.status_var.set("Configuration loaded successfully")
            
        except Exception as e:
            self.status_var.set(f"Warning: {str(e)}")
    
    def _format_prompt_for_display(self, prompt_data: Dict[str, Any]) -> str:
        """Format prompt data for display in text widget."""
        lines = []
        for key, value in prompt_data.items():
            if key != "overrides":
                lines.append(f"{key.upper()}:\n{value}\n")
        return "\n".join(lines)
    
    def _parse_prompt_from_text(self) -> Dict[str, str]:
        """Parse the text widget content into prompt structure."""
        text = self.prompt_text.get("1.0", tk.END).strip()
        
        # Simple parsing: look for ROLE:, TASK:, etc.
        prompt_dict = {}
        current_key = None
        current_value = []
        
        for line in text.split("\n"):
            line_upper = line.strip().upper()
            
            # Check if line is a key
            if line_upper.endswith(":") and line_upper.rstrip(":") in [
                "ROLE", "TASK", "REQUIREMENTS", "TOOLS_DESCRIPTION", "OUTPUT_FORMAT"
            ]:
                # Save previous key-value
                if current_key:
                    prompt_dict[current_key] = "\n".join(current_value).strip()
                
                # Start new key
                current_key = line_upper.rstrip(":").lower()
                current_value = []
            else:
                # Add to current value
                if line.strip():
                    current_value.append(line)
        
        # Save last key-value
        if current_key:
            prompt_dict[current_key] = "\n".join(current_value).strip()
        
        # If no structured format found, treat entire text as task
        if not prompt_dict:
            prompt_dict = {"task": text}
        
        return prompt_dict
    
    def _get_selected_tools(self) -> list:
        """Get list of selected tools."""
        return [tool for tool, var in self.tool_vars.items() if var.get()]
    
    def _save_prompt(self):
        """Save the current prompt to prompt.yaml."""
        try:
            prompt_dict = self._parse_prompt_from_text()
            
            with open(PROMPT_FILE, "w", encoding="utf-8") as f:
                yaml.dump(prompt_dict, f, default_flow_style=False, sort_keys=False)
            
            messagebox.showinfo("Success", "Prompt saved to prompt.yaml")
            self.status_var.set("Prompt saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save prompt: {e}")
            self.status_var.set(f"Error: {e}")
    
    def _clear_all(self):
        """Clear all inputs and results."""
        self.prompt_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        for var in self.tool_vars.values():
            var.set(False)
        
        self.status_var.set("Cleared")
    
    def _run_agent(self):
        """Run the agent with current prompt and tools."""
        try:
            # Validate inputs
            prompt_text = self.prompt_text.get("1.0", tk.END).strip()
            if not prompt_text:
                messagebox.showwarning("Warning", "Please enter a prompt")
                return
            
            selected_tools = self._get_selected_tools()
            if not selected_tools:
                messagebox.showwarning("Warning", "Please select at least one tool")
                return
            
            # Disable button during processing
            self.run_button.config(state=tk.DISABLED)
            self.status_var.set("Processing...")
            self.root.update()
            
            # Clear previous results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete("1.0", tk.END)
            self.results_text.config(state=tk.DISABLED)
            
            # Load configuration
            token = self.config_loader.get_config_value(CONFIG_FILE, "HF_TOKEN")
            model_name = self.config_loader.get_config_value(CONFIG_FILE, "MODEL_NAME")
            search_provider = self.config_loader.get_config_value(CONFIG_FILE, "SEARCH_PROVIDER")
            
            # Initialize agent if not already done
            if not self.agent:
                initialize_huggingface(token)
            
            # Create agent with selected tools
            agent = create_agent(model_name, search_provider, selected_tools)
            
            # Run agent with error handling
            self.status_var.set("Agent running...")
            self.root.update()
            
            try:
                response = agent.run(task=prompt_text)
                result_text = str(response)
            except SyntaxError as se:
                # Handle syntax errors from malformed agent code
                result_text = f"Agent encountered a syntax error. This usually means the response was too long or complex.\n\nError: {str(se)}\n\nTry:\n- Simplifying your prompt\n- Asking for fewer results\n- Being more specific in your requirements"
            except Exception as agent_error:
                result_text = f"Agent execution error: {str(agent_error)}"
            
            # Display results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.insert("1.0", result_text)
            self.results_text.config(state=tk.DISABLED)
            
            self.status_var.set("Completed")
            
        except ConfigurationError as e:
            messagebox.showerror("Configuration Error", str(e))
            self.status_var.set(f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_var.set(f"Error: {e}")
        finally:
            self.run_button.config(state=tk.DISABLED)


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = AgentGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()