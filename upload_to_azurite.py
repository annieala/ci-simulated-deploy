"""
Upload CSV File to Azurite Blob Storage Emulator
Utility script to upload All_Diets.csv to local Azurite
"""

from azure.storage.blob import BlobServiceClient
from datetime import datetime
import os

def upload_csv_to_azurite(csv_file='All_Diets.csv'):
    """
    Upload CSV file to Azurite blob storage
    
    Args:
        csv_file: Path to the CSV file to upload
    """
    
    print("="*60)
    print("AZURITE BLOB UPLOAD UTILITY")
    print("="*60)
    print(f"Timestamp: {datetime.now()}")
    print(f"File to upload: {csv_file}")
    print("="*60 + "\n")
    
    # Azurite connection string (default credentials)
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    
    try:
        # Check if file exists
        if not os.path.exists(csv_file):
            print(f"[ERROR] File not found: {csv_file}")
            return False
        
        file_size = os.path.getsize(csv_file)
        print(f"[INFO] File size: {file_size:,} bytes")
        
        # Create blob service client
        print("[INFO] Connecting to Azurite Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Create container
        container_name = 'datasets'
        print(f"[INFO] Creating container: {container_name}")
        
        try:
            container_client = blob_service_client.create_container(container_name)
            print(f"[SUCCESS] Container '{container_name}' created")
        except Exception as e:
            if "ContainerAlreadyExists" in str(e):
                print(f"[INFO] Container '{container_name}' already exists")
                container_client = blob_service_client.get_container_client(container_name)
            else:
                raise e
        
        # Upload file
        blob_name = os.path.basename(csv_file)
        print(f"[INFO] Uploading blob: {blob_name}")
        
        blob_client = container_client.get_blob_client(blob_name)
        
        with open(csv_file, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"[SUCCESS] File '{blob_name}' uploaded successfully!")
        
        # Verify upload
        print("\n[INFO] Verifying upload...")
        blob_properties = blob_client.get_blob_properties()
        print(f"[VERIFICATION] Blob size: {blob_properties.size:,} bytes")
        print(f"[VERIFICATION] Content type: {blob_properties.content_settings.content_type}")
        print(f"[VERIFICATION] Last modified: {blob_properties.last_modified}")
        
        # List all blobs in container
        print("\n[INFO] Listing all blobs in container:")
        blob_list = container_client.list_blobs()
        for i, blob in enumerate(blob_list, 1):
            print(f"  {i}. {blob.name} ({blob.size:,} bytes)")
        
        print("\n" + "="*60)
        print("UPLOAD COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Container: {container_name}")
        print(f"Blob Name: {blob_name}")
        print(f"Endpoint: http://127.0.0.1:10000/devstoreaccount1/{container_name}/{blob_name}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Upload failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure Azurite is running: azurite")
        print("2. Check if port 10000 is available: netstat -tuln | grep 10000")
        print("3. Verify CSV file exists in current directory")
        return False

def list_blobs_in_azurite():
    """List all blobs in Azurite storage"""
    
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client('datasets')
        
        print("\n" + "="*60)
        print("BLOBS IN AZURITE STORAGE")
        print("="*60)
        
        blob_list = container_client.list_blobs()
        for i, blob in enumerate(blob_list, 1):
            print(f"{i}. {blob.name}")
            print(f"   Size: {blob.size:,} bytes")
            print(f"   Modified: {blob.last_modified}")
            print()
        
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Could not list blobs: {e}")

def main():
    """Main entry point"""
    
    import sys
    
    # Get CSV file from command line or use default
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'All_Diets.csv'
    
    # Upload file
    success = upload_csv_to_azurite(csv_file)
    
    if success:
        # List all blobs
        list_blobs_in_azurite()
        
        print("\n Next steps:")
        print("1. Run the serverless function: python3 lambda_function.py")
        print("2. Or start the event watcher: python3 blob_watcher.py")
    else:
        print("\n Upload failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())