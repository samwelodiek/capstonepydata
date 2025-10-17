import requests
import pandas as pd
import json

# Let's try different Chicago traffic datasets
DATASETS = {
    "traffic_crashes": "https://data.cityofchicago.org/resource/85ca-t3if.json",  # Traffic crashes (more recent)
    "traffic_volume": "https://data.cityofchicago.org/resource/d7gs-wdfn.json",   # Traffic volume counts
    "red_light_cameras": "https://data.cityofchicago.org/resource/spqx-js37.json", # Red light camera data
    "speed_cameras": "https://data.cityofchicago.org/resource/hhq-xns9.json",     # Speed camera data
}

def test_datasets():
    """Test different Chicago traffic datasets"""
    print("🔍 Testing Alternative Chicago Traffic Datasets")
    print("=" * 60)
    
    for name, url in DATASETS.items():
        print(f"\n Testing: {name}")
        print(f"   URL: {url}")
        print("-" * 40)
        
        try:
            response = requests.get(url, params={'$limit': 3}, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    print(f"    SUCCESS! Got {len(data)} records")
                    print(f"   Latest record date: {data[0].get('date', 'N/A')}")
                    print(f"   Sample keys: {list(data[0].keys())[:5]}...")
                    
                    # Show sample data
                    df = pd.DataFrame(data)
                    print(f"   Columns: {list(df.columns)}")
                else:
                    print("    No data returned")
            else:
                print(f"    Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   💥 Connection error: {e}")

if __name__ == "__main__":
    test_datasets()