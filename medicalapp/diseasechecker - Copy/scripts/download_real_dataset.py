"""
Download REAL medical dataset from Hugging Face
Source: shanover/disease_symptoms_prec_full
Contains: Disease + Symptoms + Precautions
"""

import pandas as pd
import os
import json

def download_real_dataset():
    """Download the disease-symptoms-precautions dataset from Hugging Face"""
    
    print("="*60)
    print("📥 Downloading REAL Medical Dataset")
    print("="*60)
    
    # The dataset is available via Hugging Face datasets library
    try:
        from datasets import load_dataset
        
        print("\n🔄 Loading dataset from Hugging Face...")
        dataset = load_dataset("shanover/disease_symptoms_prec_full", split="train")
        
        # Convert to pandas DataFrame
        df = dataset.to_pandas()
        
        print(f"✅ Loaded {len(df)} disease records")
        print(f"📊 Columns: {list(df.columns)}")
        
        return df
        
    except ImportError:
        print("⚠️ datasets library not installed. Installing...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "datasets"])
        
        # Try again
        from datasets import load_dataset
        dataset = load_dataset("shanover/disease_symptoms_prec_full", split="train")
        df = dataset.to_pandas()
        return df
    
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        print("\n📋 Manual download option:")
        print("   Visit: https://huggingface.co/datasets/shanover/disease_symptoms_prec_full")
        print("   Download the CSV files manually to ./data/ folder")
        return None

def prepare_training_data(df):
    """Convert the dataset to training format"""
    
    training_data = []
    disease_precautions = {}
    
    for _, row in df.iterrows():
        disease = row['disease']
        symptoms_str = row['symptoms']
        precautions_str = row['precautions']
        
        # Parse symptoms (underscore-separated, convert to readable format)
        if pd.notna(symptoms_str):
            symptoms = [s.strip().replace('_', ' ') for s in symptoms_str.split(',')]
        else:
            symptoms = []
        
        # Parse precautions
        if pd.notna(precautions_str):
            precautions = [p.strip() for p in precautions_str.split(',')]
        else:
            precautions = ["Consult a doctor", "Get adequate rest", "Stay hydrated", "Follow prescribed treatment"]
        
        if symptoms and disease:
            training_data.append({
                "symptoms": symptoms,
                "disease": disease,
                "precautions": precautions,
                "source": "HuggingFace Medical Dataset"
            })
            
            disease_precautions[disease] = precautions
    
    return training_data, disease_precautions

def save_data(training_data, disease_precautions):
    """Save the processed data"""
    
    os.makedirs("data", exist_ok=True)
    os.makedirs("model", exist_ok=True)
    
    # Save training data as JSON
    with open("data/real_training_data.json", "w") as f:
        json.dump(training_data, f, indent=2)
    
    # Save precautions mapping
    with open("data/disease_precautions_real.json", "w") as f:
        json.dump(disease_precautions, f, indent=2)
    
    # Also save as CSV for easy viewing
    records = []
    for item in training_data:
        records.append({
            "disease": item["disease"],
            "symptoms": ", ".join(item["symptoms"]),
            "precautions": " | ".join(item["precautions"])
        })
    
    df_out = pd.DataFrame(records)
    df_out.to_csv("data/real_medical_dataset.csv", index=False)
    
    print(f"\n💾 Saved files:")
    print(f"   - data/real_training_data.json ({len(training_data)} records)")
    print(f"   - data/disease_precautions_real.json ({len(disease_precautions)} diseases)")
    print(f"   - data/real_medical_dataset.csv")

def display_sample(df):
    """Display sample of the dataset"""
    print("\n" + "="*60)
    print("📊 DATASET SAMPLE")
    print("="*60)
    
    for i, row in df.head(10).iterrows():
        print(f"\n{i+1}. 🩺 {row['disease']}")
        
        symptoms = [s.replace('_', ' ') for s in row['symptoms'].split(',')]
        print(f"   Symptoms: {', '.join(symptoms[:6])}")
        if len(symptoms) > 6:
            print(f"     ... and {len(symptoms)-6} more")
        
        precautions = row['precautions'].split(',')
        print(f"   Precautions: {precautions[0]}...")
    print("\n" + "="*60)

if __name__ == "__main__":
    # Download and process
    df = download_real_dataset()
    
    if df is not None:
        # Display sample
        display_sample(df)
        
        # Prepare training data
        training_data, precautions = prepare_training_data(df)
        
        print(f"\n📈 Dataset Statistics:")
        print(f"   - Total diseases: {len(training_data)}")
        print(f"   - Unique diseases: {len(precautions)}")
        print(f"   - Avg symptoms per disease: {sum(len(d['symptoms']) for d in training_data) / len(training_data):.1f}")
        
        # Save processed data
        save_data(training_data, precautions)
        
        print("\n✅ Dataset ready for training!")
        print("\nNext step: Update your model to use this data")