# 🤖 AI-Generated Blog

> **Fresh insights, generated daily.**

A fully-automated blog system that uses AI to generate high-quality content about technology and productivity. Powered by OpenAI's GPT-4o and DALL·E, deployed automatically via GitHub Actions to Netlify.

## ✨ Features

- 🧠 **AI-Powered Content**: Daily content generation using OpenAI GPT-4o
- 🎨 **Auto-Generated Images**: Cover images created with DALL·E 3
- 🚀 **Automated Publishing**: Git-based workflow with GitHub Actions
- 🌙 **Modern Design**: Tailwind CSS with dark mode support
- ⚡ **Performance Optimized**: Lighthouse score 90+ 
- 📱 **Fully Responsive**: Mobile-first design
- 🔍 **SEO Optimized**: Structured data, meta tags, and sitemaps
- 📊 **Analytics Ready**: Google Analytics and AdSense integration
- 🔄 **RSS & JSON Feeds**: Multiple feed formats supported

## 🏗️ Architecture

```
RSS Feeds → AI Content Generator → Pelican Static Site → Netlify Deployment
     ↓              ↓                    ↓                    ↓
Feed Sources   OpenAI GPT-4o      Tailwind Theme       CDN Distribution
               DALL·E Images      SEO Optimization     Performance Monitoring
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- GitHub account
- Netlify account

### 1. Clone and Setup

```bash
git clone https://github.com/🔸{GITHUB_REPO}.git
cd aiblog
pip install -r requirements.txt
```

### 2. Environment Configuration

Create `.env` file from template:

```bash
cp .env.example .env
```

Required environment variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# RSS Feed Sources (comma-separated)
FEED_SOURCES=https://feeds.feedburner.com/TechCrunch,https://www.wired.com/feed/rss

# Deployment Configuration
NETLIFY_AUTH_TOKEN=your_netlify_auth_token
NETLIFY_SITE_ID=your_netlify_site_id

# Analytics (Optional)
GA_TRACKING_ID=your_google_analytics_id
ADSENSE_ID=your_adsense_publisher_id

# Social (Optional)
TWITTER_USERNAME=your_twitter_handle
GITHUB_USERNAME=your_github_username
```

### 3. Local Development

```bash
# Start development server
docker-compose --profile dev up

# Or manually:
pelican content -s pelicanconf.py
pelican --listen --autoreload
```

Visit `http://localhost:8000` to see your blog.

### 4. Generate Content

```bash
# Generate a single post
python -m content_pipeline.generator

# Generate with images
python -m content_pipeline.images

# Publish to Git
python -m content_pipeline.publisher
```

### 5. Deploy to Production

1. **Fork this repository**
2. **Set up GitHub Secrets**:
   - `OPENAI_API_KEY`
   - `NETLIFY_AUTH_TOKEN`
   - `NETLIFY_SITE_ID`
   - `FEED_SOURCES`

3. **Enable GitHub Actions**
4. **Push to main branch** - automated deployment will begin!

## 📁 Project Structure

```
aiblog/
├── content_pipeline/          # AI content generation system
│   ├── __init__.py
│   ├── generator.py          # Main content generator
│   ├── images.py             # DALL·E image generator  
│   └── publisher.py          # Git publishing automation
├── themes/aiblog/            # Custom Pelican theme
│   ├── templates/            # Jinja2 templates
│   └── static/               # CSS, JS, images
├── content/                  # Generated blog posts
│   ├── images/               # Generated cover images
│   └── YYYY/MM/              # Posts organized by date
├── .github/workflows/        # GitHub Actions
├── tests/                    # Test suite
├── pelicanconf.py           # Development config
├── publishconf.py           # Production config
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Development environment
└── .env.example           # Environment template
```

## 🔧 Configuration

### Content Generation

Edit `pelicanconf.py` to customize:

```python
# AI Blog Configuration
AI_BLOG_CONFIG = {
    'show_reading_time': True,
    'show_categories': True, 
    'show_tags': True,
    'show_social_share': True,
    'enable_dark_mode': True,
    'google_analytics': '🔸{GA_TRACKING_ID}',
    'max_related_posts': 3,
}

# Categories for content generation
CATEGORIES = [
    "AI & Machine Learning",
    "Web Development",
    "Productivity", 
    "Tech News",
    "Software Engineering",
    "Data Science"
]
```

### Feed Sources

Add your preferred RSS feeds to `.env`:

```env
FEED_SOURCES=https://feeds.feedburner.com/TechCrunch,https://rss.cnn.com/rss/edition.rss,https://feeds.arstechnica.com/arstechnica/index
```

### Theme Customization

The theme uses Tailwind CSS with custom configuration in `themes/aiblog/templates/base.html`. Key customization points:

