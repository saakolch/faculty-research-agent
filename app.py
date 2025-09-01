from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
from hkust_scraper import HKUSTGZScraper
from research_matcher import ResearchMatcher
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Global variables to store data
faculty_profiles = []
research_matcher = None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_faculty():
    """Start scraping HKUST-GZ faculty directory"""
    global faculty_profiles
    
    try:
        data = request.get_json()
        headless = data.get('headless', True)
        delay = data.get('delay', 2.0)
        
        # Initialize scraper
        scraper = HKUSTGZScraper(headless=headless, delay=delay)
        
        # Start scraping
        profiles = scraper.scrape_all_faculty()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"faculty_profiles_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        
        faculty_profiles = profiles
        
        return jsonify({
            'success': True,
            'message': f'Successfully scraped {len(profiles)} faculty profiles',
            'filename': filename,
            'count': len(profiles)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/load_profiles', methods=['POST'])
def load_profiles():
    """Load previously scraped faculty profiles"""
    global faculty_profiles
    
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename or not os.path.exists(filename):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        with open(filename, 'r', encoding='utf-8') as f:
            faculty_profiles = json.load(f)
        
        return jsonify({
            'success': True,
            'message': f'Loaded {len(faculty_profiles)} faculty profiles',
            'count': len(faculty_profiles)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/match', methods=['POST'])
def match_interests():
    """Match user interests with faculty profiles"""
    global faculty_profiles, research_matcher
    
    try:
        data = request.get_json()
        user_interests = data.get('interests', '')
        openai_key = data.get('openai_key', '')
        
        if not user_interests:
            return jsonify({
                'success': False,
                'error': 'Research interests are required'
            }), 400
        
        if not faculty_profiles:
            return jsonify({
                'success': False,
                'error': 'No faculty profiles loaded. Please scrape or load profiles first.'
            }), 400
        
        # Initialize research matcher
        research_matcher = ResearchMatcher(openai_api_key=openai_key)
        
        # Perform matching
        matches = research_matcher.match_faculty_with_interests(faculty_profiles, user_interests)
        
        # Prepare results for frontend
        results = []
        for match in matches:
            profile = match['faculty_profile']
            results.append({
                'name': profile.get('name', 'Unknown'),
                'title': profile.get('title', ''),
                'department': profile.get('department', ''),
                'email': profile.get('email', ''),
                'similarity_score': round(match['similarity_score'], 3),
                'match_reasons': match['match_reasons'],
                'research_interests': profile.get('research_interests', []),
                'bio': profile.get('bio', '')[:200] + '...' if len(profile.get('bio', '')) > 200 else profile.get('bio', ''),
                'profile_url': profile.get('url', ''),
                'google_scholar': profile.get('google_scholar', ''),
                'research_gate': profile.get('research_gate', '')
            })
        
        return jsonify({
            'success': True,
            'matches': results,
            'total_matches': len(results),
            'total_profiles': len(faculty_profiles)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/analyze/<int:match_index>', methods=['POST'])
def analyze_faculty(match_index):
    """Get detailed analysis of a specific faculty member"""
    global faculty_profiles, research_matcher
    
    try:
        data = request.get_json()
        user_interests = data.get('interests', '')
        
        if match_index >= len(faculty_profiles):
            return jsonify({
                'success': False,
                'error': 'Invalid faculty index'
            }), 400
        
        if not research_matcher:
            return jsonify({
                'success': False,
                'error': 'Research matcher not initialized'
            }), 400
        
        # Get detailed analysis
        analysis = research_matcher.get_detailed_analysis(
            faculty_profiles[match_index], user_interests
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/export', methods=['POST'])
def export_results():
    """Export matching results"""
    try:
        data = request.get_json()
        matches = data.get('matches', [])
        format_type = data.get('format', 'json')
        
        if not matches:
            return jsonify({
                'success': False,
                'error': 'No matches to export'
            }), 400
        
        if not research_matcher:
            return jsonify({
                'success': False,
                'error': 'Research matcher not initialized'
            }), 400
        
        # Export results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == 'json':
            filename = f"faculty_matches_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(matches, f, indent=2, ensure_ascii=False)
            
            return send_file(filename, as_attachment=True)
        
        elif format_type == 'csv':
            filename = f"faculty_matches_{timestamp}.csv"
            csv_data = research_matcher.export_results(matches, 'csv')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(csv_data)
            
            return send_file(filename, as_attachment=True)
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unsupported format: {format_type}'
            }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/files')
def list_files():
    """List available data files"""
    try:
        files = []
        for filename in os.listdir('.'):
            if filename.endswith('.json') and 'faculty' in filename.lower():
                files.append({
                    'name': filename,
                    'size': os.path.getsize(filename),
                    'modified': datetime.fromtimestamp(os.path.getmtime(filename)).isoformat()
                })
        
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    
    print("Starting Faculty Research Agent...")
    print(f"Access the application at: http://localhost:{port}")
    
    # Use 0.0.0.0 for deployment, localhost for development
    host = '0.0.0.0' if os.environ.get('PORT') else 'localhost'
    
    app.run(debug=False, host=host, port=port) 