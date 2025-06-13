"""
Tests for the content generator module.
"""

import os
import json
import pytest
from unittest.mock import Mock, patch, mock_open
from datetime import datetime
from pathlib import Path

from content_pipeline.generator import ContentGenerator, BlogPost


class TestBlogPost:
    """Test BlogPost dataclass."""
    
    def test_blog_post_creation(self):
        """Test BlogPost creation with basic data."""
        post = BlogPost(
            title="Test Title",
            slug="test-title",
            content="Test content",
            summary="Test summary", 
            meta_description="Test meta",
            category="Tech News",
            tags=["test", "python"]
        )
        
        assert post.title == "Test Title"
        assert post.slug == "test-title"
        assert post.tags == ["test", "python"]
        assert isinstance(post.date, datetime)
        assert post.tweets == []
    
    def test_blog_post_with_custom_date(self):
        """Test BlogPost with custom date."""
        custom_date = datetime(2024, 1, 15)
        post = BlogPost(
            title="Test",
            slug="test",
            content="Content",
            summary="Summary",
            meta_description="Meta",
            category="Tech",
            tags=[],
            date=custom_date
        )
        
        assert post.date == custom_date


class TestContentGenerator:
    """Test ContentGenerator class."""
    
    @pytest.fixture
    def generator(self):
        """Create a ContentGenerator instance for testing."""
        return ContentGenerator(
            api_key="test_key",
            feed_sources=["https://example.com/feed.xml"]
        )
    
    @pytest.fixture
    def mock_feed_data(self):
        """Mock RSS feed data."""
        return {
            'feed': {'title': 'Test Feed'},
            'entries': [
                {
                    'title': 'AI Advances in 2024',
                    'description': 'Latest AI developments',
                    'link': 'https://example.com/ai-2024',
                    'published': '2024-01-15'
                },
                {
                    'title': 'Python Web Development',
                    'description': 'Building web apps with Python',
                    'link': 'https://example.com/python-web',
                    'published': '2024-01-14'
                }
            ]
        }
    
    def test_initialization(self, generator):
        """Test ContentGenerator initialization."""
        assert generator.feed_sources == ["https://example.com/feed.xml"]
        assert len(generator.categories) == 6
        assert "AI & Machine Learning" in generator.categories
    
    @patch('content_pipeline.generator.feedparser.parse')
    def test_fetch_trending_topics(self, mock_parse, generator, mock_feed_data):
        """Test fetching trending topics from RSS feeds."""
        mock_parse.return_value = mock_feed_data
        
        topics = generator.fetch_trending_topics()
        
        assert len(topics) == 2
        assert topics[0]['title'] == 'AI Advances in 2024'
        assert topics[0]['source'] == 'Test Feed'
        assert topics[1]['title'] == 'Python Web Development'
    
    @patch('content_pipeline.generator.feedparser.parse')
    def test_fetch_trending_topics_with_error(self, mock_parse, generator):
        """Test fetching topics when feed parsing fails."""
        mock_parse.side_effect = Exception("Network error")
        
        topics = generator.fetch_trending_topics()
        
        assert topics == []
    
    def test_select_topic_keyword(self, generator):
        """Test topic keyword selection."""
        topics = [
            {'title': 'AI Machine Learning Advances'},
            {'title': 'Machine Learning in Python'},
            {'title': 'Data Science with AI'}
        ]
        
        keyword = generator.select_topic_keyword(topics)
        
        # Should select the most frequent meaningful word
        assert keyword in ['Machine', 'Learning', 'AI', 'Python', 'Data', 'Science']
    
    def test_select_topic_keyword_fallback(self, generator):
        """Test keyword selection fallback."""
        topics = [
            {'title': 'The and for are but not'},  # Only stopwords
        ]
        
        keyword = generator.select_topic_keyword(topics)
        
        assert keyword == "Technology"  # Fallback
    
    @patch('content_pipeline.generator.openai.OpenAI')
    def test_generate_content_outline(self, mock_openai_class, generator):
        """Test content outline generation."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices[0].message.content = "I. Introduction\nII. Main Content\nIII. Conclusion"
        mock_client.chat.completions.create.return_value = mock_response
        
        outline = generator.generate_content_outline("AI")
        
        assert "Introduction" in outline
        assert "Main Content" in outline
        assert "Conclusion" in outline
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('content_pipeline.generator.openai.OpenAI')
    def test_generate_content_outline_error(self, mock_openai_class, generator):
        """Test outline generation with API error."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        outline = generator.generate_content_outline("AI")
        
        assert "AI: A Comprehensive Guide" in outline
        assert "Introduction" in outline
    
    @patch('content_pipeline.generator.openai.OpenAI')
    def test_generate_full_article(self, mock_openai_class, generator):
        """Test full article generation."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Mock content response
        content_response = Mock()
        content_response.choices[0].message.content = "## Introduction\n\nThis is test content.\n\n## Conclusion\n\nTest conclusion."
        
        # Mock SEO response
        seo_response = Mock()
        seo_response.choices[0].message.content = json.dumps({
            "title": "AI Test Article",
            "slug": "ai-test-article",
            "meta_description": "Test meta description",
            "tweets": ["Test tweet 1", "Test tweet 2"],
            "tags": ["ai", "test"],
            "category": "AI & Machine Learning",
            "summary": "Test summary"
        })
        
        mock_client.chat.completions.create.side_effect = [content_response, seo_response]
        
        post = generator.generate_full_article("AI", "Test outline")
        
        assert isinstance(post, BlogPost)
        assert post.title == "AI Test Article"
        assert post.slug == "ai-test-article"
        assert post.category == "AI & Machine Learning"
        assert len(post.tags) == 2
        assert len(post.tweets) == 2
        assert "Introduction" in post.content
    
    @patch('content_pipeline.generator.openai.OpenAI')
    def test_generate_full_article_seo_error(self, mock_openai_class, generator):
        """Test article generation with SEO data error."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        content_response = Mock()
        content_response.choices[0].message.content = "Test content"
        
        # SEO response fails
        mock_client.chat.completions.create.side_effect = [
            content_response,
            Exception("SEO API Error")
        ]
        
        post = generator.generate_full_article("AI", "Test outline")
        
        assert isinstance(post, BlogPost)
        assert post.title == "AI: Complete Guide"  # Fallback title
        assert post.slug == "ai"  # Fallback slug
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    @patch('yaml.dump')
    def test_save_post(self, mock_yaml_dump, mock_mkdir, mock_file, generator):
        """Test saving blog post to file."""
        post = BlogPost(
            title="Test Post",
            slug="test-post",
            content="Test content",
            summary="Test summary",
            meta_description="Test meta",
            category="Tech News",
            tags=["test"],
            tweets=["Test tweet"]
        )
        
        filepath = generator.save_post(post, Path("test_content"))
        
        # Check file operations
        mock_mkdir.assert_called_once()
        mock_file.assert_called_once()
        mock_yaml_dump.assert_called_once()
        
        # Check filepath
        assert "test-post.md" in str(filepath)
    
    @patch('content_pipeline.generator.ContentGenerator.fetch_trending_topics')
    @patch('content_pipeline.generator.ContentGenerator.select_topic_keyword')
    @patch('content_pipeline.generator.ContentGenerator.generate_content_outline')
    @patch('content_pipeline.generator.ContentGenerator.generate_full_article')
    @patch('content_pipeline.generator.ContentGenerator.save_post')
    def test_generate_daily_post_success(self, mock_save, mock_article, mock_outline,
                                       mock_keyword, mock_topics, generator):
        """Test successful daily post generation."""
        # Setup mocks
        mock_topics.return_value = [{'title': 'Test Topic'}]
        mock_keyword.return_value = "AI"
        mock_outline.return_value = "Test outline"
        mock_post = BlogPost(
            title="Test", slug="test", content="content", 
            summary="summary", meta_description="meta",
            category="Tech", tags=[]
        )
        mock_article.return_value = mock_post
        mock_save.return_value = Path("test.md")
        
        result = generator.generate_daily_post()
        
        assert result == Path("test.md")
        mock_topics.assert_called_once()
        mock_keyword.assert_called_once()
        mock_outline.assert_called_once()
        mock_article.assert_called_once()
        mock_save.assert_called_once()
    
    @patch('content_pipeline.generator.ContentGenerator.fetch_trending_topics')
    def test_generate_daily_post_no_topics(self, mock_topics, generator):
        """Test daily post generation when no topics are found."""
        mock_topics.return_value = []
        
        result = generator.generate_daily_post()
        
        assert result is None
    
    @patch('content_pipeline.generator.ContentGenerator.fetch_trending_topics')
    def test_generate_daily_post_error(self, mock_topics, generator):
        """Test daily post generation with error."""
        mock_topics.side_effect = Exception("Test error")
        
        result = generator.generate_daily_post()
        
        assert result is None


class TestGeneratorCLI:
    """Test the CLI functionality of the generator module."""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('content_pipeline.generator.ContentGenerator')
    def test_main_with_env_vars(self, mock_generator_class):
        """Test main function with environment variables."""
        from content_pipeline.generator import main
        
        mock_generator = Mock()
        mock_generator.generate_daily_post.return_value = Path("test.md")
        mock_generator_class.return_value = mock_generator
        
        main()
        
        mock_generator_class.assert_called_once()
        mock_generator.generate_daily_post.assert_called_once()
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('sys.exit')
    def test_main_without_api_key(self, mock_exit):
        """Test main function without API key."""
        from content_pipeline.generator import main
        
        main()
        
        mock_exit.assert_called_with(1)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('content_pipeline.generator.ContentGenerator')
    @patch('sys.exit')
    def test_main_generation_failure(self, mock_exit, mock_generator_class):
        """Test main function when generation fails."""
        from content_pipeline.generator import main
        
        mock_generator = Mock()
        mock_generator.generate_daily_post.return_value = None
        mock_generator_class.return_value = mock_generator
        
        main()
        
        mock_exit.assert_called_with(1) 