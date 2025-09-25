# How to Build ChatGPT: Educational Content Generator

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MCP Integration](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io/)
[![YouTube Transcripts](https://img.shields.io/badge/YouTube-Transcript%20Processing-red.svg)](https://youtube.com/)
[![Educational Content](https://img.shields.io/badge/Content-Educational-purple.svg)](https://www.aimakerspace.com/)
[![AI Engineering](https://img.shields.io/badge/AI-Engineering-orange.svg)](https://github.com/AI-Maker-Space)
[![Mermaid Diagrams](https://img.shields.io/badge/Diagrams-Mermaid-ff69b4.svg)](https://mermaid-js.github.io/mermaid/)

An AI-powered educational content generation system that transforms video tutorials into comprehensive study guides and technical walkthroughs. Built specifically for the **AI Makerspace "How to Build ChatGPT"** series, this project demonstrates modern AI engineering practices including video transcript processing, structured content generation, and automated documentation.

## Overview

This project addresses a common challenge in AI education: converting rich video content into structured, searchable, and comprehensive learning materials. Using Model Context Protocol (MCP) integration and advanced content processing, it generates:

- **Detailed Study Guides** - Complete learning paths with prerequisites, objectives, and technical insights
- **Code Walkthroughs** - Architectural analysis and technical commentary on implementation patterns
- **Visual Diagrams** - Mermaid-based architecture and workflow visualizations
- **Transcript Integration** - Seamless access to video content with proper citations

## Key Features

- **MCP Integration** - Uses Model Context Protocol for YouTube transcript access
- **Multi-format Output** - Generates Markdown documentation with embedded diagrams
- **Source Attribution** - Comprehensive citation system linking back to original videos
- **Automated Processing** - YAML-defined task system for reproducible content generation
- **Quality Assurance** - Built-in validation and gap identification
- **Professional Formatting** - LinkedIn-ready content with proper structure and presentation

## Generated Content Structure

```
outputs/
├── documents/           # Main educational content
│   ├── study_guide.md          # Complete study guide (464 lines)
│   └── code_walkthrough.md     # Technical analysis (497 lines)
├── diagrams/           # Visual documentation
│   ├── study_guide_concept.md  # Study guide concept map (Mermaid)
│   ├── code_walkthrough_arch.md # Repository architecture (Mermaid)
│   ├── runner_tasks.md         # Workflow diagrams (Mermaid)
│   └── e2e_sequence.md         # End-to-end sequence diagrams (Mermaid)
└── documentation/      # Supporting documentation
    └── mcp-setup.md            # MCP configuration guide
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) for dependency management
- Access to YouTube videos (for transcript processing)

### Installation

```bash
# Clone the repository
git clone https://github.com/donbr/agentic-chat
cd agentic-chat

# Set up virtual environment
uv venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -e .

# Set up MCP configuration (for transcript access)
cp .mcp.json.example .mcp.json
# See outputs/documentation/mcp-setup.md for detailed MCP configuration instructions
```

### Basic Usage

```bash
# View generated content
ls -la outputs/

# Check content quality
wc -l outputs/documents/*
grep -c "\*(\[Part" outputs/documents/study_guide.md

# Browse generated content directly
ls -la outputs/documents/  # Main study guides and walkthroughs
ls -la outputs/diagrams/   # Mermaid diagrams and visualizations

# Use Makefile for common tasks
make check             # Quality checks
make docs              # Validate documentation
```

### Content Examples

```bash
# Read the main deliverables
cat outputs/documents/study_guide.md
cat outputs/documents/code_walkthrough.md

# View Mermaid diagrams
ls -la outputs/diagrams/
```

### Advanced Usage

For transcript processing capabilities:

```bash
# Download video transcripts (if needed)
python scripts/download_transcripts.py

# Validate all deliverables
ls -la outputs/ transcripts/
```

## Content Overview

### Study Guide Features
- **Learning Path Structure** - Progressive curriculum from basics to production
- **Technical Deep-dives** - OpenAI Responses API, RAG systems, Agent architectures
- **Video Integration** - Direct citations with timestamps and URL references
- **Implementation Examples** - Minimal, runnable code fragments
- **Next Steps Planning** - Advanced topics and production considerations

### Code Walkthrough Features
- **Architectural Analysis** - Multi-branch repository structure examination
- **Technical Commentary** - Line-by-line code analysis with video context
- **Production Patterns** - Real-world implementation insights
- **Gap Identification** - Explicit documentation of enhancement opportunities
- **Visual Diagrams** - Mermaid-based architecture and flow diagrams

## Technical Architecture

### Core Components

1. **Task Definition System** (`ai-tasks.yaml`)
   - YAML-based configuration for content generation tasks
   - Structured input/output specifications
   - Quality guardrails and validation rules

2. **Transcript Processing** (`download_transcripts.py`)
   - YouTube video transcript extraction using yt-dlp
   - VTT format processing and organization
   - Backup content access for offline processing

3. **MCP Integration** (`.mcp.json`)
   - Model Context Protocol configuration
   - YouTube transcript and GitHub repository access
   - Environment-based authentication

4. **Content Generation**
   - AI-powered analysis of video and code content
   - Structured markdown generation with citations
   - Mermaid diagram creation and validation

### Project Structure

```
agentic-chat/
├── README.md              # Project documentation
├── LICENSE                # MIT license
├── pyproject.toml         # Python project configuration
├── Makefile              # Development commands
├── ai-tasks.yaml         # Task definitions and metadata
├── src/agentic_chat/     # Package source code
├── scripts/              # Utility scripts
│   └── download_transcripts.py
├── outputs/              # All generated content
│   ├── documents/        # Main deliverables
│   │   ├── study_guide.md
│   │   └── code_walkthrough.md
│   ├── diagrams/         # Mermaid diagrams
│   │   ├── study_guide_concept.md
│   │   ├── code_walkthrough_arch.md
│   │   ├── runner_tasks.md
│   │   └── e2e_sequence.md
│   └── documentation/    # Supporting docs
│       └── mcp-setup.md
└── transcripts/          # Video transcripts (gitignored)
```

### Technology Stack

- **Python 3.11+** - Core application runtime
- **yt-dlp** - YouTube transcript extraction
- **MCP Protocol** - AI tool integration
- **YAML** - Configuration and task definition
- **Markdown + Mermaid** - Documentation and visualization

## Educational Value

This project demonstrates several modern AI engineering concepts:

- **Content Processing Pipelines** - Automated transformation of multimedia content
- **Model Context Protocol** - Standard integration patterns for AI tools
- **Structured Output Generation** - Reliable, formatted content creation
- **Citation and Attribution** - Academic-quality source tracking
- **Quality Assurance** - Validation and gap identification in AI-generated content

## Contributing

We welcome contributions! Please see our [contribution guidelines](CONTRIBUTING.md) for details on:

- Code style and standards
- Documentation requirements
- Testing procedures
- Pull request process

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Attribution

This project is built upon the excellent educational content from **AI Makerspace**:

- **Original Series**: ["How to Build ChatGPT"](https://www.youtube.com/playlist?list=PLrSHiQgy4VjG1B5TXPn99eKf52zSnEUZz)
- **Source Repository**: [AI-Maker-Space/How-to-Build-ChatGPT](https://github.com/AI-Maker-Space/How-to-Build-ChatGPT)
- **Educational Framework**: Used with appreciation for educational and research purposes

### � Special Thanks to AI Makerspace

A heartfelt shoutout to the incredible **AI Makerspace team** for creating world-class educational content that makes cutting-edge AI engineering accessible to everyone. Their "How to Build ChatGPT" series exemplifies the highest standards of technical education, combining theoretical depth with practical implementation.

As a proud **Peer Supporter** for the AI Engineering Bootcamp across 3+ cohorts, I've witnessed firsthand the transformative impact of their curriculum and community. The team's dedication to fostering the next generation of AI engineers is truly inspiring, and their content continues to set the gold standard for AI education.

**The AI Makerspace community is where AI engineers are made.** �

Visit [AI Makerspace](https://www.aimakerspace.com/) to join this amazing learning journey!

### Video Series Credits

- **Part 1**: [Prompting & Responses API](https://www.youtube.com/live/OkqnAk1eH4M)
- **Part 2**: [RAG & Connectors](https://www.youtube.com/live/BAtY88cw3rw)
- **Part 3**: [Agentic Search & Agents SDK](https://www.youtube.com/live/qQ6nCN6ynXo)
- **Part 4**: [Vibe-Coding & Deployment](https://www.youtube.com/watch?v=t13Y5Igh66U)

All generated content includes proper citations and links back to original sources. This project serves as a complementary educational tool and does not replace the original video content.

## Contact & Support

- **Issues**: Please report bugs or suggest features via [GitHub Issues](https://github.com/donbr/agentic-chat/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/donbr/agentic-chat/discussions)
- **AI Makerspace**: Visit [AI Makerspace](https://www.aimakerspace.com/) for the original educational content

---

*Built with d for the AI education community. Transforming video learning into structured knowledge.*