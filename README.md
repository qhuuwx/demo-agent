# Productivity Agent

An intelligent Claude-powered agent that automates code documentation and content creation through a pipeline architecture.

## Features

- **Code Pipeline**: Automatically generates docstrings, README files, and validates code against lint rules
- **Content Pipeline**: Researches topics, drafts content, and reviews/reformats to match templates
- **Intelligent Orchestration**: Claude decides which pipeline best suits each task
- **Retry Loop**: Code pipeline automatically fixes issues and retries up to 3 times
- **Modular Tools**: Reusable file and shell execution tools

## Architecture

```
productivity-agent/
├── orchestrator.py        # Main Claude decision-maker
├── pipelines/
│   ├── code_pipeline.py   # Scanner → Doc gen → Lint loop
│   └── content_pipeline.py # Research → Draft → Review loop
├── tools/
│   ├── file_tools.py      # Read/write/list files
│   └── shell_tools.py     # Execute commands, run linters/tests
├── config.yaml            # Configuration (thresholds, templates, paths)
├── run.py                 # CLI entry point
└── requirements.txt       # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd productivity-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### Command Line

Document a Python project:
```bash
python run.py --task "document my Python project" --path ./my_project --verbose
```

Write content about a topic:
```bash
python run.py --task "write an article about machine learning best practices" --template markdown
```

### Programmatic Usage

```python
from orchestrator import orchestrate

task = "Generate comprehensive documentation for my Python project"
context = {
    "project_path": "./my_project",
    "template": "markdown"
}

result = orchestrate(task, context)
print(result)
```

## Configuration

Edit `config.yaml` to customize:

- **Code Pipeline**: Max retries, lint tool, file patterns
- **Content Pipeline**: Research depth, output format
- **Claude Model**: Model selection, token limits
- **Paths**: Output directories, log locations

## Pipeline Details

### Code Pipeline

1. **Scan**: Discovers Python files in the project
2. **Generate Docs**: Claude creates docstrings and README
3. **Write**: Files updated with new documentation
4. **Lint**: Ruff checks for code style issues
5. **Fix & Retry**: If lint fails, Claude fixes docs and retries (up to 3 times)

### Content Pipeline

1. **Research**: Claude gathers key points on the topic
2. **Draft**: Claude writes structured content using research
3. **Review & Reformat**: Claude reviews for clarity and applies template

## API Keys

The agent uses the Anthropic API. Set your API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Or create a `.env` file with:
```
ANTHROPIC_API_KEY=your-key-here
```

## Tools

### File Tools (`tools/file_tools.py`)
- `read_file()`: Read file contents
- `write_file()`: Write/create files
- `append_file()`: Append to files
- `list_files()`: List files with filtering
- `file_exists()`: Check file existence
- `create_directory()`: Create directories

### Shell Tools (`tools/shell_tools.py`)
- `run_command()`: Execute shell commands
- `run_linter()`: Run linting tools (default: ruff)
- `run_tests()`: Run test suites

## Examples

### Example 1: Document a Project

```bash
python run.py --task "Create comprehensive documentation for my Python library" \
  --path ./src \
  --verbose
```

### Example 2: Generate Blog Post

```bash
python run.py --task "Write a beginner-friendly blog post about Docker containerization" \
  --template markdown
```

### Example 3: Code Review Notes

```bash
python run.py --task "Generate code review documentation highlighting best practices" \
  --path ./app
```

## Troubleshooting

**Issue**: "No API key found"
- **Solution**: Set ANTHROPIC_API_KEY environment variable or .env file

**Issue**: Lint failures persist after retries
- **Solution**: Check config.yaml for compatible linter settings, examine lint output

**Issue**: Module import errors
- **Solution**: Ensure you've run `pip install -r requirements.txt`

## Performance Tips

1. Keep project sizes reasonable (limit to key files)
2. Configure `include_patterns` in config.yaml to focus on specific file types
3. Adjust `max_tokens` settings based on your needs
4. Use `--verbose` flag to monitor progress

## Contributing

Contributions welcome! Areas for enhancement:
- Additional pipeline types (testing, deployment)
- More sophisticated error recovery
- Batch processing multiple projects
- Integration with version control systems

## License

MIT
