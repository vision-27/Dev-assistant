#!/usr/bin/env python3
"""
Simple Build Script for ConnectOnion Developer Assistant
Creates a standalone executable using PyInstaller

Usage: python build_executable.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    
    # Check ConnectOnion
    try:
        import connectonion
        print("✅ ConnectOnion found")
    except ImportError:
        print("❌ ConnectOnion not found. Install with: pip install connectonion")
        return False
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    print("✅ All requirements satisfied")
    return True

def create_main_script():
    """Create the main Python script for the executable"""
    
    script_content = '''#!/usr/bin/env python3
"""
ConnectOnion Developer Assistant - Standalone Version
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def check_connectonion():
    """Check if ConnectOnion is available"""
    try:
        from connectonion import Agent
        return Agent
    except ImportError:
        print("ERROR: ConnectOnion not found!")
        print("Please install: pip install connectonion")
        sys.exit(1)

# Storage setup
STORAGE_DIR = Path.home() / '.connectonion_dev_assistant'
STORAGE_DIR.mkdir(exist_ok=True)
CONTEXT_FILE = STORAGE_DIR / 'contexts.json'

def get_project_info():
    """Get current project information"""
    cwd = os.getcwd()
    project_name = os.path.basename(cwd)
    
    # Try to get git info
    try:
        repo_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        branch = subprocess.check_output(
            ['git', 'branch', '--show-current'], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        modified_files = subprocess.check_output(
            ['git', 'status', '--porcelain'], 
            stderr=subprocess.DEVNULL
        ).decode().strip().split('\\n')
        
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
    """Save current coding context"""
    project_info = get_project_info()
    
    # Load existing contexts
    contexts = {}
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, 'r') as f:
            contexts = json.load(f)
    
    project_name = project_info['project_name']
    if project_name not in contexts:
        contexts[project_name] = []
    
    # Add new context entry
    context_entry = {
        'timestamp': datetime.now().isoformat(),
        'description': description,
        'project_info': project_info
    }
    
    contexts[project_name].append(context_entry)
    contexts[project_name] = contexts[project_name][-10:]  # Keep last 10
    
    # Save to file
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(contexts, f, indent=2)
    
    return f"SAVED: Context for '{project_name}': {description}"

def recall_coding_context() -> str:
    """Recall most recent context for current project"""
    project_info = get_project_info()
    project_name = project_info['project_name']
    
    if not CONTEXT_FILE.exists():
        return "No saved contexts yet. Try: 'save context - what you're working on'"
    
    with open(CONTEXT_FILE, 'r') as f:
        contexts = json.load(f)
    
    if project_name not in contexts or not contexts[project_name]:
        return f"No saved context for '{project_name}'"
    
    last_context = contexts[project_name][-1]
    timestamp = datetime.fromisoformat(last_context['timestamp'])
    
    result = f"LAST CONTEXT for '{project_name}':\\n"
    result += f"Note: {last_context['description']}\\n"
    result += f"Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\\n"
    
    if last_context['project_info'].get('branch'):
        result += f"Branch: {last_context['project_info']['branch']}\\n"
    
    return result

def show_all_projects() -> str:
    """Show all tracked projects"""
    if not CONTEXT_FILE.exists():
        return "No projects tracked yet!"
    
    with open(CONTEXT_FILE, 'r') as f:
        contexts = json.load(f)
    
    if not contexts:
        return "No projects tracked yet!"
    
    result = "ALL TRACKED PROJECTS:\\n\\n"
    
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
        
        result += f"PROJECT: {project_name}\\n"
        result += f"  Note: {last_ctx['description'][:60]}...\\n"
        result += f"  Time: {time_str}\\n\\n"
    
    return result

def setup_new_project(project_type: str, project_name: str = "") -> str:
    """Set up new project"""
    templates = {
        'react': {
            'desc': 'React + TypeScript + Vite',
            'cmds': [
                f'npm create vite@latest {project_name or "."} -- --template react-ts',
                'npm install'
            ]
        },
        'python': {
            'desc': 'Python + FastAPI',
            'cmds': [
                'python -m venv venv',
                '. venv/bin/activate && pip install fastapi uvicorn'
            ]
        },
        'vue': {
            'desc': 'Vue 3 + TypeScript',
            'cmds': [
                f'npm create vue@latest {project_name or "."}',
                'npm install'
            ]
        }
    }
    
    if project_type not in templates:
        return f"ERROR: Unknown type. Available: {', '.join(templates.keys())}"
    
    template = templates[project_type]
    result = f"SETTING UP: {template['desc']}\\n"
    
    if project_name:
        try:
            os.makedirs(project_name, exist_ok=True)
            os.chdir(project_name)
            result += f"Created directory: {project_name}\\n"
        except Exception as e:
            return f"ERROR: Failed to create directory: {e}"
    
    for i, cmd in enumerate(template['cmds'], 1):
        result += f"[{i}/{len(template['cmds'])}] {cmd}\\n"
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            result += "SUCCESS\\n"
        except subprocess.CalledProcessError:
            result += "FAILED\\n"
            break
    
    return result + "\\nSETUP COMPLETE!"

