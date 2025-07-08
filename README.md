# Price Comparison Tool

A generic tool that fetches product prices from multiple websites based on country and product query, with AI/LLM integration for product matching, data extraction, and intelligent ranking.

## Features

- **Multi-Country Support**: Supports 12+ countries including US, UK, India, Canada, Germany, France, etc.
- **AI-Powered Matching**: Uses LLM for accurate product matching and relevance scoring
- **Intelligent Ranking**: Ranks products by relevance and price
- **Modern UI**: Responsive web interface with professional design
- **Caching**: In-memory caching for improved performance
- **RESTful API**: Clean API endpoints for integration

## Tech Stack

- **Backend**: Python Flask with FastAPI-style architecture
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Web Scraping**: Playwright for dynamic content handling
- **AI/LLM**: OpenAI integration with mock fallback
- **Caching**: In-memory cache service
- **Styling**: Modern CSS with gradients and animations

## Quick Start

### Prerequisites
- Python 3.11+
- Virtual environment support

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd price_comparison_tool
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

4. Run the application
```bash
python src/main.py
```

5. Open browser and navigate to `http://localhost:5000`

## API Usage

### Compare Prices Endpoint

**POST** `/api/compare-prices`

**Request Body:**
```json
{
  "country": "US",
  "query": "iPhone 16 Pro, 128GB"
}
```

**Response:**
```json
[
  {
    "link": "https://amazon.com/...",
    "price": "999",
    "currency": "USD",
    "productName": "Apple iPhone 16 Pro 128GB",
    "rating": "4.5",
    "reviewsCount": "1234",
    "source": "Amazon",
    "relevanceScore": 0.95
  }
]
```

### Test Endpoint

**GET** `/api/test`

Returns a simple health check message.

## Supported Countries

- 🇺🇸 United States (US)
- 🇬🇧 United Kingdom (UK)
- 🇮🇳 India (IN)
- 🇨🇦 Canada (CA)
- 🇩🇪 Germany (DE)
- 🇫🇷 France (FR)
- 🇮🇹 Italy (IT)
- 🇪🇸 Spain (ES)
- 🇯🇵 Japan (JP)
- 🇦🇺 Australia (AU)
- 🇧🇷 Brazil (BR)
- 🇲🇽 Mexico (MX)

## Example Queries

- `{"country": "US", "query": "iPhone 16 Pro, 128GB"}`
- `{"country": "IN", "query": "boAt Airdopes 311 Pro"}`
- `{"country": "UK", "query": "Samsung Galaxy S24"}`

## Project Structure

```
price_comparison_tool/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── routes/
│   │   ├── price_comparison.py # Price comparison API routes
│   │   └── user.py            # User management routes
│   ├── services/
│   │   ├── scraper_service.py  # Web scraping logic
│   │   ├── llm_service.py      # AI/LLM integration
│   │   └── cache_service.py    # Caching service
│   ├── models/
│   │   └── user.py            # Database models
│   └── static/
│       └── index.html         # Frontend interface
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for LLM integration (optional, falls back to mock)

### Customization

- **Add New Countries**: Update `country_domains` and `currency_map` in `scraper_service.py`
- **Add New Websites**: Create new scraping adapters in the scraper service
- **Modify UI**: Edit `src/static/index.html` for frontend changes

## Development

### Running Tests

Currently using manual testing. API can be tested with:

```bash
curl -X POST http://localhost:5000/api/compare-prices \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "query": "iPhone 16 Pro, 128GB"}'
```

### Architecture

The application follows a modular architecture:

1. **Frontend**: Single-page application with modern UI
2. **API Layer**: Flask routes handling HTTP requests
3. **Service Layer**: Business logic for scraping, LLM processing, and caching
4. **Data Layer**: In-memory cache and optional database integration

## Deployment

The application is designed to be easily deployable on various platforms:

- **Local**: Run with `python src/main.py`
- **Docker**: Containerization ready
- **Cloud**: Compatible with Heroku, AWS, Google Cloud, etc.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository or contact the development team.

