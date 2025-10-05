"""
Serverless Function for Processing Nutritional Data from Azurite Blob Storage
Task 3: Cloud-Native Data Processing with Serverless Functions
"""

from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os
from datetime import datetime

def process_nutritional_data_from_azurite():
    """
    Simulated serverless function that:
    1. Reads CSV from Azurite Blob Storage
    2. Calculates average macros per diet type
    3. Stores results in simulated NoSQL database (JSON file)
    """
    
    print(f"[{datetime.now()}] Starting serverless function execution...")
    
    # Azurite connection string (default credentials)
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    
    try:
        # Connect to Azurite Blob Storage
        print("[INFO] Connecting to Azurite Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Configuration
        container_name = 'datasets'
        blob_name = 'All_Diets.csv'
        
        # Get blob client
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        print(f"[INFO] Downloading blob: {blob_name} from container: {container_name}")
        
        # Download blob content
        stream = blob_client.download_blob().readall()
        print(f"[SUCCESS] Downloaded {len(stream)} bytes from Azurite")
        
        # Load data into pandas DataFrame
        df = pd.read_csv(io.BytesIO(stream))
        print(f"[INFO] Loaded {len(df)} rows from CSV")
        print(f"[INFO] Columns: {list(df.columns)}")
        
        # Data processing: Calculate average macros per diet type
        print("[INFO] Calculating average macronutrients per diet type...")
        avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
        
        # Additional insights
        diet_counts = df['Diet_type'].value_counts()
        total_calories_avg = df.groupby('Diet_type')['Calories'].mean()
        
        # Prepare results for NoSQL storage
        results = {
            'timestamp': datetime.now().isoformat(),
            'source_file': blob_name,
            'total_records_processed': len(df),
            'diet_types_analyzed': len(avg_macros),
            'average_macros': avg_macros.reset_index().to_dict(orient='records'),
            'diet_type_counts': diet_counts.to_dict(),
            'average_calories_per_diet': total_calories_avg.to_dict()
        }
        
        # Create directory for simulated NoSQL storage
        os.makedirs('simulated_nosql', exist_ok=True)
        
        # Save to JSON (simulating NoSQL database)
        output_file = 'simulated_nosql/results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[SUCCESS] Results saved to {output_file}")
        
        # Print summary
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Total records processed: {len(df)}")
        print(f"Diet types analyzed: {len(avg_macros)}")
        print("\nAverage Macronutrients by Diet Type:")
        print(avg_macros.to_string())
        print("="*60)
        
        return {
            'status': 'success',
            'message': 'Data processed and stored successfully',
            'records_processed': len(df),
            'output_file': output_file
        }
        
    except Exception as e:
        error_msg = f"[ERROR] Function execution failed: {str(e)}"
        print(error_msg)
        return {
            'status': 'error',
            'message': error_msg
        }

def main():
    """Main entry point for the serverless function"""
    print("="*60)
    print("SERVERLESS FUNCTION: Nutritional Data Processor")
    print("="*60)
    
    result = process_nutritional_data_from_azurite()
    
    print("\n" + "="*60)
    print("FUNCTION EXECUTION RESULT")
    print("="*60)
    print(json.dumps(result, indent=2))
    print("="*60)
    
    return result

if __name__ == "__main__":
    main()