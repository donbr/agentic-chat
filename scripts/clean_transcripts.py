#!/usr/bin/env python3
"""
Clean VTT transcript files by removing duplicates, inline tags, and formatting issues.
Outputs clean markdown files suitable for documentation and study guides.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class SubtitleBlock:
    """Represents a single subtitle block from VTT file"""
    start_time: str
    end_time: str
    text: str
    start_seconds: float
    end_seconds: float


def time_to_seconds(time_str: str) -> float:
    """Convert VTT timestamp to seconds"""
    parts = time_str.split(':')
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_time(seconds: float) -> str:
    """Convert seconds back to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def parse_vtt_file(file_path: Path) -> List[SubtitleBlock]:
    """Parse VTT file and extract subtitle blocks"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into blocks by double newline
    blocks = content.split('\n\n')

    subtitle_blocks = []
    timestamp_pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})'

    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue

        # Find timestamp line
        timestamp_match = None
        text_lines = []

        for i, line in enumerate(lines):
            match = re.search(timestamp_pattern, line)
            if match:
                timestamp_match = match
                # Collect all lines after timestamp that aren't metadata
                for j in range(i + 1, len(lines)):
                    if not lines[j].strip().endswith('position:0%'):
                        text_lines.append(lines[j])
                break

        if timestamp_match and text_lines:
            start_time = timestamp_match.group(1)
            end_time = timestamp_match.group(2)

            # Join text lines and clean
            text = ' '.join(text_lines)

            # Skip empty blocks
            if text.strip():
                subtitle_blocks.append(SubtitleBlock(
                    start_time=start_time,
                    end_time=end_time,
                    text=text,
                    start_seconds=time_to_seconds(start_time),
                    end_seconds=time_to_seconds(end_time)
                ))

    return subtitle_blocks


def clean_text(text: str) -> str:
    """Remove inline timestamp and formatting tags from text"""
    # Remove timestamp tags like <00:00:01.120>
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)

    # Remove color/style tags like <c> and </c>
    text = re.sub(r'</?c>', '', text)

    # Remove other HTML-like tags
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def deduplicate_blocks(blocks: List[SubtitleBlock]) -> List[SubtitleBlock]:
    """Remove duplicate text blocks, keeping the first occurrence"""
    seen_texts = set()
    unique_blocks = []

    for block in blocks:
        cleaned_text = clean_text(block.text)

        # Skip if we've seen this exact text before
        if cleaned_text in seen_texts:
            continue

        # Also check for partial overlaps (common in VTT)
        is_duplicate = False
        for seen in seen_texts:
            if len(cleaned_text) > 10 and len(seen) > 10:
                # Check if one text contains the other (with some tolerance)
                if cleaned_text in seen or seen in cleaned_text:
                    # If the new text is longer, replace
                    if len(cleaned_text) > len(seen):
                        seen_texts.remove(seen)
                        seen_texts.add(cleaned_text)
                        # Find and update the block
                        for i, ub in enumerate(unique_blocks):
                            if clean_text(ub.text) == seen:
                                unique_blocks[i] = SubtitleBlock(
                                    start_time=block.start_time,
                                    end_time=block.end_time,
                                    text=cleaned_text,
                                    start_seconds=block.start_seconds,
                                    end_seconds=block.end_seconds
                                )
                                break
                    is_duplicate = True
                    break

        if not is_duplicate:
            seen_texts.add(cleaned_text)
            block.text = cleaned_text
            unique_blocks.append(block)

    return unique_blocks


def group_into_paragraphs(blocks: List[SubtitleBlock], window_seconds: float = 30) -> List[Tuple[str, str, str]]:
    """Group subtitle blocks into logical paragraphs based on time windows"""
    if not blocks:
        return []

    paragraphs = []
    current_paragraph = []
    paragraph_start = blocks[0].start_seconds
    paragraph_start_time = blocks[0].start_time

    for block in blocks:
        # Check if we should start a new paragraph
        if block.start_seconds - paragraph_start > window_seconds and current_paragraph:
            # Save current paragraph
            end_time = current_paragraph[-1].end_time
            text = ' '.join([b.text for b in current_paragraph])
            paragraphs.append((
                seconds_to_time(paragraph_start),
                seconds_to_time(current_paragraph[-1].end_seconds),
                text
            ))

            # Start new paragraph
            current_paragraph = [block]
            paragraph_start = block.start_seconds
            paragraph_start_time = block.start_time
        else:
            current_paragraph.append(block)

    # Don't forget the last paragraph
    if current_paragraph:
        text = ' '.join([b.text for b in current_paragraph])
        paragraphs.append((
            seconds_to_time(paragraph_start),
            seconds_to_time(current_paragraph[-1].end_seconds),
            text
        ))

    return paragraphs


def create_markdown_output(paragraphs: List[Tuple[str, str, str]], title: str) -> str:
    """Create markdown formatted output"""
    lines = [f"# {title}\n"]

    for start, end, text in paragraphs:
        lines.append(f"\n## [{start} - {end}]\n")
        lines.append(f"{text}\n")

    return '\n'.join(lines)


def process_transcript(input_path: Path, output_path: Path, title: str) -> Dict:
    """Process a single transcript file"""
    print(f"Processing {input_path.name}...")

    # Parse VTT file
    blocks = parse_vtt_file(input_path)
    original_count = len(blocks)

    # Clean and deduplicate
    unique_blocks = deduplicate_blocks(blocks)
    unique_count = len(unique_blocks)

    # Group into paragraphs
    paragraphs = group_into_paragraphs(unique_blocks)

    # Create markdown output
    markdown = create_markdown_output(paragraphs, title)

    # Save to file
    output_path.write_text(markdown, encoding='utf-8')

    # Calculate statistics
    original_size = input_path.stat().st_size
    output_size = output_path.stat().st_size
    reduction_pct = ((original_size - output_size) / original_size) * 100

    stats = {
        'file': input_path.name,
        'original_blocks': original_count,
        'unique_blocks': unique_count,
        'paragraphs': len(paragraphs),
        'original_size_kb': round(original_size / 1024, 2),
        'output_size_kb': round(output_size / 1024, 2),
        'reduction_percent': round(reduction_pct, 1)
    }

    print(f"  - Blocks: {original_count} -> {unique_count} unique")
    print(f"  - Size: {stats['original_size_kb']}KB -> {stats['output_size_kb']}KB ({stats['reduction_percent']}% reduction)")
    print(f"  - Output: {len(paragraphs)} paragraphs")

    return stats


def main():
    """Process all transcript files"""
    base_dir = Path('transcripts')
    raw_dir = base_dir / 'raw'
    cleaned_dir = base_dir / 'cleaned'

    # Ensure directories exist
    cleaned_dir.mkdir(exist_ok=True)

    # Define transcript files and their titles
    transcripts = [
        ('part1_OkqnAk1eH4M.en.vtt', 'Part 1: Prompting & Responses API', 'part1_clean.md'),
        ('part2_BAtY88cw3rw.en.vtt', 'Part 2: RAG & Connectors', 'part2_clean.md'),
        ('part3_qQ6nCN6ynXo.en.vtt', 'Part 3: Agentic Search & Agents SDK', 'part3_clean.md'),
        ('part4_t13Y5Igh66U.en.vtt', 'Part 4: Vibe-Coding & Deployment', 'part4_clean.md'),
    ]

    all_stats = []
    all_paragraphs = []

    for vtt_file, title, md_file in transcripts:
        input_path = raw_dir / vtt_file
        output_path = cleaned_dir / md_file

        if input_path.exists():
            stats = process_transcript(input_path, output_path, title)
            all_stats.append(stats)

            # Collect paragraphs for combined file
            blocks = parse_vtt_file(input_path)
            unique_blocks = deduplicate_blocks(blocks)
            paragraphs = group_into_paragraphs(unique_blocks)
            all_paragraphs.append((title, paragraphs))
        else:
            print(f"Warning: {input_path} not found")

    # Create combined transcript
    if all_paragraphs:
        print("\nCreating combined transcript...")
        combined_path = cleaned_dir / 'full_transcript.md'

        lines = ["# How to Build ChatGPT - Complete Transcript\n"]
        for title, paragraphs in all_paragraphs:
            lines.append(f"\n---\n\n# {title}\n")
            for start, end, text in paragraphs:
                lines.append(f"\n## [{start} - {end}]\n")
                lines.append(f"{text}\n")

        combined_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"  - Saved to {combined_path}")

    # Save metadata
    metadata = {
        'processed_files': all_stats,
        'total_files': len(all_stats),
        'total_original_size_kb': sum(s['original_size_kb'] for s in all_stats),
        'total_output_size_kb': sum(s['output_size_kb'] for s in all_stats),
        'average_reduction_percent': round(sum(s['reduction_percent'] for s in all_stats) / len(all_stats), 1) if all_stats else 0
    }

    metadata_path = base_dir / 'metadata.json'
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

    print(f"\nProcessing complete!")
    print(f"  - Processed {metadata['total_files']} files")
    print(f"  - Total size: {metadata['total_original_size_kb']}KB -> {metadata['total_output_size_kb']}KB")
    print(f"  - Average reduction: {metadata['average_reduction_percent']}%")
    print(f"  - Metadata saved to {metadata_path}")


if __name__ == '__main__':
    main()