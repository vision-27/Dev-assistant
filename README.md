# OnionDev

A powerful AI-powered developer tool that helps with context management, project setup, and error recovery.

## 🚀 Quick Setup

### Step 1: Prerequisites
```bash
# Install Python 3.8+ if not already installed
# Install ConnectOnion framework
pip install connectonion

# Install PyInstaller for building
pip install pyinstaller
```

### Step 2: Build the Executable
```bash
# Download the build script
curl -o build.sh https://raw.githubusercontent.com/vision-27/OnionDev/refs/heads/main/build.sh
chmod +x build.sh

# Run the build
./build.sh
```

**Or manually:**
```bash
# Copy the build_executable.py script and run:
python build_executable.py
```

### Step 3: Use Your New Tool!
```bash
# The executable will be in dist/
./dist/dev-assistant "help me code!"

# Or copy to PATH for system-wide access:
sudo cp dist/dev-assistant /usr/local/bin/
dev-assistant "save my context - working on login bug"
```

## 💡 Usage Examples

### Context Management
```bash
# Save what you're working on
dev-assistant "save context - debugging user authentication, session timeout issue"

# Later, recall your context
dev-assistant "what was I working on last time?"

# See all your projects
dev-assistant "show me all my tracked projects"
```

### Project Setup
```bash
# Set up new React project
dev-assistant "create a new react project called my-dashboard"

# Python FastAPI project
dev-assistant "set up a python api project"

# In current directory
dev-assistant "initialize a react app here"
```

### Error Recovery
```bash
# Fix Python import errors
dev-assistant "fix this error: ModuleNotFoundError: No module named 'pandas'"

# Port conflicts
dev-assistant "fix: port 3000 already in use"

# Permission issues
dev-assistant "help with permission denied error"
```

## 🎯 Natural Language Interface

The tool understands natural language, so you can ask for help in many ways:

```bash
# These all work:
dev-assistant "I need to save my progress on this feature"
dev-assistant "remember that I'm working on the login system"
dev-assistant "what project was I coding yesterday?"
dev-assistant "help me set up a new vue app"
dev-assistant "my python script can't find the requests module"
```

## 📁 File Structure

After building, you'll have:
```
your-project/
├── dist/
│   └── dev-assistant          # Your standalone executable
├── dev-assistant-distribution/
│   ├── dev-assistant          # Copy of executable
│   ├── README.md             # User documentation
│   └── install.sh            # Simple installer
```

## 🌟 Features

- **🧠 Smart Context Tracking**: Never lose track of what you were working on
- **🚀 Instant Project Setup**: Zero-config setup for React, Python, Vue, Node.js
- **🛠️ Auto Error Recovery**: Automatically fix common development errors
- **💬 Natural Language**: Just describe what you need in plain English
- **📦 Standalone**: No dependencies after building (except ConnectOnion)
- **🔒 Privacy**: All data stored locally in `~/.connectonion_dev_assistant/`

## 🔧 Advanced Usage

### Environment Variables
```bash
# Set custom storage location
export CONNECTONION_STORAGE=~/my-dev-contexts

# Set preferred package manager
export CONNECTONION_PKG_MANAGER=yarn
```

### Integration with Shell
```bash
# Add alias to your .bashrc/.zshrc
alias da='dev-assistant'
alias save-context='dev-assistant "save context -"'

# Now you can use:
da "what was I working on?"
save-context "debugging oauth integration"
```

### Custom Installation Script
```bash
#!/bin/bash
# install-dev-assistant.sh

echo "Installing ConnectOnion Developer Assistant..."

# Install ConnectOnion if not present
pip install connectonion

# Download and build
curl -o build.sh https://raw.githubusercontent.com/your-repo/build.sh
chmod +x build.sh && ./build.sh

# Install to PATH
sudo cp dist/dev-assistant /usr/local/bin/
echo "✅ Installed! Try: dev-assistant 'hello world'"
```

## 🐛 Troubleshooting

### Build Issues
```bash
# If PyInstaller fails
pip install --upgrade pyinstaller setuptools

# If ConnectOnion import fails
pip install --upgrade connectonion

# Clean build
rm -rf build dist *.spec && python build_executable.py
```

### Runtime Issues
```bash
# If "ConnectOnion not found"
pip install connectonion

# If git commands fail
# Install git or use in non-git directories

# If permission denied
chmod +x dev-assistant
```

### Common Build Errors

1. **"ModuleNotFoundError: connectonion"**
   ```bash
   pip install connectonion
   ```

2. **"PyInstaller command not found"**
   ```bash
   pip install pyinstaller
   ```

3. **"Executable too large"**
   - Normal! The executable includes Python runtime (~50-100MB)
   - Use `pyinstaller --exclude-module matplotlib` to reduce size

## 📊 Distribution

### For End Users (No Python Required)
```bash
# Just download and run the executable
curl -L -o dev-assistant https://github.com/your-repo/releases/latest/dev-assistant
chmod +x dev-assistant
./dev-assistant "help me code!"
```

### For Developers
```bash
# Clone and build yourself
git clone https://github.com/your-repo/connectonion-dev-assistant
cd connectonion-dev-assistant
./build.sh
```

## 🚀 What Makes This Special

1. **Actually uses ConnectOnion properly** - Single agent, multiple tools
2. **Standalone executable** - Users don't need Python installed
3. **Natural language interface** - No complex CLI syntax
4. **Solves real problems** - Context switching, project setup, error recovery
5. **Privacy-focused** - All data stays local
6. **Cross-platform** - Works on Windows, Mac, Linux

## 🎉 Success!

You now have a powerful, standalone developer assistant that:
- Remembers your coding context across sessions
- Sets up new projects instantly
- Fixes common errors automatically
- Understands natural language commands
- Requires no installation for end users

Share the executable with your team, or distribute it to help other developers be more productive!
