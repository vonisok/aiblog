"""
Image Generator

Creates AI-generated cover images using DALL·E and optimizes them for web use.
"""

import os
import base64
import hashlib
import requests
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

import openai
from PIL import Image, ImageOps
from rich.console import Console

console = Console()


class ImageGenerator:
    """AI-powered image generator for blog cover images."""

    def __init__(self, api_key: str, output_dir: Path = None):
        """Initialize the image generator.
        
        Args:
            api_key: OpenAI API key
            output_dir: Directory to save generated images
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.output_dir = output_dir or Path("content/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_file_size = 400 * 1024  # 400KB limit

    def generate_cover_image(
        self, 
        title: str, 
        category: str, 
        keywords: list = None
    ) -> Optional[str]:
        """Generate a cover image for a blog post.
        
        Args:
            title: Blog post title
            category: Post category
            keywords: Additional keywords for image generation
            
        Returns:
            Relative path to generated image file, or None if failed
        """
        try:
            # Create descriptive prompt for DALL·E
            prompt = self._create_image_prompt(title, category, keywords)
            console.print(f"[blue]Generating image with prompt: {prompt[:100]}...[/blue]")
            
            # Generate image using DALL·E
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",  # High resolution for better quality
                quality="standard",
                n=1
            )
            
            # Download the generated image
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            
            # Process and optimize the image
            filename = self._create_filename(title)
            optimized_path = self._process_and_save_image(
                image_data, 
                filename,
                target_size=(1200, 630)  # Social media optimized size
            )
            
            if optimized_path:
                console.print(f"[green]Generated cover image: {optimized_path}[/green]")
                # Return relative path for use in markdown
                return f"images/{optimized_path.name}"
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error generating cover image: {e}[/red]")
            return None

    def _create_image_prompt(
        self, 
        title: str, 
        category: str, 
        keywords: list = None
    ) -> str:
        """Create a descriptive prompt for DALL·E image generation.
        
        Args:
            title: Blog post title
            category: Post category  
            keywords: Additional keywords
            
        Returns:
            Generated prompt for DALL·E
        """
        # Base style for tech blog images
        base_style = "modern, clean, professional, tech-inspired, minimalist"
        
        # Category-specific visual elements
        category_styles = {
            "AI & Machine Learning": "neural networks, data visualization, blue and purple gradients",
            "Web Development": "code elements, browser interfaces, geometric patterns",
            "Productivity": "organized layouts, productivity tools, calm colors",
            "Tech News": "digital interface, news layout, modern typography",
            "Software Engineering": "code snippets, development tools, structured design",
            "Data Science": "charts, graphs, data visualization, analytical themes"
        }
        
        category_style = category_styles.get(category, "technology, digital, modern")
        
        # Clean title for prompt (remove special chars)
        clean_title = title.replace('"', '').replace("'", "")
        
        # Combine elements
        prompt_parts = [
            f"Create a professional blog cover image representing '{clean_title}'",
            f"Style: {base_style}",
            f"Visual elements: {category_style}",
            "Colors: modern tech palette with good contrast",
            "Layout: suitable for blog header, no text overlay needed",
            "Aspect ratio: landscape orientation"
        ]
        
        if keywords:
            keyword_str = ", ".join(keywords[:3])  # Limit keywords to avoid prompt bloat
            prompt_parts.append(f"Related concepts: {keyword_str}")
        
        return ". ".join(prompt_parts)

    def _create_filename(self, title: str) -> str:
        """Create a safe filename from blog post title.
        
        Args:
            title: Blog post title
            
        Returns:
            Safe filename string
        """
        # Create hash from title for uniqueness
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        
        # Create safe filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '-').lower()[:30]  # Limit length
        
        timestamp = datetime.now().strftime("%Y%m%d")
        
        return f"{timestamp}-{safe_title}-{title_hash}.jpg"

    def _process_and_save_image(
        self, 
        image_data: bytes, 
        filename: str,
        target_size: Tuple[int, int] = (1200, 630)
    ) -> Optional[Path]:
        """Process and optimize image for web use.
        
        Args:
            image_data: Raw image data
            filename: Target filename
            target_size: Target dimensions (width, height)
            
        Returns:
            Path to saved optimized image, or None if failed
        """
        try:
            # Load image
            image = Image.open(BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to target dimensions while maintaining aspect ratio
            image = ImageOps.fit(image, target_size, Image.Resampling.LANCZOS)
            
            # Save with optimization
            output_path = self.output_dir / filename
            
            # Start with high quality and reduce if file is too large
            quality = 85
            while quality > 30:
                buffer = BytesIO()
                image.save(buffer, format='JPEG', quality=quality, optimize=True)
                
                if len(buffer.getvalue()) <= self.max_file_size:
                    # File size is acceptable, save it
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    
                    console.print(
                        f"[green]Optimized image: {len(buffer.getvalue())/1024:.1f}KB "
                        f"at {quality}% quality[/green]"
                    )
                    return output_path
                
                quality -= 10
            
            # If we can't get under size limit, save with minimum quality
            with open(output_path, 'wb') as f:
                image.save(f, format='JPEG', quality=30, optimize=True)
            
            console.print(
                f"[yellow]Warning: Image saved at minimum quality to meet size limit[/yellow]"
            )
            return output_path
            
        except Exception as e:
            console.print(f"[red]Error processing image: {e}[/red]")
            return None

    def generate_placeholder_image(
        self, 
        title: str, 
        size: Tuple[int, int] = (1200, 630)
    ) -> Optional[str]:
        """Generate a simple placeholder image when DALL·E is unavailable.
        
        Args:
            title: Blog post title
            size: Image dimensions
            
        Returns:
            Relative path to placeholder image, or None if failed
        """
        try:
            # Create simple gradient placeholder
            width, height = size
            image = Image.new('RGB', size, color='#1a1a1a')
            
            # Add some visual interest with a gradient effect
            for y in range(height):
                for x in range(width):
                    # Simple gradient from dark to slightly lighter
                    intensity = int(26 + (y / height) * 40)  # 26 to 66
                    image.putpixel((x, y), (intensity, intensity, intensity))
            
            # Save placeholder
            filename = self._create_filename(f"placeholder-{title}")
            output_path = self.output_dir / filename
            
            image.save(output_path, format='JPEG', quality=80)
            
            console.print(f"[yellow]Created placeholder image: {output_path}[/yellow]")
            return f"images/{output_path.name}"
            
        except Exception as e:
            console.print(f"[red]Error creating placeholder image: {e}[/red]")
            return None

    def cleanup_old_images(self, days_old: int = 30) -> None:
        """Remove old generated images to save space.
        
        Args:
            days_old: Remove images older than this many days
        """
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            removed_count = 0
            for image_file in self.output_dir.glob("*.jpg"):
                if image_file.stat().st_mtime < cutoff_time:
                    image_file.unlink()
                    removed_count += 1
            
            if removed_count > 0:
                console.print(f"[blue]Cleaned up {removed_count} old images[/blue]")
            
        except Exception as e:
            console.print(f"[red]Error during image cleanup: {e}[/red]")


def main():
    """CLI entry point for image generation testing."""
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]OPENAI_API_KEY environment variable required[/red]")
        sys.exit(1)
    
    # Test image generation
    generator = ImageGenerator(api_key)
    
    test_title = "The Future of AI in Web Development"
    test_category = "AI & Machine Learning"
    test_keywords = ["artificial intelligence", "web development", "automation"]
    
    image_path = generator.generate_cover_image(test_title, test_category, test_keywords)
    
    if image_path:
        console.print(f"[green]Test image generated: {image_path}[/green]")
    else:
        console.print("[red]Failed to generate test image[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main() 