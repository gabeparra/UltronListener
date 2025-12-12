"""CLI entrypoint."""

import asyncio
from datetime import datetime, timedelta

from rich.console import Console

from caption_ai.bus import Segment, SegmentBus
from caption_ai.config import config
from caption_ai.storage import Storage
from caption_ai.summarizer import Summarizer

console = Console()


async def generate_fake_segments(bus: SegmentBus, count: int = 20) -> None:
    """Generate fake transcript segments for testing."""
    base_time = datetime.now()
    fake_segments = [
        ("Alice", "Let's start by reviewing the Q4 results."),
        ("Bob", "I've prepared the financial overview."),
        ("Alice", "Great, can you walk us through the key metrics?"),
        ("Bob", "Revenue is up 15% compared to last quarter."),
        ("Charlie", "That's excellent news. What about expenses?"),
        ("Bob", "Expenses are well controlled, only up 3%."),
        ("Alice", "So we're looking at a strong profit margin."),
        ("Charlie", "Yes, this positions us well for next year."),
        ("Alice", "Let's discuss the roadmap for Q1."),
        ("Bob", "I think we should focus on the new product launch."),
        ("Charlie", "Agreed, but we also need to address technical debt."),
        ("Alice", "Let's prioritize both. Bob, can you draft a plan?"),
        ("Bob", "I'll have something ready by Friday."),
        ("Alice", "Perfect. Any other items to discuss?"),
        ("Charlie", "I think we're good. Let's wrap up."),
        ("Alice", "Sounds good. Meeting adjourned."),
    ]

    for i, (speaker, text) in enumerate(fake_segments[:count]):
        segment = Segment(
            timestamp=base_time + timedelta(seconds=i * 3),
            text=text,
            speaker=speaker,
        )
        await bus.put(segment)
        console.print(
            f"[dim][{segment.timestamp.strftime('%H:%M:%S')}] "
            f"{speaker}: {text}[/dim]"
        )
        await asyncio.sleep(0.5)  # Simulate real-time arrival


async def main() -> None:
    """Main entrypoint."""
    console.print("[bold blue]Caption AI - Meeting Summarizer[/bold blue]")
    console.print(f"[dim]Using LLM provider: {config.llm_provider}[/dim]")

    # Initialize components
    bus = SegmentBus()
    storage = Storage()
    await storage.init()

    summarizer = Summarizer(bus, storage, summary_interval_seconds=15)

    # Start summarizer in background
    summarizer_task = asyncio.create_task(summarizer.run())

    # Generate fake segments
    await generate_fake_segments(bus, count=16)

    # Wait a bit for final summary
    await asyncio.sleep(5)

    # Stop summarizer
    summarizer_task.cancel()
    try:
        await summarizer_task
    except asyncio.CancelledError:
        pass

    console.print("[green]Done![/green]")


def cli() -> None:
    """CLI entrypoint."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()

