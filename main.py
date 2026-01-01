#!/usr/bin/env python3
"""
Unified Multimodal Knowledge Representation Framework
Author: Pranay M.

System that can seamlessly translate knowledge between text, images,
audio, video, and structured data formats.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║        🔄 UNIFIED MULTIMODAL KNOWLEDGE REPRESENTATION FRAMEWORK 🔄             ║
║                    Cross-Modal Knowledge Translation                           ║
║                           Author: Pranay M.                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Text-to-Visual Translator", "text_visual", "Convert text to visual representations"),
    "2": ("Visual-to-Text Translator", "visual_text", "Convert visuals to text descriptions"),
    "3": ("Audio-to-Text Translator", "audio_text", "Convert audio concepts to text"),
    "4": ("Knowledge Graph Builder", "knowledge_graph", "Build structured knowledge graphs"),
    "5": ("Cross-Modal Mapper", "cross_modal", "Map concepts across modalities"),
    "6": ("Schema Translator", "schema", "Translate between data schemas"),
    "7": ("Semantic Aligner", "semantic", "Align semantics across formats"),
    "8": ("Format Optimizer", "format_opt", "Optimize format for purpose"),
    "9": ("Integration Engine", "integration", "Integrate multi-source knowledge"),
    "10": ("Knowledge Dashboard", "dashboard", "View knowledge representation status")
}

SYSTEM_PROMPTS = {
    "text_visual": """You are an expert in knowledge visualization and visual communication.

For each text-to-visual translation, provide:

1. **Content Analysis**: Key concepts, relationships, hierarchy
2. **Visual Format Selection**: Best visualization type (diagram, chart, infographic)
3. **Visual Design**: Layout, colors, typography recommendations
4. **Element Specification**: Specific visual elements to include
5. **Narrative Flow**: Visual storytelling structure
6. **Implementation Guide**: How to create the visual

Translate textual knowledge to visual representations.""",

    "visual_text": """You are an expert in visual analysis and textual description.

For each visual-to-text translation, provide:

1. **Visual Analysis**: What the visual contains
2. **Structure Description**: Layout, organization, hierarchy
3. **Content Extraction**: Key information depicted
4. **Relationship Mapping**: Connections shown in visual
5. **Textual Representation**: Written description
6. **Format Options**: Prose, outline, structured data

Translate visual knowledge to textual descriptions.""",

    "audio_text": """You are an expert in audio content and textual representation.

For each audio-to-text conceptual translation, provide:

1. **Audio Content Analysis**: Speech, music, sound concepts
2. **Information Extraction**: Key content, messages, themes
3. **Temporal Structure**: How content unfolds over time
4. **Textual Mapping**: How to represent in text
5. **Notation Systems**: Transcription, annotation approaches
6. **Format Recommendations**: Best text format for content

Translate audio concepts to textual representations.""",

    "knowledge_graph": """You are an expert in knowledge graphs and semantic networks.

For each knowledge graph building request, develop:

1. **Entity Extraction**: Key entities to include
2. **Relationship Definition**: Connections between entities
3. **Ontology Design**: Categories, hierarchies, types
4. **Property Specification**: Attributes of entities
5. **Graph Structure**: Overall organization
6. **Query Capabilities**: What questions graph can answer

Build structured knowledge graphs from content.""",

    "cross_modal": """You are an expert in cross-modal representation and translation.

For each cross-modal mapping, provide:

1. **Source Analysis**: Original modality content
2. **Target Requirements**: Destination modality needs
3. **Concept Mapping**: How concepts translate
4. **Loss Assessment**: What's lost in translation
5. **Enhancement Opportunities**: What's gained
6. **Bidirectional Considerations**: Round-trip fidelity

Map knowledge concepts across modalities.""",

    "schema": """You are an expert in data schemas and format translation.

For each schema translation, provide:

1. **Source Schema Analysis**: Original structure, types, constraints
2. **Target Schema Design**: Destination structure requirements
3. **Mapping Rules**: How fields/elements translate
4. **Transformation Logic**: Required data transformations
5. **Validation Approach**: Ensuring translation accuracy
6. **Edge Cases**: Handling exceptions, missing data

Translate between data schemas and formats.""",

    "semantic": """You are an expert in semantics and meaning alignment.

For each semantic alignment, analyze:

1. **Semantic Content**: Meaning in source representation
2. **Target Semantics**: How meaning maps to target
3. **Ambiguity Resolution**: Handling multiple meanings
4. **Context Preservation**: Maintaining contextual meaning
5. **Inference Mapping**: Implicit knowledge handling
6. **Verification Methods**: Confirming semantic accuracy

Align semantics across different formats.""",

    "format_opt": """You are an expert in information design and format optimization.

For each format optimization, recommend:

1. **Use Case Analysis**: How knowledge will be used
2. **Audience Assessment**: Who will consume the knowledge
3. **Format Evaluation**: Pros/cons of format options
4. **Optimization Criteria**: What to optimize for
5. **Recommended Format**: Best format for purpose
6. **Conversion Guidance**: How to achieve optimal format

Optimize knowledge format for specific purposes.""",

    "integration": """You are an expert in knowledge integration and fusion.

For each integration request, provide:

1. **Source Inventory**: All knowledge sources to integrate
2. **Compatibility Analysis**: How sources relate
3. **Conflict Resolution**: Handling contradictions
4. **Deduplication**: Identifying redundancies
5. **Unified Representation**: Integrated knowledge structure
6. **Quality Assessment**: Completeness, accuracy

Integrate knowledge from multiple sources and formats.""",

    "dashboard": """You are an expert in knowledge management analytics.

For each dashboard, generate:

1. **Knowledge Inventory**: Available knowledge representations
2. **Format Distribution**: Breakdown by modality/format
3. **Integration Status**: Cross-modal connections
4. **Quality Metrics**: Completeness, accuracy, freshness
5. **Usage Analytics**: How knowledge is accessed
6. **Recommendations**: Optimization opportunities

View knowledge representation status and analytics."""
}

def get_multiline_input(prompt_text):
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

def display_menu():
    console.print(BANNER, style="bold blue")
    table = Table(title="🔄 Knowledge Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=42)
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_module(module_key):
    name, key, desc = MODULES[module_key]
    console.print(Panel(f"🔄 {name}", style="bold green"))
    user_input = get_multiline_input(f"Describe your {name.lower()} request:")
    with console.status(f"[bold green]Processing {name}..."):
        response = query_llama(SYSTEM_PROMPTS[key], user_input)
    console.print(Panel(Markdown(response), title=f"🔄 {name} Results", border_style="green"))

def main():
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Multimodal Knowledge Framework![/yellow]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        try:
            run_module(choice)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
