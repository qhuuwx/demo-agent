import anthropic

client = anthropic.Anthropic()

def run_content_pipeline(topic: str, template: str):
    # Step 1: Research
    research = client.messages.create(
        model="claude-opus-4-5", max_tokens=2048,
        messages=[{"role": "user", "content": f"Research key points on: {topic}"}]
    ).content[0].text

    # Step 2: Draft
    draft = client.messages.create(
        model="claude-opus-4-5", max_tokens=2048,
        messages=[{"role": "user", "content": f"Write structured content about {topic} using: {research}"}]
    ).content[0].text

    # Step 3: Self-review + reformat
    final = client.messages.create(
        model="claude-opus-4-5", max_tokens=2048,
        messages=[{"role": "user", "content": f"Review this for clarity, then reformat to match template:\n{draft}\n\nTemplate:\n{template}"}]
    ).content[0].text

    return {"output": final, "topic": topic}