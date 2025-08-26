#!/usr/bin/env python3
"""
Manual Model Registration Script

Since GitHub Actions can't access the API due to IP restrictions,
use this script to register models manually from your local machine.

Usage: python manual-model-register.py
"""

import json
import requests
import time
import sys

def register_model_manually():
    """Register model manually from local machine"""
    
    api_url = "https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager"
    
    # Same configuration as would be used in GitHub Actions
    config = {
        "model_name": "mlt-batch",
        "variant": f"sllim-tg-pkg-300-manual-{int(time.time())}",
        "owner_team": "personalization",
        "omd_business_service": "content-discovery",
        "related_features": {},
        "inference_configuration": {
            "response_item_limit": -1
        },
        "serving_configuration": {
            "autoscaling": True,
            "autoscale_conditions": {
                "rps": 20
            },
            "min_instance": 1,
            "max_instance": 5,
            "machine_type": "ml.c5.xlarge",
            "processor": "cpu",
            "framework": {
                "framework_name": "tensorflow",
                "framework_version": "2.9.2"
            },
            "shadow_config": {}
        },
        "serving_regions": ["us-east-1"]
    }
    
    headers = {'Content-Type': 'application/json'}
    register_url = f"{api_url}/v1/models/register"
    
    print("🚀 MANUAL MODEL REGISTRATION")
    print("=" * 50)
    print(f"Model: {config['model_name']}")
    print(f"Variant: {config['variant']}")
    print(f"API URL: {register_url}")
    print()
    print("Registering model...")
    
    try:
        response = requests.post(register_url, json=config, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ SUCCESS: Model registered successfully!")
            response_data = response.json()
            model_id = response_data.get('response', {}).get('id', 'Unknown')
            print(f"📋 Model ID: {model_id}")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print("ℹ️ Model variant already exists - this is normal")
            print("✅ SUCCESS: Registration completed (model exists)")
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: Request error: {e}")
        return False

def update_model_manually():
    """Update model configuration manually"""
    
    api_url = "https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager"
    model_id = "CD:personalization:mlt-batch:sllim-tg-pkg-3"
    
    # Update payload (only serving_configuration)
    update_payload = {
        "model": {
            "serving_configuration": {
                "autoscaling": True,
                "autoscale_conditions": {
                    "rps": 10  # Changed from 20 to 10
                },
                "min_instance": 1,
                "max_instance": 30,  # Increased from 5 to 30
                "machine_type": "ml.c5.xlarge",
                "processor": "cpu",
                "framework": {
                    "framework_name": "tensorflow",
                    "framework_version": "2.9.2"
                },
                "shadow_config": {}
            }
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    update_url = f"{api_url}/v1/models/update/{model_id}"
    
    print("🔄 MANUAL MODEL UPDATE")
    print("=" * 50)
    print(f"Model ID: {model_id}")
    print(f"API URL: {update_url}")
    print()
    print("Updating model...")
    
    try:
        response = requests.put(update_url, json=update_payload, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ SUCCESS: Model updated successfully!")
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: Request error: {e}")
        return False

def main():
    print("🤖 MANUAL MODEL DEPLOYMENT")
    print("Since GitHub Actions can't access the API due to IP restrictions,")
    print("use this script to register/update models from your local machine.")
    print("=" * 60)
    
    while True:
        print("\nChoose an action:")
        print("1. Register new model")
        print("2. Update existing model")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print()
            success = register_model_manually()
            if success:
                print("\n🎉 Model registration completed!")
            else:
                print("\n❌ Model registration failed!")
                
        elif choice == "2":
            print()
            success = update_model_manually()
            if success:
                print("\n🎉 Model update completed!")
            else:
                print("\n❌ Model update failed!")
                
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library not found.")
        print("Please install it with: pip install requests")
        print("Or use virtual environment:")
        print("  python3 -m venv env")
        print("  source env/bin/activate")
        print("  pip install requests")
        sys.exit(1)
    
    main()
