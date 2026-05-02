#!/usr/bin/env python3
"""
Entry point for the Productivity Agent.

Usage:
    python run.py --task "document my Python project" --path /path/to/project
    python run.py --task "write article about machine learning" --template markdown
"""

import argparse
import sys
import json
from orchestrator import orchestrate


def main():
    """Main entry point for the productivity agent."""
    parser = argparse.ArgumentParser(
        description="Productivity Agent - Automate code documentation and content creation"
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="The task to execute (e.g., 'document my Python project')"
    )
    parser.add_argument(
        "--path",
        type=str,
        default="./",
        help="Project path (for code tasks)"
    )
    parser.add_argument(
        "--template",
        type=str,
        default="markdown",
        help="Template format (for content tasks)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Prepare context
    context = {
        "project_path": args.path,
        "template": args.template,
        "verbose": args.verbose
    }
    
    try:
        if args.verbose:
            print(f"[*] Task: {args.task}")
            print(f"[*] Context: {json.dumps(context, indent=2)}")
        
        # Run the orchestrator
        result = orchestrate(args.task, context)
        
        if args.verbose:
            print("[*] Result:")
            print(json.dumps(result, indent=2, default=str))
        else:
            print(json.dumps(result, indent=2, default=str))
        
        return 0
    
    except Exception as e:
        print(f"[!] Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
