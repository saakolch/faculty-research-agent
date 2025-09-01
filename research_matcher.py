import json
import logging
from typing import List, Dict, Tuple
import openai
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from config import Config

class ResearchMatcher:
    """AI-powered research interest matcher using LLM and semantic similarity"""
    
    def __init__(self, openai_api_key: str = None):
        self.config = Config()
        self.openai_client = None
        self.sentence_model = None
        self.setup_logging()
        self.setup_models(openai_api_key)
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('matcher.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_models(self, openai_api_key: str = None):
        """Setup OpenAI client and sentence transformer model"""
        try:
            # Setup OpenAI
            api_key = openai_api_key or self.config.OPENAI_API_KEY
            if api_key:
                openai.api_key = api_key
                self.openai_client = openai
                self.logger.info("OpenAI client initialized")
            else:
                self.logger.warning("No OpenAI API key provided - LLM features will be limited")
            
            # Setup sentence transformer for semantic similarity
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.logger.info("Sentence transformer model loaded")
            
        except Exception as e:
            self.logger.error(f"Error setting up models: {e}")
    
    def analyze_research_interests(self, user_interests: str) -> Dict:
        """Analyze and structure user research interests using LLM"""
        if not self.openai_client:
            return {"interests": user_interests, "keywords": user_interests.split()}
        
        try:
            prompt = f"""
            Analyze the following research interests and extract key themes, methodologies, and specific areas:
            
            Research Interests: {user_interests}
            
            Please provide a structured analysis in JSON format with the following fields:
            - primary_areas: List of main research areas
            - methodologies: List of research methodologies mentioned
            - keywords: List of important keywords
            - specific_topics: List of specific research topics
            - interdisciplinary_connections: List of related fields
            
            Return only the JSON object, no additional text.
            """
            
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            analysis = json.loads(response.choices[0].message.content)
            self.logger.info("Successfully analyzed user research interests")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing research interests: {e}")
            return {"interests": user_interests, "keywords": user_interests.split()}
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            if not self.sentence_model:
                return 0.0
            
            # Encode texts to embeddings
            embedding1 = self.sentence_model.encode([text1])
            embedding2 = self.sentence_model.encode([text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(embedding1, embedding2)[0][0]
            return float(similarity)
            
        except Exception as e:
            self.logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def extract_faculty_research_text(self, faculty_profile: Dict) -> str:
        """Extract and combine all research-related text from faculty profile"""
        research_text = []
        
        # Add research interests
        if faculty_profile.get('research_interests'):
            research_text.extend(faculty_profile['research_interests'])
        
        # Add bio
        if faculty_profile.get('bio'):
            research_text.append(faculty_profile['bio'])
        
        # Add publications (first few for analysis)
        if faculty_profile.get('publications'):
            publications = faculty_profile['publications'][:5]  # Limit to first 5
            research_text.extend(publications)
        
        # Add title and department
        if faculty_profile.get('title'):
            research_text.append(faculty_profile['title'])
        if faculty_profile.get('department'):
            research_text.append(faculty_profile['department'])
        
        return ' '.join(research_text)
    
    def match_faculty_with_interests(self, faculty_profiles: List[Dict], user_interests: str) -> List[Dict]:
        """Match faculty profiles with user research interests"""
        try:
            # Analyze user interests
            interest_analysis = self.analyze_research_interests(user_interests)
            
            # Prepare user interest text for comparison
            user_interest_text = user_interests
            if isinstance(interest_analysis, dict) and 'keywords' in interest_analysis:
                user_interest_text += ' ' + ' '.join(interest_analysis['keywords'])
            
            matches = []
            
            for profile in faculty_profiles:
                if not profile.get('name'):
                    continue
                
                # Extract faculty research text
                faculty_research_text = self.extract_faculty_research_text(profile)
                
                if not faculty_research_text.strip():
                    continue
                
                # Calculate semantic similarity
                similarity_score = self.calculate_semantic_similarity(
                    user_interest_text, faculty_research_text
                )
                
                # Only include matches above threshold
                if similarity_score >= self.config.SIMILARITY_THRESHOLD:
                    match_data = {
                        'faculty_profile': profile,
                        'similarity_score': similarity_score,
                        'match_reasons': self.generate_match_reasons(
                            profile, interest_analysis, similarity_score
                        )
                    }
                    matches.append(match_data)
            
            # Sort by similarity score (highest first)
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Limit results
            matches = matches[:self.config.MAX_RESULTS]
            
            self.logger.info(f"Found {len(matches)} matching faculty members")
            return matches
            
        except Exception as e:
            self.logger.error(f"Error matching faculty with interests: {e}")
            return []
    
    def generate_match_reasons(self, faculty_profile: Dict, interest_analysis: Dict, similarity_score: float) -> List[str]:
        """Generate specific reasons why a faculty member matches user interests"""
        reasons = []
        
        try:
            if not self.openai_client:
                # Fallback to simple keyword matching
                faculty_text = self.extract_faculty_research_text(faculty_profile).lower()
                if isinstance(interest_analysis, dict) and 'keywords' in interest_analysis:
                    for keyword in interest_analysis['keywords']:
                        if keyword.lower() in faculty_text:
                            reasons.append(f"Research involves {keyword}")
                return reasons
            
            # Use LLM to generate specific match reasons
            faculty_text = self.extract_faculty_research_text(faculty_profile)
            
            prompt = f"""
            Given a faculty member's research profile and user interests, provide 2-3 specific reasons why they would be a good match.
            
            Faculty Profile:
            Name: {faculty_profile.get('name', 'Unknown')}
            Title: {faculty_profile.get('title', '')}
            Department: {faculty_profile.get('department', '')}
            Research Interests: {', '.join(faculty_profile.get('research_interests', []))}
            Bio: {faculty_profile.get('bio', '')[:500]}...
            
            User Interests: {interest_analysis.get('interests', '')}
            
            Similarity Score: {similarity_score:.3f}
            
            Provide 2-3 specific, concise reasons for the match. Focus on concrete research areas, methodologies, or topics that align.
            Return as a JSON array of strings.
            """
            
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            
            reasons = json.loads(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"Error generating match reasons: {e}")
            reasons = [f"Semantic similarity score: {similarity_score:.3f}"]
        
        return reasons 