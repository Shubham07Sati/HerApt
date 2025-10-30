"""
HerApt Career Assessment Questionnaire
Interactive form that asks users detailed questions
Returns career predictions with SUCCESS PERCENTAGE (0-100%)
"""

from career_predictor_ultra import UltraCareerPredictor
import json

class CareerAssessmentForm:
    def __init__(self):
        self.predictor = UltraCareerPredictor()
        self.answers = {}
    
    def display_welcome(self):
        """Welcome message"""
        print("\n" + "="*80)
        print(" HERAPT CAREER ASSESSMENT - INTERACTIVE QUESTIONNAIRE")
        print("="*80)
        print("\nWelcome! This comprehensive assessment will help us recommend")
        print("the perfect career paths for you based on 48 different factors.\n")
        print("  Estimated time: 10-15 minutes")
        print(" Answer honestly for best results!\n")
        input("Press Enter to begin...")
    
    def question_numeric(self, key, question, min_val, max_val, unit=""):
        """Ask numeric question"""
        while True:
            try:
                response = input(f"\n{question} ({min_val}-{max_val}{unit}): ").strip()
                value = float(response)
                if min_val <= value <= max_val:
                    self.answers[key] = value
                    return value
                else:
                    print(f" Please enter a value between {min_val} and {max_val}")
            except ValueError:
                print(" Invalid input. Please enter a number.")
    
    def question_choice(self, key, question, options):
        """Ask multiple choice question"""
        print(f"\n{question}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input("Your choice (1-{}): ".format(len(options))))
                if 1 <= choice <= len(options):
                    self.answers[key] = options[choice - 1]
                    return options[choice - 1]
                else:
                    print(f" Please choose between 1 and {len(options)}")
            except ValueError:
                print(" Invalid input. Please enter a number.")
    
    def question_scale(self, key, question, scale=5):
        """Ask 1-5 scale question"""
        print(f"\n{question}")
        print(f"  1 = Strongly Disagree")
        for i in range(2, scale):
            print(f"  {i} = {'Neutral' if i == (scale//2 + 1) else ''}")
        print(f"  {scale} = Strongly Agree")
        
        while True:
            try:
                response = int(input(f"Your rating (1-{scale}): "))
                if 1 <= response <= scale:
                    self.answers[key] = response
                    return response
                else:
                    print(f" Please choose between 1 and {scale}")
            except ValueError:
                print(" Invalid input.")
    
    def run_assessment(self):
        """Run complete assessment"""
        self.display_welcome()
        
        
        print("\n" + "="*80)
        print("SECTION 1: BASIC INFORMATION")
        print("="*80)
        
        self.question_choice('Age_Group', 
            "What is your age group?",
            ['18-24', '25-30', '31-35', '36-40', '40+'])
        
        self.question_choice('Academic_Stream',
            "What was your academic stream?",
            ['Science (PCM/PCB)', 'Commerce', 'Arts/Humanities', 'Interdisciplinary'])
        
        self.question_choice('Education_Level',
            "Highest education level completed:",
            ['High School (10th/12th)', 'Bachelors Degree', 'Masters Degree', 'PhD/Doctorate'])
        
        self.question_numeric('GPA', 
            "Your GPA/Percentage (on 4.0 scale)", 0, 4.0)
        
        
        print("\n" + "="*80)
        print("SECTION 2: EXPERIENCE & BACKGROUND")
        print("="*80)
        
        self.question_numeric('Work_Experience_Years',
            "Years of work experience", 0, 30)
        
        self.question_numeric('Internships',
            "Number of internships completed", 0, 10)
        
        self.question_numeric('Projects',
            "Number of projects you've worked on", 0, 20)
        
        self.question_numeric('Industry_Certifications',
            "Number of professional certifications", 0, 20)
        
        self.question_numeric('Extracurricular_Activities',
            "Extracurricular activities you've participated in", 0, 20)
        
        
        print("\n" + "="*80)
        print("SECTION 3: CAREER BREAK (If Applicable)")
        print("="*80)
        
        self.question_choice('Career_Break',
            "Have you taken a career break?",
            ['No', 'Yes'])
        
        if self.answers['Career_Break'] == 'Yes':
            self.question_numeric('Career_Break_Months',
                "Duration of career break (months)", 1, 120)
            self.answers['Career_Break'] = 1
        else:
            self.answers['Career_Break_Months'] = 0
            self.answers['Career_Break'] = 0
        
        
        print("\n" + "="*80)
        print("SECTION 4: TECHNICAL SKILLS")
        print("="*80)
        
        self.question_scale('Coding_Skills',
            "Rate your coding/programming skills", 5)
        
        self.question_scale('Analytical_Skills',
            "Rate your analytical thinking ability", 5)
        
        self.question_scale('Problem_Solving_Skills',
            "Rate your problem-solving skills", 5)
        
        self.question_scale('Data_Driven_Thinking',
            "I make decisions based on data and metrics", 5)
        
        self.question_scale('Domain_Expertise_Depth',
            "Deep expertise in your field/domain", 5)
        
        
        print("\n" + "="*80)
        print("SECTION 5: SOFT SKILLS")
        print("="*80)
        
        self.question_scale('Communication_Skills',
            "Rate your communication skills", 5)
        
        self.question_scale('Teamwork_Skills',
            "Rate your ability to work in teams", 5)
        
        self.question_scale('Presentation_Skills',
            "Rate your presentation skills", 5)
        
        self.question_scale('Networking_Skills',
            "Rate your networking and relationship-building skills", 5)
        
        self.question_scale('Public_Speaking_Confidence',
            "Confident speaking in front of large audiences", 5)
        
        self.question_scale('Conflict_Resolution_Skills',
            "Rate your conflict resolution abilities", 5)
        
        
        print("\n" + "="*80)
        print("SECTION 6: PERSONALITY & TRAITS")
        print("="*80)
        
        self.question_scale('Leadership_Readiness',
            "Ready to take on leadership roles", 5)
        
        self.question_scale('Risk_Tolerance',
            "Comfortable taking calculated risks", 5)
        
        self.question_scale('Adaptability_Score',
            "Able to adapt to changing situations", 5)
        
        self.question_scale('Stress_Management_Skills',
            "Good at managing stress and pressure", 5)
        
        self.question_scale('Continuous_Learning',
            "Committed to continuous learning and development", 5)
        
        self.question_scale('Innovation_Interest',
            "Interested in innovation and new ideas", 5)
        
        self.question_scale('Customer_Focus',
            "Customer satisfaction is important to me", 5)
        
        self.question_scale('Mentoring_Experience',
            "Experience mentoring others", 5)
        
        
        print("\n" + "="*80)
        print("SECTION 7: CAREER PREFERENCES")
        print("="*80)
        
        self.question_choice('Preferred_Work_Mode',
            "Preferred work mode:",
            ['Remote', 'Hybrid', 'Office', 'Flexible'])
        
        self.question_choice('Location_Preference',
            "Location preference:",
            ['Metro Cities (Tier 1)', 'Big Cities (Tier 2)', 'Smaller Cities (Tier 3)', 'Any Location'])
        
        self.question_scale('Work_Life_Balance_Priority',
            "Work-life balance is very important to me", 5)
        
        self.question_choice('Industry_Preference',
            "Preferred industry/sector:",
            ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Education', 'No Preference'])
        
        self.question_choice('Prefer_Corporate',
            "Prefer corporate or startup environment?",
            ['Startup (Dynamic, Fast-paced)', 'Corporate (Structured, Stable)'])
        
        self.question_scale('Entrepreneurship_Interest',
            "Interest in starting your own business", 5)
        
        self.question_numeric('Salary_Expectation_Lakh',
            "Expected salary (in lakh per annum)", 1, 100)
        
        
        print("\n" + "="*80)
        print("SECTION 8: GOALS & FAMILY SUPPORT")
        print("="*80)
        
        self.question_scale('Career_Goal_Clarity',
            "Clear about your career goals", 5)
        
        self.question_scale('Certifications_Interest',
            "Interested in pursuing certifications", 5)
        
        self.question_scale('English_Proficiency',
            "English language proficiency", 5)
        
        self.question_scale('Family_Support_Score',
            "Family is supportive of your career choices", 5)
        
        self.question_choice('Willing_To_Relocate',
            "Willing to relocate for a job?",
            ['No', 'Yes'])
        
        self.answers['Willing_To_Relocate'] = 0 if self.answers['Willing_To_Relocate'] == 'No' else 1
        
        
        self.answers['Prefer_Corporate'] = 0 if self.answers['Prefer_Corporate'] == 'Startup (Dynamic, Fast-paced)' else 1
        
        print("\n" + "="*80)
        print(" ASSESSMENT COMPLETE!")
        print("="*80)
        print("\nAnalyzing your profile and generating career recommendations...")
        print("(This may take a moment...)\n")
        
        return self.get_predictions()
    
    def get_predictions(self):
        """Get career predictions with success percentage"""
        try:
            recommendations = self.predictor.predict_with_success_rate(self.answers)
            return recommendations
        except Exception as e:
            print(f" Error getting predictions: {e}")
            return None
    
    def display_results(self, recommendations):
        """Display results beautifully"""
        if not recommendations:
            print(" Could not generate recommendations")
            return
        
        print("\n" + "="*80)
        print(" YOUR PERSONALIZED CAREER RECOMMENDATIONS")
        print("="*80)
        
        print(f"\nBased on your 48-factor profile analysis:\n")
        
        for rank, (career, success_pct, match_score) in enumerate(recommendations[:5], 1):
            print(f"{rank}. {career.upper()}")
            print(f"   Success Probability: {success_pct:.1f}%", end="")
            
            
            bar_filled = int(success_pct / 5)
            bar_empty = 20 - bar_filled
            print(f"  {'█' * bar_filled}{'░' * bar_empty}")
            
            print(f"   Match Score: {match_score:.1f}%")
            
            
            if success_pct >= 75:
                interpretation = "🟢 Excellent Fit - Highly Recommended"
            elif success_pct >= 60:
                interpretation = "🟡 Good Fit - Strong Match"
            elif success_pct >= 45:
                interpretation = "🟠 Moderate Fit - Viable Option"
            else:
                interpretation = "🔴 Low Fit - Not Ideal"
            
            print(f"   {interpretation}\n")
        
        print("="*80)
        print("\n WHAT THIS MEANS:")
        print("   - Success Probability: Likelihood of success in this career")
        print("   - Match Score: How well your profile aligns with the career")
        print("   - Based on 48 factors: skills, experience, goals, preferences, traits")
        
        print("\n NEXT STEPS:")
        print("   1. Select your top choice career")
        print("   2. Get personalized upskilling plan")
        print("   3. Connect with a mentor in that field")
        print("   4. Track your progress toward this goal")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    form = CareerAssessmentForm()
    recommendations = form.run_assessment()
    form.display_results(recommendations)
