# HKUST-GZ Faculty Research Agent - Setup Guide

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python run.py
   ```

3. **Access the Web Interface:**
   Open your browser and go to: http://localhost:5000

## Detailed Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for web scraping)
- Internet connection

### Installation Steps

1. **Clone or download the project:**
   ```bash
   cd faculty-research-agent
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Set up OpenAI API key for enhanced analysis:**
   - Get an API key from [OpenAI](https://platform.openai.com/)
   - Add it to the web interface when running the application

### Testing the Installation

Run the test script to verify everything works:
```bash
python test_scraper.py
```

This will:
- Create sample faculty data
- Test the research matching functionality
- Optionally test web scraping

### Usage

1. **Start the application:**
   ```bash
   python run.py
   ```

2. **Step 1: Collect Faculty Data**
   - Click "Start Scraping" to scrape HKUST-GZ faculty directory
   - Or load existing data from a JSON file

3. **Step 2: Define Your Research Interests**
   - Enter your research interests in detail
   - Optionally provide OpenAI API key for enhanced analysis

4. **Step 3: View Results**
   - See matching faculty members ranked by similarity
   - Click "Detailed Analysis" for in-depth insights
   - Export results in JSON or CSV format

### Features

- **Web Scraping:** Automatically scrapes HKUST-GZ faculty directory
- **AI-Powered Matching:** Uses semantic similarity and LLM analysis
- **Interactive Web Interface:** Modern, responsive UI
- **Export Results:** Save matches in multiple formats
- **Detailed Analysis:** Get specific insights about each faculty member

### Configuration

Edit `config.py` to customize:
- Similarity threshold for matching
- Maximum number of results
- API rate limiting
- Data source preferences

### Troubleshooting

**Common Issues:**

1. **Chrome WebDriver not found:**
   - The application automatically downloads ChromeDriver
   - Make sure Chrome browser is installed

2. **OpenAI API errors:**
   - Check your API key is correct
   - Ensure you have sufficient credits

3. **Web scraping fails:**
   - Website structure may have changed
   - Check internet connection
   - Try increasing delay between requests

4. **Import errors:**
   - Make sure all dependencies are installed
   - Run `pip install -r requirements.txt`

### File Structure

```
faculty-research-agent/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── hkust_scraper.py       # Web scraping module
├── research_matcher.py    # AI matching module
├── run.py                 # Application launcher
├── test_scraper.py        # Test script
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── SETUP.md              # This setup guide
├── templates/            # HTML templates
│   └── index.html
└── static/               # CSS and JavaScript
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

### API Endpoints

- `GET /` - Main web interface
- `POST /scrape` - Start faculty scraping
- `POST /load_profiles` - Load existing data
- `POST /match` - Find matching faculty
- `POST /analyze/<index>` - Get detailed analysis
- `POST /export` - Export results
- `GET /files` - List available data files

### Security Notes

- The application runs locally by default
- OpenAI API keys are not stored permanently
- Web scraping respects rate limits and robots.txt
- No sensitive data is transmitted to external services

### Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in the application directory
3. Test with the provided test script
4. Check the HKUST-GZ website structure hasn't changed

## License

This project is provided as-is for educational and research purposes. 