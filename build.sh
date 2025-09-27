#!/bin/bash
# build.sh - Simple script to build the ConnectOnion Developer Assistant executable

echo "🧅 ConnectOnion Developer Assistant - Build Script"
echo "=================================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install pip"
    exit 1
fi

echo "🔍 Checking/Installing dependencies..."

# Install required packages
pip install connectonion pyinstaller

echo "🚀 Building executable..."

# Create the optimized standalone script
cat > dev_assistant_standalone.py << 'EOF'
#!/usr/bin/env python3
"""
ConnectOnion Developer Assistant - Standalone Executable
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def get_connectonion_agent():
    try:
        from connectonion import Agent
        return Agent
    except ImportError:
        print("❌ ConnectOnion not found. Please install: pip install connectonion")
        sys.exit(1)

# Storage setup
STORAGE_DIR = Path.home() / '.connectonion_dev_assistant'
STORAGE_DIR.mkdir(exist_ok=True)
CONTEXT_FILE = STORAGE_DIR / 'contexts.json'

def get_project_info() -> dict:
    cwd = os.getcwd()
    project_name = os.path.basename(cwd)
    
    try:
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL).decode().strip()
        branch = subprocess.check_output(['git', 'branch', '--show-current'], stderr=subprocess.DEVNULL).decode().strip()
        modified_files = subprocess.check_output(['git', 'status', '--porcelain'], stderr=subprocess.DEVNULL).decode().strip().split('\n')
        
        return {
            'project_name': os.path.basename(repo_root),
            'working_dir': cwd,
            'is_git_repo': True,
            'branch': branch,
            'modified_files': [f.strip() for f in modified_files if f.strip()]
        }
    except:
        return {
            'project_name': project_name,
            'working_dir': cwd,
            'is_git_repo': False
        }

def save_coding_context(description: str) -> str:
    project_info = get_project_info()
    contexts = {}
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, 'r') as f:
            contexts = json.load(f)
    
    project_name = project_info['project_name']
    if project_name not in contexts:
        contexts[project_name] = []
    
    context_entry = {
        'timestamp': datetime.now().isoformat(),
        'description': description,
        'project_info': project_info
    }
    
    contexts[project_name].append(context_entry)
    contexts[project_name] = contexts[project_name][-10:]
    
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(contexts, f, indent=2)
    
    return f"💾 Saved context for '{project_name}': {description}"

def recall_coding_context() -> str:
    project_info = get_project_info()
    project_name = project_info['project_name']
    
    if not CONTEXT_FILE.exists():
        return "🤔 No saved contexts yet. Try: 'save context - what you're working on'"
    
    with open(CONTEXT_FILE, 'r') as f:
        contexts = json.load(f)
    
    if project_name not in contexts or not contexts[project_name]:
        return f"🤔 No saved context for '{project_name}'. Try: 'save context - what you're working on'"
    
    last_context = contexts[project_name][-1]
    timestamp = datetime.fromisoformat(last_context['timestamp'])
    
    result = f"🧠 Last context for '{project_name}':\n"
    result += f"📝 {last_context['description']}\n"
    result += f"⏰ Saved: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    if last_context['project_info'].get('branch'):
        result += f"🌿 Branch: {last_context['project_info']['branch']}\n"
    
    return result

def show_all_projects() -> str:
    if not CONTEXT_FILE.exists():
        return "📊 No projects tracked yet!"
    
    with open(CONTEXT_FILE, 'r') as f:
        contexts = json.load(f)
    
    if not contexts:
        return "📊 No projects tracked yet!"
    
    result = "📊 All tracked projects:\n\n"
    
    for project_name, project_contexts in contexts.items():
        if not project_contexts:
            continue
        
        last_ctx = project_contexts[-1]
        last_time = datetime.fromisoformat(last_ctx['timestamp'])
        time_ago = datetime.now() - last_time
        
        if time_ago.days > 0:
            time_str = f"{time_ago.days}d ago"
        elif time_ago.seconds > 3600:
            time_str = f"{time_ago.seconds // 3600}h ago"
        else:
            time_str = f"{time_ago.seconds // 60}m ago"
        
        result += f"🗂️  {project_name}\n"
        result += f"   📝 {last_ctx['description'][:60]}...\n"
        result += f"   ⏰ {time_str} • {len(project_contexts)} sessions\n\n"
    
    return result

def setup_new_project(project_type: str, project_name: str = "") -> str:
    templates = {
        'react': {
            'description': 'React + TypeScript + Vite',
            'commands': [
                f'npm create vite@latest {project_name or "."} -- --template react-ts',
                'npm install'
            ]
        },
        'python': {
            'description': 'Python + FastAPI',
            'commands': [
                'python -m venv venv',
                '. venv/bin/activate && pip install fastapi uvicorn'
            ]
        }
    }
    
    if project_type not in templates:
        available = ', '.join(templates.keys())
        return f"❌ Unknown type '{project_type}'. Available: {available}"
    
    template = templates[project_type]
    result = f"🚀 Setting up {template['description']}\n"
    
    if project_name:
        try:
            os.makedirs(project_name, exist_ok=True)
            os.chdir(project_name)
            result += f"📁 Created: {project_name}\n"
        except Exception as e:
            return f"❌ Failed: {e}"
    
    for i, cmd in enumerate(template['commands'], 1):
        result += f"[{i}/{len(template['commands'])}] {cmd}\n"
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            result += "✅ Done\n"
        except subprocess.CalledProcessError as e:
            result += f"❌ Failed: {e}\n"
            break
    
    return result + "\n🎉 Setup complete!"

def fix_common_error(error_description: str) -> str:
    error_lower = error_description.lower()
    
    if 'modulenotfounderror' in error_lower:
        import re
        match = re.search(r"no module named ['\"]([^'\"]+)['\"]", error_description, re.IGNORECASE)
        if match:
            module = match.group(1)
            try:
                subprocess.run(f'pip install {module}', shell=True, check=True, capture_output=True)
                return f"✅ Installed {module}"
            except:
                return f"❌ Failed to install {module}. Try: pip install {module}"
    
    elif 'port' in error_lower and 'in use' in error_lower:
        return "🔍 Port in use. Try different port or: lsof -ti:PORT | xargs kill -9"
    
    elif 'permission denied' in error_lower:
        return "🔒 Permission denied. Try: python3 instead of python, or use virtual environment"
    
    else:
        return f"🤔 Unknown error. Try googling: '{error_description[:50]}...'"

def main():
    if len(sys.argv) < 2:
        print("""🧅 ConnectOnion Developer Assistant

