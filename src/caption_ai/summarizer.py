"""Rolling summarizer loop."""

import asyncio
from datetime import datetime, timedelta

from caption_ai.bus import Segment, SegmentBus
from caption_ai.llm.router import get_llm_client
from caption_ai.prompts import build_rolling_summary_prompt
from caption_ai.storage import Storage
from caption_ai.config import config
from rich.console import Console

console = Console()


class Summarizer:
    """Rolling summarizer that processes segments and generates summaries."""

    def __init__(
        self,
        bus: SegmentBus,
        storage: Storage,
        summary_interval_seconds: int = 30,
    ) -> None:
        """Initialize summarizer."""
        self.bus = bus
        self.storage = storage
        self.summary_interval = summary_interval_seconds
        self.llm_client = get_llm_client(config.llm_provider)
        self.current_summary: str | None = None
        self.last_summary_time = datetime.now()

    async def run(self) -> None:
        """Run the summarizer loop."""
        console.print("[green]Summarizer started[/green]")
        accumulated_segments: list[Segment] = []

        while True:
            try:
                # Wait for segment with timeout
                try:
                    segment = await asyncio.wait_for(
                        self.bus.get(), timeout=1.0
                    )
                    accumulated_segments.append(segment)
                    await self.storage.append(segment)
                    self.bus.task_done()
                except asyncio.TimeoutError:
                    pass

                # Check if it's time to summarize
                now = datetime.now()
                if (
                    accumulated_segments
                    and (now - self.last_summary_time).total_seconds()
                    >= self.summary_interval
                ):
                    await self._summarize(accumulated_segments)
                    accumulated_segments.clear()
                    self.last_summary_time = now

            except KeyboardInterrupt:
                console.print("[yellow]Summarizer stopping...[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error in summarizer: {e}[/red]")
                await asyncio.sleep(1)

    async def _summarize(self, segments: list[Segment]) -> None:
        """Generate summary from accumulated segments."""
        if not segments:
            return

        console.print(
            f"[cyan]Summarizing {len(segments)} segments...[/cyan]"
        )
        prompt = build_rolling_summary_prompt(
            self.current_summary, segments
        )

        try:
            reply = await self.llm_client.complete(prompt)
            self.current_summary = reply.content
            console.print(f"[green]Summary:[/green] {reply.content}")
        except Exception as e:
            console.print(f"[red]LLM error: {e}[/red]")

