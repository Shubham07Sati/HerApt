"""
Ultra Career Predictor for HerApt
48 features → Success Percentage (0-100%)
Uses advanced ML with better accuracy
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

class UltraCareerPredictor:
    """Advanced career prediction with success percentages"""
    
    def __init__(self):
        """Initialize predictor"""
        self.model = None
        self.preprocessor = None
        self.label_encoder = None
        self.feature_config = None
        self.numeric_features = None
        self.categorical_features = None
        
        # Load or create model
        self.load_or_create_model()
    
    def load_or_create_model(self):
        """Try to load model, create if doesn't exist"""
        try:
            self.model = joblib.load('career_rf_model_ultra.pkl')
            self.preprocessor = joblib.load('career_preprocessor_ultra.pkl')
            self.label_encoder = joblib.load('career_label_encoder_ultra.pkl')
            self.feature_config = joblib.load('feature_config_ultra.pkl')
            print("✅ Loaded existing ultra model")
        except FileNotFoundError:
            print("⚠️  Model not found. Run train_model_ultra.py first.")
            print("   Command: python train_model_ultra.py")
            exit(1)
        
        # Set features
        self.numeric_features = self.feature_config['numeric_features']
        self.categorical_features = self.feature_config['categorical_features']
    
    def validate_input(self, user_profile):
        """Validate user input"""
        required_fields = self.numeric_features + self.categorical_features
        missing = [f for f in required_fields if f not in user_profile]
        
        if missing:
            print(f"⚠️  Missing fields: {missing}")
            print("   Using default values for missing fields")
            for field in missing:
                if field in self.categorical_features:
                    user_profile[field] = 'Unknown'
                else:
                    user_profile[field] = 0
        
        return user_profile
    
    def predict(self, user_profile, top_n=5):
        """
        Predict top N careers with success percentages
        
        Args:
            user_profile: dict with all 48 features
            top_n: number of recommendations
            
        Returns:
            List of (career, success_percentage, match_score) tuples
        """
        # Validate input
        user_profile = self.validate_input(user_profile)
        
        # Prepare features
        try:
            features_num = [user_profile.get(f, 0) for f in self.numeric_features]
            features_cat = [user_profile.get(f, 'Unknown') for f in self.categorical_features]
            
            # Create DataFrame
            feature_names = self.numeric_features + self.categorical_features
            df_input = pd.DataFrame([features_num + features_cat], columns=feature_names)
            
            # Preprocess
            X_processed = self.preprocessor.transform(df_input)
            
            # Get predictions
            probabilities = self.model.predict_proba(X_processed)[0]
            
            # Get top N
            top_indices = np.argsort(probabilities)[-top_n:][::-1]
            top_careers = self.label_encoder.inverse_transform(top_indices)
            top_probs = probabilities[top_indices]
            
            # Calculate success percentages
            results = []
            for career, prob in zip(top_careers, top_probs):
                success_pct = self.calculate_success_percentage(user_profile, career, prob)
                match_score = prob * 100
                results.append((career, success_pct, match_score))
            
            return results
            
        except Exception as e:
            print(f"❌ Error in prediction: {e}")
            return []
    
    def calculate_success_percentage(self, user_profile, career, base_prob):
        """
        Calculate actual success percentage (0-100%)
        
        Formula:
        - Base probability (ML model): 40%
        - Skill match: 25%
        - Experience match: 15%
        - Goal clarity: 10%
        - Work preference alignment: 10%
        """
        
        # Base score from ML
        base_score = base_prob * 100 * 0.40
        
        # Skill match (25%)
        skills = [
            user_profile.get('Coding_Skills', 0),
            user_profile.get('Analytical_Skills', 0),
            user_profile.get('Problem_Solving_Skills', 0),
            user_profile.get('Communication_Skills', 0),
            user_profile.get('Teamwork_Skills', 0),
        ]
        skill_score = (sum(skills) / (5 * 4)) * 100 * 0.25  # Max 5 skills, each 0-4
        
        # Experience match (15%)
        exp_score = min(user_profile.get('Work_Experience_Years', 0) / 10 * 100, 100) * 0.15
        
        # Goal clarity (10%)
        clarity = user_profile.get('Career_Goal_Clarity', 3)
        clarity_score = (clarity / 5) * 100 * 0.10
        
        # Preference alignment (10%)
        pref_scores = []
        
        # Work-life balance
        wlb = user_profile.get('Work_Life_Balance_Priority', 3)
        pref_scores.append(wlb / 5)
        
        # Continuous learning
        learning = user_profile.get('Continuous_Learning', 3)
        pref_scores.append(learning / 5)
        
        # Career clarity
        clarity_align = user_profile.get('Career_Goal_Clarity', 3) / 5
        pref_scores.append(clarity_align)
        
        pref_score = (sum(pref_scores) / len(pref_scores)) * 100 * 0.10
        
        # Total
        total = base_score + skill_score + exp_score + clarity_score + pref_score
        
        # Add small randomness (±2%)
        final = total + np.random.uniform(-2, 2)
        
        # Ensure between 10% and 100%
        return round(max(min(final, 100), 10), 1)
    
    def predict_with_success_rate(self, user_profile):
        """Alias for predict method"""
        return self.predict(user_profile, top_n=5)
    
    def get_personalized_advice(self, user_profile, career):
        """Get personalized advice for a specific career"""
        
        strengths = []
        improvements = []
        
        # Analyze technical skills
        tech_skills = {
            'Coding_Skills': (user_profile.get('Coding_Skills', 0), 'Coding Proficiency'),
            'Analytical_Skills': (user_profile.get('Analytical_Skills', 0), 'Analytical Thinking'),
            'Problem_Solving_Skills': (user_profile.get('Problem_Solving_Skills', 0), 'Problem Solving'),
        }
        
        for skill_key, (score, skill_name) in tech_skills.items():
            if score >= 4:
                strengths.append(f"Strong {skill_name}")
            elif score <= 1:
                improvements.append(f"Improve {skill_name}")
        
        # Analyze soft skills
        soft_skills = {
            'Communication_Skills': (user_profile.get('Communication_Skills', 0), 'Communication'),
            'Teamwork_Skills': (user_profile.get('Teamwork_Skills', 0), 'Teamwork'),
        }
        
        for skill_key, (score, skill_name) in soft_skills.items():
            if score >= 4:
                strengths.append(f"Excellent {skill_name}")
            elif score <= 1:
                improvements.append(f"Build {skill_name}")
        
        # Check experience
        exp_years = user_profile.get('Work_Experience_Years', 0)
        if exp_years >= 5:
            strengths.append(f"Solid {exp_years} years experience")
        elif exp_years == 0:
            improvements.append("Gain practical work experience")
        
        # Check learning mindset
        learning = user_profile.get('Continuous_Learning', 0)
        if learning >= 4:
            strengths.append("Strong commitment to learning")
        
        return {
            'career': career,
            'strengths': strengths,
            'improvements': improvements,
        }


