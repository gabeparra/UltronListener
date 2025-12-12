"""Prompt templates for rolling summaries."""

from typing import Sequence

from caption_ai.bus import Segment


def build_rolling_summary_prompt(
    previous_summary: str | None,
    new_segments: Sequence[Segment],
) -> str:
    """Build a prompt for rolling summary generation."""
    segments_text = "\n".join(
        f"[{seg.timestamp.strftime('%H:%M:%S')}] {seg.speaker or 'Speaker'}: {seg.text}"
        for seg in new_segments
    )

    if previous_summary:
        prompt = f"""You are summarizing a meeting transcript. Here is the previous summary:

{previous_summary}

And here are new transcript segments:

{segments_text}

Please provide an updated summary that incorporates the new information while maintaining context from the previous summary. Keep it concise and focused on key points."""
    else:
        prompt = f"""You are summarizing a meeting transcript. Here are the initial segments:

{segments_text}

Please provide a concise summary focusing on key points and decisions."""

    return prompt

