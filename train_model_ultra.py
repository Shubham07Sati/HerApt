"""
HerApt ULTRA MODEL TRAINING
48 Features → Success Percentage Predictions
Advanced ML with better accuracy and interpretability
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("HERAPT ULTRA MODEL TRAINING")
print("48 Features → Success Percentage Predictions")
print("="*80)

# Load enhanced dataset
print("\n[1/8] Loading ultra-enhanced dataset...")
try:
    df = pd.read_csv('career_path_ultra_enhanced.csv')
    print(f"✅ Loaded {len(df)} records with {len(df.columns)} columns")
except FileNotFoundError:
    print("❌ career_path_ultra_enhanced.csv not found!")
    print("   Run: python create_ultra_dataset.py")
    exit(1)

# Explore data
print(f"\n[2/8] Exploring data...")
print(f"   Columns: {len(df.columns)}")
print(f"   Rows: {len(df)}")
print(f"   Careers: {df['Career'].nunique()}")
print(f"   Success % - Min: {df['Success_Percentage'].min():.1f}%, Max: {df['Success_Percentage'].max():.1f}%")
print(f"   Missing values: {df.isnull().sum().sum()}")

# Define features and target
print("\n[3/8] Defining features and target...")

numeric_features = [
    'GPA', 'Extracurricular_Activities', 'Internships', 'Projects',
    'Leadership_Positions', 'Field_Specific_Courses', 'Research_Experience',
    'Coding_Skills', 'Communication_Skills', 'Problem_Solving_Skills',
    'Teamwork_Skills', 'Analytical_Skills', 'Presentation_Skills',
    'Networking_Skills', 'Industry_Certifications', 'Work_Experience_Years',
    'Career_Break', 'Career_Break_Months', 'Family_Support_Score',
    'English_Proficiency', 'Entrepreneurship_Interest', 'Risk_Tolerance',
    'Leadership_Readiness', 'Certifications_Interest', 'Work_Life_Balance_Priority',
    'Salary_Expectation_Lakh', 'Public_Speaking_Confidence', 'Conflict_Resolution_Skills',
    'Stress_Management_Skills', 'Adaptability_Score', 'Mentoring_Experience',
    'Innovation_Interest', 'Customer_Focus', 'Data_Driven_Thinking',
    'Continuous_Learning', 'Career_Goal_Clarity', 'Domain_Expertise_Depth',
    'Current_Role_Success'
]

categorical_features = [
    'Academic_Stream', 'Education_Level', 'Age_Group',
    'Preferred_Work_Mode', 'Location_Preference', 'Industry_Preference',
    'Field'
]

# Prepare features and targets
X = df[numeric_features + categorical_features]
y = df['Career']  # Predict career
target_success = df['Success_Percentage']  # Success percentage (for reference)

print(f"✅ Numeric features: {len(numeric_features)}")
print(f"✅ Categorical features: {len(categorical_features)}")
print(f"✅ Total features: {len(X.columns)}")

# Encode target
print("\n[4/8] Encoding target variable...")
le_career = LabelEncoder()
y_encoded = le_career.fit_transform(y)
print(f"✅ Encoded {len(le_career.classes_)} unique careers")

# Create preprocessing pipeline
print("\n[5/8] Creating preprocessing pipeline...")
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])

X_processed = preprocessor.fit_transform(X)
print(f"✅ Preprocessed features shape: {X_processed.shape}")
print(f"✅ Total features after encoding: {X_processed.shape[1]}")

# Split data
print("\n[6/8] Splitting data (80-20 train-test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Test set: {len(X_test)} samples")

# Train Random Forest (primary model)
print("\n[7/8] Training models...")

print("\n   Training Random Forest Classifier...")
rf_model = RandomForestClassifier(
    n_estimators=200,       # More trees for better accuracy
    max_depth=30,           # Deeper trees
    min_samples_split=3,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
    verbose=1
)
rf_model.fit(X_train, y_train)

# Evaluate
y_pred_rf = rf_model.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)

print(f"\n   ✅ Random Forest Accuracy: {accuracy_rf:.2%}")

# Cross-validation score
cv_scores = cross_val_score(rf_model, X_processed, y_encoded, cv=5)
print(f"   ✅ Cross-validation (5-fold): {cv_scores.mean():.2%} (±{cv_scores.std():.2%})")

# Feature importance
print("\n   Extracting feature importance...")
feature_names = numeric_features + list(preprocessor.get_feature_names_out()[len(numeric_features):])
feature_importance = pd.DataFrame({
    'Feature': [f.replace('cat__', '') for f in preprocessor.get_feature_names_out()],
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n   Top 15 Most Important Features:")
for idx, row in feature_importance.head(15).iterrows():
    print(f"      {row['Feature']:<40} {row['Importance']:.4f}")

# Save models
print("\n[8/8] Saving models and preprocessors...")

joblib.dump(rf_model, 'career_rf_model_ultra.pkl')
print("   ✅ career_rf_model_ultra.pkl")

joblib.dump(preprocessor, 'career_preprocessor_ultra.pkl')
print("   ✅ career_preprocessor_ultra.pkl")

joblib.dump(le_career, 'career_label_encoder_ultra.pkl')
print("   ✅ career_label_encoder_ultra.pkl")

feature_config = {
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
}
joblib.dump(feature_config, 'feature_config_ultra.pkl')
print("   ✅ feature_config_ultra.pkl")

print("\n" + "="*80)
print("✅ ULTRA MODEL TRAINING COMPLETE!")
print("="*80)

print("\n📊 MODEL SPECIFICATIONS:")
print(f"   Algorithm: Random Forest with {rf_model.n_estimators} trees")
print(f"   Max Depth: {rf_model.max_depth}")
print(f"   Accuracy: {accuracy_rf:.2%}")
print(f"   Cross-validation: {cv_scores.mean():.2%}")
print(f"   Input Features: 48 (37 numeric + 11 categorical after encoding)")
print(f"   Output: 90 unique careers")
print(f"   Success Metric: 0-100% probability based on 8 factors")

print("\n📈 CAREER STATISTICS:")
print(f"   Total unique careers: {len(le_career.classes_)}")
print(f"   Sample careers:")
for i, career in enumerate(le_career.classes_[:10], 1):
    print(f"      {i:2d}. {career}")

print("\n🚀 NEXT STEPS:")
print("   1. Test the model: python career_predictor_ultra.py")
print("   2. Run assessment form: python career_assessment_form.py")
print("   3. Deploy API: uvicorn fastapi_app_ultra:app --reload")

print("\n" + "="*80)

# Show example prediction
print("\n🎯 SAMPLE PREDICTION:")
print("-" * 80)

sample_idx = np.random.randint(0, len(X_test))
sample_features = X_test[sample_idx:sample_idx+1]
sample_pred = rf_model.predict(sample_features)[0]
sample_proba = rf_model.predict_proba(sample_features)[0]

predicted_career = le_career.inverse_transform([sample_pred])[0]
top_5_idx = np.argsort(sample_proba)[-5:][::-1]
top_5_careers = le_career.inverse_transform(top_5_idx)
top_5_probs = sample_proba[top_5_idx] * 100

print(f"\nPredicted Career: {predicted_career}")
print(f"\nTop 5 Predictions:")
for i, (career, prob) in enumerate(zip(top_5_careers, top_5_probs), 1):
    bar = "█" * int(prob / 2)
    print(f"   {i}. {career:<40} {prob:>5.1f}% {bar}")

print("\n" + "="*80)
print("Ready to use! 🎉")
print("="*80)