def fix_common_error(error_description: str) -> str:
    """Fix common development errors"""
    error_lower = error_description.lower()
    
    # Python module not found
    if 'modulenotfounderror' in error_lower or 'no module named' in error_lower:
        import re
        # Simple pattern - just capture word characters after "no module named"
        match = re.search(r"no module named.+?([a-zA-Z_][a-zA-Z0-9_]*)", error_description, re.IGNORECASE)
        if match:
            module = match.group(1)
            
            # Common package mappings
            mappings = {
                'cv2': 'opencv-python',
                'PIL': 'Pillow', 
                'sklearn': 'scikit-learn',
                'yaml': 'PyYAML'
            }
            
            package = mappings.get(module, module)
            
            try:
                subprocess.run(f'pip install {package}', shell=True, check=True, capture_output=True)
                return f"SUCCESS: Installed {package} for module '{module}'"
            except:
                return f"ERROR: Failed to install {package}. Try: pip install {package}"
    
    # Port in use
    elif 'port' in error_lower and 'in use' in error_lower:
        return """Port in use error detected.
        
Quick fixes:
- Change port in your app
- Kill process: lsof -ti:PORT | xargs kill -9
- Find what's using port: lsof -i :PORT"""
    
    # Permission denied
    elif 'permission denied' in error_lower:
        return """Permission denied error detected.
        
Quick fixes:
- Use virtual environment
- Try python3 instead of python
- Check file permissions: ls -la
- Use --user flag: pip install --user"""
    
    else:
        return f"Unknown error. For: '{error_description[:50]}...', try googling the exact error message"

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("""ConnectOnion Developer Assistant

Usage: dev-assistant "what you want to do"

Examples:
- "save context - debugging login issue"  
- "what was I working on?"
- "set up react project called my-app"
- "fix error: ModuleNotFoundError requests"
- "show all projects"
""")
        return
    
    user_input = " ".join(sys.argv[1:])
    
    try:
        # Import ConnectOnion agent
        Agent = check_connectonion()
        
        # Create agent with tools
        agent = Agent(
            name="dev_assistant",
            tools=[
                save_coding_context,
                recall_coding_context,
                show_all_projects, 
                setup_new_project,
                fix_common_error
            ],
            system_prompt="""You are a helpful development assistant. You can:
1. Save/recall coding context using save_coding_context() and recall_coding_context()
2. Show all projects with show_all_projects()
3. Set up new projects with setup_new_project()  
4. Fix errors with fix_common_error()

Be conversational and call the right function based on what the user needs."""
        )
        
        # Process user input
        response = agent.input(user_input)
        print(response)
        
    except KeyboardInterrupt:
        print("\\nGoodbye!")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
'''
    
    # Write the script to file with UTF-8 encoding
    script_path = 'dev_assistant_main.py'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✅ Created main script: {script_path}")
    return script_path

def build_executable(script_path):
    """Build executable using PyInstaller"""
    print("🔨 Building executable with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                 # Single file
        '--clean',                   # Clean cache  
        '--name=dev-assistant',      # Output name
        '--console',                 # Console app
        '--noconfirm',               # Don't ask for confirmation
        script_path
    ]
    
    try:
        # Run PyInstaller
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            
            # Check for executable
            exe_path = Path('dist') / 'dev-assistant'
            if not exe_path.exists():
                exe_path = Path('dist') / 'dev-assistant.exe'  # Windows
            
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 Executable: {exe_path}")
                print(f"📊 Size: {size_mb:.1f} MB")
                
                # Make executable on Unix
                if exe_path.suffix != '.exe':
                    exe_path.chmod(0o755)
                
                return True
            else:
                print("❌ Executable not found in dist/")
                return False
        else:
            print("❌ PyInstaller failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def cleanup():
    """Clean up build artifacts"""
    print("🧹 Cleaning up...")
    
    # Remove temporary files
    cleanup_items = [
        'dev_assistant_main.py',
        'build',
        '__pycache__',
        '*.spec'
    ]
    
    for item in cleanup_items:
        if '*' in item:
            # Handle wildcards
            import glob
            for file in glob.glob(item):
                try:
                    os.remove(file)
                    print(f"  Removed: {file}")
                except:
                    pass
        else:
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    print(f"  Removed: {item}")
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"  Removed: {item}/")
            except:
                pass

def main():
    """Main build process"""
    print("🧅 ConnectOnion Developer Assistant - Build Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("❌ Please install missing requirements and try again")
        return False
    
    # Create main script
    try:
        script_path = create_main_script()
    except Exception as e:
        print(f"❌ Failed to create script: {e}")
        return False
    
    # Build executable
    success = build_executable(script_path)
    
    # Cleanup
    cleanup()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 Build complete!")
        print("📁 Check the 'dist/' directory for your executable")
        print("\nUsage examples:")
        print('  ./dist/dev-assistant "save context - working on login"')
        print('  ./dist/dev-assistant "what was I working on?"')
        print('  ./dist/dev-assistant "set up new react project"')
        print("\nOptional: Add to PATH")
        print("  sudo cp dist/dev-assistant /usr/local/bin/")
    else:
        print("\n❌ Build failed. Check errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)