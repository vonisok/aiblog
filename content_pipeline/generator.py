"""
Content Generator

Fetches RSS headlines, selects topics, and generates AI-powered blog content.
"""

import os
import re
import yaml
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

import feedparser
import openai
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track

console = Console()


@dataclass
class BlogPost:
    """Blog post data structure."""
    title: str
    slug: str
    content: str
    summary: str
    meta_description: str
    category: str
    tags: List[str]
    cover_image: Optional[str] = None
    tweets: List[str] = None
    date: datetime = None

    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now(timezone.utc)
        if self.tweets is None:
            self.tweets = []


class ContentGenerator:
    """AI-powered content generator for blog posts."""

    def __init__(self, api_key: str, feed_sources: List[str]):
        """Initialize the content generator.
        
        Args:
            api_key: OpenAI API key
            feed_sources: List of RSS feed URLs
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.feed_sources = feed_sources
        self.categories = [
            "AI & Machine Learning",
            "Web Development", 
            "Productivity",
            "Tech News",
            "Software Engineering",
            "Data Science"
        ]

    def fetch_trending_topics(self) -> List[Dict[str, str]]:
        """Fetch trending topics from RSS feeds.
        
        Returns:
            List of trending topics with titles and descriptions
        """
        topics = []
        
        for feed_url in track(self.feed_sources, description="Fetching RSS feeds..."):
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # Top 5 from each feed
                    topic = {
                        "title": entry.title,
                        "description": getattr(entry, 'description', ''),
                        "link": getattr(entry, 'link', ''),
                        "published": getattr(entry, 'published', ''),
                        "source": feed.feed.get('title', 'Unknown')
                    }
                    topics.append(topic)
            except Exception as e:
                console.print(f"[red]Error fetching {feed_url}: {e}[/red]")
                continue
        
        return topics

    def select_topic_keyword(self, topics: List[Dict[str, str]]) -> str:
        """Select optimal topic keyword using CTR-weighted heuristics.
        
        Args:
            topics: List of trending topics
            
        Returns:
            Selected keyword for content generation
        """
        # Extract keywords from titles and weight by frequency
        keyword_counts = {}
        
        for topic in topics:
            # Extract meaningful keywords (3+ chars, not common words)
            words = re.findall(r'\b[a-zA-Z]{3,}\b', topic['title'].lower())
            stopwords = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 
                        'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day',
                        'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now',
                        'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its',
                        'let', 'put', 'say', 'she', 'too', 'use'}
            
            for word in words:
                if word not in stopwords and len(word) > 2:
                    keyword_counts[word] = keyword_counts.get(word, 0) + 1
        
        # Sort by frequency and select top keyword
        if keyword_counts:
            top_keyword = max(keyword_counts.items(), key=lambda x: x[1])[0]
            return top_keyword.title()
        
        # Fallback keywords
        return "Technology"

    def generate_content_outline(self, keyword: str) -> str:
        """Generate content outline using OpenAI.
        
        Args:
            keyword: Topic keyword for content generation
            
        Returns:
            Generated content outline
        """
        prompt = f"""
        Create a detailed outline for a 1200-word blog post about "{keyword}" 
        targeting tech professionals and productivity enthusiasts.
        
        Requirements:
        - Focus on actionable insights and practical applications
        - Include 5-7 main sections with subpoints
        - Add specific examples and case studies where relevant
        - Maintain a concise, lightly opinionated tone
        - Include relevant statistics or data points
        
        Format as a structured outline with Roman numerals and bullet points.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]Error generating outline: {e}[/red]")
            return f"# {keyword}: A Comprehensive Guide\n\nI. Introduction\nII. Key Concepts\nIII. Practical Applications\nIV. Best Practices\nV. Conclusion"

    def generate_full_article(self, keyword: str, outline: str) -> BlogPost:
        """Generate full blog article from outline.
        
        Args:
            keyword: Topic keyword
            outline: Content outline
            
        Returns:
            Complete BlogPost object
        """
        # Generate main content
        content_prompt = f"""
        Write a comprehensive 1200-word blog post based on this outline:
        
        {outline}
        
        Topic: {keyword}
        
        Requirements:
        - Write in Markdown format
        - Use clear, engaging headers (##, ###)
        - Include code examples where relevant (use ```language blocks)
        - Add actionable takeaways and practical tips
        - Maintain professional but conversational tone
        - Include relevant statistics and data
        - End with a strong conclusion and call-to-action
        - Do not include title - just the body content
        """
        
        try:
            content_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": content_prompt}],
                temperature=0.7,
                max_tokens=2500
            )
            content = content_response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]Error generating content: {e}[/red]")
            content = f"## Introduction\n\nThis article explores {keyword} and its applications.\n\n## Conclusion\n\nStay tuned for more insights!"

        # Generate SEO metadata
        seo_prompt = f"""
        Based on this article content about "{keyword}", generate:
        
        1. SEO-optimized title (max 60 chars)
        2. URL slug (lowercase, hyphens, max 50 chars)
        3. Meta description (150-160 chars)
        4. 3 tweetable snippets (max 280 chars each)
        5. 3-5 relevant tags
        6. Category from: {', '.join(self.categories)}
        7. Brief summary (max 160 chars)
        
        Article preview:
        {content[:500]}...
        
        Respond in JSON format:
        {
            "title": "...",
            "slug": "...",
            "meta_description": "...",
            "tweets": ["...", "...", "..."],
            "tags": ["...", "...", "..."],
            "category": "...",
            "summary": "..."
        }
        """
        
        try:
            seo_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": seo_prompt}],
                temperature=0.3,
                max_tokens=800
            )
            seo_data = json.loads(seo_response.choices[0].message.content)
        except Exception as e:
            console.print(f"[red]Error generating SEO data: {e}[/red]")
            # Fallback SEO data
            slug = re.sub(r'[^a-z0-9]+', '-', keyword.lower()).strip('-')
            seo_data = {
                "title": f"{keyword}: Complete Guide",
                "slug": slug,
                "meta_description": f"Comprehensive guide to {keyword} with practical tips and insights.",
                "tweets": [f"New article: {keyword} insights!", f"Learn about {keyword} today", f"Essential {keyword} tips"],
                "tags": [keyword, "tech", "productivity"],
                "category": "Tech News",
                "summary": f"Essential insights and practical tips about {keyword}."
            }

        return BlogPost(
            title=seo_data["title"],
            slug=seo_data["slug"],
            content=content,
            summary=seo_data["summary"],
            meta_description=seo_data["meta_description"],
            category=seo_data["category"],
            tags=seo_data["tags"],
            tweets=seo_data["tweets"]
        )

    def save_post(self, post: BlogPost, content_dir: Path = None) -> Path:
        """Save blog post to content directory.
        
        Args:
            post: BlogPost object to save
            content_dir: Content directory path
            
        Returns:
            Path to saved file
        """
        if content_dir is None:
            content_dir = Path("content")
        
        # Create year/month directory structure
        year = post.date.year
        month = f"{post.date.month:02d}"
        post_dir = content_dir / str(year) / month
        post_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = f"{post.slug}.md"
        filepath = post_dir / filename
        
        # Create front matter
        front_matter = {
            "title": post.title,
            "date": post.date.isoformat(),
            "category": post.category,
            "tags": post.tags,
            "summary": post.summary,
            "description": post.meta_description,
            "slug": post.slug
        }
        
        if post.cover_image:
            front_matter["cover_image"] = post.cover_image
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(front_matter, f, default_flow_style=False, allow_unicode=True)
            f.write("---\n\n")
            f.write(post.content)
            
            # Add tweetable snippets as comments
            if post.tweets:
                f.write("\n\n<!-- Tweetable Snippets:\n")
                for i, tweet in enumerate(post.tweets, 1):
                    f.write(f"{i}. {tweet}\n")
                f.write("-->\n")
        
        console.print(f"[green]Saved post: {filepath}[/green]")
        return filepath

    def generate_daily_post(self) -> Optional[Path]:
        """Generate and save a daily blog post.
        
        Returns:
            Path to generated post file, or None if failed
        """
        try:
            console.print("[blue]Starting daily content generation...[/blue]")
            
            # Fetch trending topics
            topics = self.fetch_trending_topics()
            if not topics:
                console.print("[red]No topics found from RSS feeds[/red]")
                return None
            
            console.print(f"[green]Found {len(topics)} trending topics[/green]")
            
            # Select topic keyword
            keyword = self.select_topic_keyword(topics)
            console.print(f"[blue]Selected keyword: {keyword}[/blue]")
            
            # Generate outline
            outline = self.generate_content_outline(keyword)
            console.print("[blue]Generated content outline[/blue]")
            
            # Generate full article
            post = self.generate_full_article(keyword, outline)
            console.print(f"[green]Generated article: {post.title}[/green]")
            
            # Save post
            filepath = self.save_post(post)
            
            return filepath
            
        except Exception as e:
            console.print(f"[red]Error in daily post generation: {e}[/red]")
            return None


def main():
    """CLI entry point for content generation."""
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]OPENAI_API_KEY environment variable required[/red]")
        sys.exit(1)
    
    feed_sources = os.getenv("FEED_SOURCES", "").split(",")
    feed_sources = [url.strip() for url in feed_sources if url.strip()]
    
    if not feed_sources:
        # Default tech RSS feeds
        feed_sources = [
            "https://feeds.feedburner.com/TechCrunch",
            "https://rss.cnn.com/rss/edition.rss",
            "https://feeds.arstechnica.com/arstechnica/index",
            "https://www.wired.com/feed/rss"
        ]
    
    generator = ContentGenerator(api_key, feed_sources)
    filepath = generator.generate_daily_post()
    
    if filepath:
        console.print(f"[green]Success! Generated post at: {filepath}[/green]")
    else:
        console.print("[red]Failed to generate post[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main() 