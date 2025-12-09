# Output Folder Refactoring - Summary

## What Changed

The codebase has been refactored so that all agent-generated code and deliverables are automatically saved to folders named after the requirement YAML file.

## Changes Made

### 1. `constants.py`
- Added `OUTPUT_ROOT` constant pointing to `output/` directory
- Added `get_output_folder()` utility function to generate folder paths from YAML filenames

### 2. `agents/manager_agent.py`
- Modified `select_requirement()` to extract folder name from YAML filename using `Path(filename).stem`
- Added `output_folder` to the requirement data dictionary
- Modified `coordinate_development()` to track and pass through the output folder
- Added `output_folder` to the return dictionary

### 3. `Agents/dev_team.py`
- Modified `main()` to automatically use the output folder from requirement data
- Automatic save when using YAML files (no prompt needed)
- Manual prompt only when entering requirements manually

## How It Works

```
requirements/holiday-park.yaml
         ↓
    [Extract stem: "holiday-park"]
         ↓
    output/holiday-park/
         ↓
    [Save all deliverables]
```

## Example Usage

### Before:
```
User selects: requirements/holiday-park.yaml
User prompted: "Enter output directory name (default: 'output'): "
Output saved to: output/ or user-specified folder
```

### After:
```
User selects: requirements/holiday-park.yaml
System automatically creates: output/holiday-park/
Output saved to: output/holiday-park/
No prompt needed!
```

## File Structure

```
AgentX/
├── requirements/
│   ├── holiday-park.yaml      → output/holiday-park/
│   ├── todo-app.yaml          → output/todo-app/
│   └── calculator.yaml        → output/calculator/
│
├── output/
│   ├── holiday-park/
│   │   ├── specification.txt
│   │   ├── final_code.py
│   │   ├── ux_feedback.txt
│   │   ├── test_feedback.txt
│   │   └── summary.txt
│   │
│   ├── todo-app/
│   │   └── [deliverables...]
│   │
│   └── calculator/
│       └── [deliverables...]
```

## Benefits

✓ **Automatic Organization** - No manual folder naming needed
✓ **No Conflicts** - Each project has its own folder
✓ **Easy Navigation** - Find outputs by requirement name
✓ **Consistent Structure** - Predictable folder layout
✓ **Better UX** - One less prompt for users

## Testing

To test the changes:

1. Create a requirement file: `requirements/test-project.yaml`
2. Run: `python Agents/dev_team.py`
3. Select option 1 (YAML file)
4. Choose your requirement
5. Verify output is saved to: `output/test-project/`

## Backward Compatibility

- Manual requirements (option 2) still prompt for folder name
- Default folder is still `output/` if no YAML file is used
- Existing code continues to work without changes
