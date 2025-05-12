"""
Command-line interface for the image generator.
"""

import argparse
import sys
from pathlib import Path
from typing import List
import logging
from rich.console import Console
from rich.progress import Progress

from .generator import ImageGenerator
from .config import GeneratorConfig, load_config

console = Console()

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate images from text prompts",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Text prompt describing the scene to generate"
    )
    
    parser.add_argument(
        "-f", "--file",
        type=Path,
        help="File containing prompts (one per line)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory for generated images"
    )
    
    parser.add_argument(
        "-c", "--config",
        type=Path,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        help="Image width"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        help="Image height"
    )
    
    parser.add_argument(
        "--format",
        choices=["PNG", "JPEG", "BMP"],
        help="Output image format"
    )
    
    parser.add_argument(
        "--quality",
        type=int,
        help="Image quality (1-100)"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Use parallel processing for batch generation"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible generation"
    )
    
    return parser.parse_args()

def main() -> int:
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.width:
        config.width = args.width
    if args.height:
        config.height = args.height
    if args.format:
        config.output_format = args.format
    if args.quality:
        config.output_quality = args.quality
    if args.output:
        config.output_dir = args.output
    if args.parallel:
        config.parallel_processing = True
    if args.seed:
        config.seed = args.seed
    
    # Ensure output directory exists
    config.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create generator
    generator = ImageGenerator(config)
    
    try:
        if args.file:
            # Batch generation from file
            with open(args.file) as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            if not prompts:
                console.print("[red]No prompts found in file[/red]")
                return 1
            
            console.print(f"[green]Generating {len(prompts)} images...[/green]")
            with Progress() as progress:
                task = progress.add_task("Generating...", total=len(prompts))
                output_paths = generator.generate_batch(prompts)
                progress.update(task, completed=len(prompts))
            
            console.print("\n[green]Generated images:[/green]")
            for path in output_paths:
                console.print(f"  {path}")
        
        elif args.prompt:
            # Single image generation
            console.print("[green]Generating image...[/green]")
            output_path = generator.generate(args.prompt)
            console.print(f"\n[green]Image generated: {output_path}[/green]")
        
        else:
            # Interactive mode
            console.print("[yellow]Enter prompts (empty line to finish):[/yellow]")
            prompts: List[str] = []
            
            while True:
                try:
                    prompt = input("> ").strip()
                    if not prompt:
                        break
                    prompts.append(prompt)
                except (KeyboardInterrupt, EOFError):
                    break
            
            if not prompts:
                console.print("[red]No prompts provided[/red]")
                return 1
            
            console.print(f"\n[green]Generating {len(prompts)} images...[/green]")
            with Progress() as progress:
                task = progress.add_task("Generating...", total=len(prompts))
                output_paths = generator.generate_batch(prompts)
                progress.update(task, completed=len(prompts))
            
            console.print("\n[green]Generated images:[/green]")
            for path in output_paths:
                console.print(f"  {path}")
        
        return 0
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Generation interrupted[/yellow]")
        return 130
    
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        logging.exception("Generation failed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 