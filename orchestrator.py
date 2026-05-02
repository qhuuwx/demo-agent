import anthropic
import json
import yaml
from pathlib import Path
from pipelines.code_pipeline import run_code_pipeline
from pipelines.content_pipeline import run_content_pipeline


client = anthropic.Anthropic()


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


CONFIG = load_config()


def orchestrate(task: str, context: dict):
    """
    Claude Code decides which pipeline to invoke.
    
    Args:
        task: The task description
        context: Additional context (project_path, template, etc.)
    
    Returns:
        Pipeline execution result
    """
    try:
        # Use Claude to decide which pipeline
        response = client.messages.create(
            model=CONFIG.get('claude', {}).get('model', 'claude-opus-4-5'),
            max_tokens=512,
            system="""You are a task orchestrator. Analyze the task and context, then return a JSON response.

Return JSON in this exact format:
{
    "pipeline": "code" | "content",
    "reasoning": "brief explanation",
    "args": {
        "key": "value"
    }
}

- Use "code" pipeline for: documentation, linting, code analysis, refactoring
- Use "content" pipeline for: writing, research, articles, blog posts""",
            messages=[
                {
                    "role": "user",
                    "content": f"""Task: {task}

Context: {json.dumps(context, indent=2)}"""
                }
            ]
        )
        
        decision = json.loads(response.content[0].text)
        
        if not isinstance(decision, dict) or 'pipeline' not in decision:
            raise ValueError("Invalid orchestration decision format")
        
        # Extract args from decision, fallback to context
        args = decision.get('args', {})
        
        # Merge with context for common args
        if decision['pipeline'] == 'code':
            args['project_path'] = args.get('project_path') or context.get('project_path', './')
            return run_code_pipeline(**args)
        
        elif decision['pipeline'] == 'content':
            args['topic'] = args.get('topic') or task
            args['template'] = args.get('template') or context.get('template', 'markdown')
            return run_content_pipeline(**args)
        
        else:
            return {"error": f"Unknown pipeline: {decision['pipeline']}"}
    
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse orchestration response: {str(e)}"}
    except Exception as e:
        return {"error": f"Orchestration failed: {str(e)}", "type": type(e).__name__}