Usage: dev-assistant "what you want to do"

Examples:
• "save context - debugging login issue"
• "what was I working on?"
• "set up react project called my-app"
• "fix error: ModuleNotFoundError requests"
• "show all my projects"
""")
        return
    
    user_input = " ".join(sys.argv[1:])
    
    try:
        Agent = get_connectonion_agent()
        
        agent = Agent(
            name="dev_assistant",
            tools=[
                save_coding_context,
                recall_coding_context, 
                show_all_projects,
                setup_new_project,
                fix_common_error
            ],
            system_prompt="You are a helpful development assistant. Use the appropriate tools based on user requests."
        )
        
        response = agent.input(user_input)
        print(response)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
EOF

echo "🔨 Running PyInstaller..."

# Build with PyInstaller
pyinstaller \
    --onefile \
    --clean \
    --name=dev-assistant \
    --console \
    --noconfirm \
    dev_assistant_standalone.py

# Check if build succeeded
if [ -f "dist/dev-assistant" ] || [ -f "dist/dev-assistant.exe" ]; then
    echo "✅ Build successful!"
    
    # Get executable path
    if [ -f "dist/dev-assistant" ]; then
        EXECUTABLE="dist/dev-assistant"
    else
        EXECUTABLE="dist/dev-assistant.exe"
    fi
    
    # Show file size
    SIZE=$(du -h "$EXECUTABLE" | cut -f1)
    echo "📦 Executable: $EXECUTABLE ($SIZE)"
    
    # Make executable (Unix-like systems)
    if [ -f "dist/dev-assistant" ]; then
        chmod +x "dist/dev-assistant"
    fi
    
    # Test the executable
    echo "🧪 Testing executable..."
    "$EXECUTABLE" "help" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Test passed!"
    else
        echo "⚠️  Warning: Test failed, but executable was created"
    fi
    
    echo ""
    echo "🎉 Build complete!"
    echo "📁 Executable location: $EXECUTABLE"
    echo ""
    echo "Usage examples:"
    echo "  $EXECUTABLE \"save context - working on authentication\""
    echo "  $EXECUTABLE \"what was I working on?\""
    echo "  $EXECUTABLE \"set up new react project\""
    echo ""
    echo "Optional: Add to PATH:"
    echo "  sudo cp $EXECUTABLE /usr/local/bin/"
    
else
    echo "❌ Build failed!"
    echo "Check the output above for errors."
    exit 1
fi

# Cleanup
echo "🧹 Cleaning up..."
rm -f dev_assistant_standalone.py
rm -rf build __pycache__ *.spec

echo "✅ Done!"