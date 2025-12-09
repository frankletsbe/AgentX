# Output Folder Organization

## Overview

AgentX automatically organizes all generated code and deliverables into folders named after your requirement files. This keeps your projects organized and makes it easy to manage multiple development tasks.

## How It Works

### Automatic Folder Creation

When you select a requirement YAML file, AgentX automatically:
1. Extracts the filename (without extension)
2. Creates an output folder with that name
3. Saves all deliverables to that folder

### Example

**Requirement File:** `requirements/holiday-park.yaml`

**Output Folder:** `output/holiday-park/`

**Generated Files:**
```
output/
└── holiday-park/
    ├── specification.txt
    ├── final_code.py
    ├── ux_feedback.txt
    ├── test_feedback.txt
    └── summary.txt
```

## Folder Structure

```
AgentX/
├── requirements/
│   ├── holiday-park.yaml
│   ├── todo-app.yaml
│   └── calculator.yaml
├── output/
│   ├── holiday-park/
│   │   ├── specification.txt
│   │   ├── final_code.py
│   │   ├── ux_feedback.txt
│   │   ├── test_feedback.txt
│   │   └── summary.txt
│   ├── todo-app/
│   │   └── [deliverables...]
│   └── calculator/
│       └── [deliverables...]
```

## Deliverables

Each output folder contains:

### 1. specification.txt
Complete specification document created by the Business Analyst

### 2. final_code.py
Final application code after all iterations and feedback

### 3. ux_feedback.txt
UX Designer's feedback on the user interface and experience

### 4. test_feedback.txt
QA Tester's feedback on code quality and testing results

### 5. summary.txt
Development summary including:
- Original requirement
- Number of iterations
- List of all deliverables

## Manual Requirements

If you enter requirements manually (option 2), you'll be prompted to specify an output folder name. The default is `output/`.

## Benefits

- **Organization**: Each project has its own dedicated folder
- **No Conflicts**: Multiple projects don't overwrite each other
- **Easy Navigation**: Find project outputs by requirement name
- **Version Control**: Track changes to specific projects over time
- **Clean Structure**: Keeps your workspace organized

## Configuration

The output root directory is defined in `constants.py`:

```python
OUTPUT_ROOT = PROJECT_ROOT / "output"
```

You can modify this if you want outputs saved to a different location.

## Tips

1. **Naming Convention**: Use descriptive names for your requirement YAML files
   - Good: `holiday-park.yaml`, `user-authentication.yaml`
   - Avoid: `test.yaml`, `temp.yaml`

2. **Multiple Runs**: Running the same requirement multiple times will overwrite previous outputs in that folder

3. **Backup Important Work**: If you want to preserve multiple versions, manually rename or copy the output folders

4. **Clean Up**: Periodically review and clean up old output folders you no longer need

## Example Workflow

```bash
# 1. Create your requirement file
requirements/holiday-park.yaml

# 2. Run the development team
python Agents/dev_team.py

# 3. Select option 1 (YAML file)

# 4. Choose your requirement

# 5. Output automatically saved to:
output/holiday-park/
```

## Related Files

- `constants.py` - Defines OUTPUT_ROOT and get_output_folder()
- `agents/manager_agent.py` - Extracts folder name from YAML
- `Agents/dev_team.py` - Saves deliverables to the correct folder