- **Colors**: Modify the `primary` color palette
- **Typography**: Adjust the `prose` configuration
- **Layout**: Edit template files in `themes/aiblog/templates/`

## 🤖 AI Content Pipeline

### Content Generation Process

1. **Feed Analysis**: Fetches trending topics from RSS feeds
2. **Topic Selection**: Uses CTR-weighted heuristics to select keywords
3. **Outline Generation**: Creates structured content outlines
4. **Article Writing**: Generates 1200-word articles with SEO optimization
5. **Image Creation**: Generates cover images using DALL·E 3
6. **Publishing**: Commits content and triggers deployment

### Prompt Engineering

The system uses carefully crafted prompts for:

- **Content Outlines**: Structured, actionable content frameworks
- **Article Generation**: Professional, engaging technical writing
- **SEO Optimization**: Titles, descriptions, and metadata
- **Image Prompts**: Professional, brand-appropriate visuals

### Quality Controls

- **Content Validation**: Ensures minimum word count and structure
- **SEO Checks**: Validates metadata and descriptions
- **Image Optimization**: Compresses images to <400KB
- **Performance Monitoring**: Lighthouse CI integration

## 📊 Analytics & Monitoring

### Built-in Analytics

- **Google Analytics 4**: Page views, user behavior
- **Performance Monitoring**: Core Web Vitals tracking  
- **Error Tracking**: Failed builds and deployments
- **Content Metrics**: Post engagement and popularity

### Performance Budget

The system enforces performance budgets:

- JavaScript: <100KB
- CSS: <50KB  
- Images: <500KB per page
- Fonts: <100KB
- Lighthouse Score: 90+

## 🔒 Security

### Content Security

- **Input Validation**: RSS feed content sanitization
- **API Rate Limiting**: OpenAI usage monitoring
- **Content Filtering**: Automated content review
- **Backup Strategy**: Git-based content versioning

### Infrastructure Security

- **Environment Variables**: All secrets in environment
- **Container Security**: Non-root user, minimal attack surface
- **Dependencies**: Regular vulnerability scanning
- **Access Control**: GitHub Actions with minimal permissions

## 🧪 Testing

Run the test suite:

```bash
# Unit tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=content_pipeline --cov-report=html

# Type checking
mypy content_pipeline/ --strict

# Linting
flake8 content_pipeline/
black content_pipeline/
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end content generation
- **Performance Tests**: Load and response time testing
- **Security Tests**: Input validation and sanitization

## 🚨 Troubleshooting

### Common Issues

**Content generation fails:**
```bash
# Check API key
python -c "import openai; print('API key valid')"

# Check feed sources
python -m content_pipeline.generator --dry-run
```

**Build failures:**
```bash
# Check Pelican configuration
pelican content -s pelicanconf.py --debug

# Validate theme
pelican-themes --install themes/aiblog --verbose
```

**Deployment issues:**
```bash
# Check Netlify configuration
netlify status
netlify deploy --prod --dir=output
```

### Performance Issues

**Slow builds:**
- Reduce content generation frequency
- Optimize image sizes
- Enable caching in GitHub Actions

**High API costs:**
- Monitor OpenAI usage dashboard
- Adjust content generation schedule
- Implement content caching

### Error Monitoring

View logs in:
- GitHub Actions workflow runs
- Netlify deploy logs  
- Browser developer console
- `pelican.log` (in production)

## 📈 Scaling

### Content Volume

- **Frequency**: Adjust cron schedule in `.github/workflows/site.yml`
- **Sources**: Add more RSS feeds to `FEED_SOURCES`
- **Categories**: Expand topic categories in configuration
- **Languages**: Add multi-language support

### Performance

- **CDN**: Configure custom domain with Netlify
- **Caching**: Implement edge-side includes
- **Images**: Use responsive image optimization
- **Database**: Add search functionality with Algolia

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure Lighthouse scores remain 90+

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Open a GitHub issue for bugs and feature requests
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: Contact [your-email@domain.com] for private inquiries

## 🔮 Roadmap

- [ ] **Multi-language Support**: Generate content in multiple languages
- [ ] **Advanced SEO**: Schema.org markup and structured data
- [ ] **Social Integration**: Auto-posting to Twitter/LinkedIn
- [ ] **Analytics Dashboard**: Custom analytics and insights
- [ ] **Content Curation**: AI-powered content recommendation
- [ ] **Voice Support**: Audio versions of articles
- [ ] **Newsletter**: Automated email newsletter generation

---

**Built with ❤️ and 🤖 AI**

*This blog generates fresh insights daily using cutting-edge AI technology. Join the future of automated content creation!* 