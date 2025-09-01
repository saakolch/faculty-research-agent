# Faculty Research Agent

An intelligent agent that analyzes faculty research profiles and matches them with your research interests using AI-powered semantic analysis.

## Features

- **Research Profile Analysis**: Scrapes and analyzes faculty research from multiple sources
- **Interest Matching**: Uses semantic similarity to match your interests with faculty research
- **Multiple Data Sources**: Google Scholar, arXiv, university websites, and more
- **Interactive Web Interface**: Modern, responsive web UI for easy interaction
- **AI-Powered Analysis**: Leverages OpenAI and local models for intelligent matching
- **Export Results**: Save and export matching results in various formats

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Start the web application
2. Enter your research interests
3. Add faculty members or institutions to analyze
4. View matching results and detailed analysis
5. Export results as needed

## Data Sources

- Google Scholar profiles
- arXiv publications
- University faculty pages
- ResearchGate profiles
- Semantic Scholar API

## Technologies Used

- **Backend**: Flask, Python
- **AI/ML**: OpenAI API, Sentence Transformers, scikit-learn
- **Data Processing**: Pandas, NLTK, BeautifulSoup
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **APIs**: Google Scholar, arXiv, Semantic Scholar

## Configuration

Edit the `.env` file to configure:
- OpenAI API key
- Other API keys as needed
- Application settings

## License

MIT License 