# Example usage
if __name__ == "__main__":
    print("="*80)
    print("HERAPT ULTRA CAREER PREDICTOR")
    print("="*80)
    
    predictor = UltraCareerPredictor()
    
    # Example profile
    profile = {
        # Demographics
        'Age_Group': '25-30',
        'Academic_Stream': 'Science',
        'Education_Level': 'Masters',
        'GPA': 3.7,
        
        # Experience
        'Work_Experience_Years': 5,
        'Internships': 2,
        'Projects': 5,
        'Industry_Certifications': 2,
        'Extracurricular_Activities': 3,
        
        # Career break
        'Career_Break': 0,
        'Career_Break_Months': 0,
        
        # Skills (Technical)
        'Coding_Skills': 4,
        'Analytical_Skills': 4,
        'Problem_Solving_Skills': 4,
        'Data_Driven_Thinking': 4,
        'Domain_Expertise_Depth': 3,
        
        # Skills (Soft)
        'Communication_Skills': 3,
        'Teamwork_Skills': 3,
        'Presentation_Skills': 3,
        'Networking_Skills': 2,
        'Public_Speaking_Confidence': 3,
        'Conflict_Resolution_Skills': 3,
        
        # Traits
        'Leadership_Readiness': 3,
        'Risk_Tolerance': 4,
        'Adaptability_Score': 4,
        'Stress_Management_Skills': 3,
        'Continuous_Learning': 5,
        'Innovation_Interest': 4,
        'Customer_Focus': 3,
        'Mentoring_Experience': 2,
        
        # Preferences
        'Preferred_Work_Mode': 'Hybrid',
        'Location_Preference': 'Tier1_City',
        'Work_Life_Balance_Priority': 4,
        'Industry_Preference': 'Tech',
        'Prefer_Corporate': 1,
        'Entrepreneurship_Interest': 3,
        'Salary_Expectation_Lakh': 25,
        
        # Goals
        'Career_Goal_Clarity': 4,
        'Certifications_Interest': 3,
        'English_Proficiency': 4,
        'Family_Support_Score': 4,
        'Willing_To_Relocate': 1,
        'Research_Experience': 1,
        'Leadership_Positions': 1,
        'Field_Specific_Courses': 5,
    }
    
    print("\n📊 User Profile:")
    print(f"  Education: {profile['Education_Level']} in {profile['Academic_Stream']}")
    print(f"  Experience: {profile['Work_Experience_Years']} years")
    print(f"  Coding: {profile['Coding_Skills']}/4, Analytical: {profile['Analytical_Skills']}/4")
    print(f"  Goal Clarity: {profile['Career_Goal_Clarity']}/5")
    
    print("\n🎯 TOP 5 CAREER RECOMMENDATIONS WITH SUCCESS PERCENTAGES:")
    print("-" * 80)
    
    recommendations = predictor.predict(profile)
    
    for rank, (career, success_pct, match_score) in enumerate(recommendations, 1):
        bar_filled = int(success_pct / 5)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        
        print(f"\n{rank}. {career.upper()}")
        print(f"   Success: {success_pct:.1f}% {bar}")
        print(f"   Match:   {match_score:.1f}%")
        
        # Get advice
        advice = predictor.get_personalized_advice(profile, career)
        if advice['strengths']:
            print(f"   ✓ Strengths: {', '.join(advice['strengths'][:2])}")
        if advice['improvements']:
            print(f"   → Develop: {', '.join(advice['improvements'][:2])}")
    
    print("\n" + "="*80)
