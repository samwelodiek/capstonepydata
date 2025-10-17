
import pandas as pd

# Let's search for the correct traffic volume and speed camera endpoints
TRAFFIC_ENDPOINTS = {
    # Traffic Volume Counts - let's try different resource IDs
    "traffic_volume_1": "https://data.cityofchicago.org/resource/traffic-volume-counts.json",
    "traffic_volume_2": "https://data.cityofchicago.org/resource/volume.json", 
    "traffic_volume_3": "https://data.cityofchicago.org/resource/traffic.json",
    "traffic_volume_4": "https://data.cityofchicago.org/resource/u77s-8q7s.json",  # Common ID pattern
    
    # Speed Cameras - try different resource IDs
    "speed_cameras_1": "https://data.cityofchicago.org/resource/speed-camera.json",
    "speed_cameras_2": "https://data.cityofchicago.org/resource/speed.json",
    "speed_cameras_3": "https://data.cityofchicago.org/resource/hhqg-x9hx.json",  # Common ID pattern
    
    # Real-time Traffic - might be more current
    "realtime_traffic": "https://data.cityofchicago.org/resource/t2qc-9pjd.json",
    "congestion": "https://data.cityofchicago.org/resource/n4j6-wkkf.json",
}

def test_traffic_endpoints():
    """Test various traffic-related endpoints"""
    print("🔍 Searching for Traffic Volume & Speed Camera Data")
    print("=" * 60)
    
    working_endpoints = {}
    
    for name, url in TRAFFIC_ENDPOINTS.items():
        print(f"\n📡 Testing: {name}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, params={'$limit': 2}, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    print(f"   ✅ SUCCESS! Got {len(data)} records")
                    print(f"   Sample keys: {list(data[0].keys())[:8]}")
                    
                    # Show sample data
                    df = pd.DataFrame(data)
                    print(f"   Columns: {list(df.columns)}")
                    
                    working_endpoints[name] = {
                        'url': url,
                        'sample_data': data[0],
                        'columns': list(df.columns)
                    }
                else:
                    print("   ⚠️  Empty response")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Error: {str(e)[:50]}...")

    return working_endpoints

def search_by_keyword():
    """Search for datasets by keyword in the Chicago data portal"""
    print("\n🔎 Searching for Traffic Datasets by Keyword")
    print("=" * 50)
    
    search_url = "https://data.cityofchicago.org/api/catalog/v1"
    search_params = {
        'query': 'traffic volume speed camera',
        'limit': 10
    }
    
    try:
        response = requests.get(search_url, params=search_params)
        if response.status_code == 200:
            results = response.json()
            print("📋 Found datasets:")
            for item in results.get('results', [])[:5]:
                resource = item['resource']
                print(f"\n🏷️  {resource['name']}")
                print(f"   📍 ID: {resource['id']}")
                print(f"   🔗 Endpoint: https://data.cityofchicago.org/resource/{resource['id']}.json")
                print(f"   📝 Description: {item.get('description', 'N/A')[:100]}...")
        else:
            print("Search API not available")
    except:
        print("Search API unavailable - using manual endpoints")

if __name__ == "__main__":
    working = test_traffic_endpoints()
    
    if working:
        print(f"\n🎉 Found {len(working)} working endpoints!")
        print("\nWorking endpoints:")
        for name, info in working.items():
            print(f"   {name}: {info['url']}")
    else:
        print("\n❌ No working traffic endpoints found")
        search_by_keyword()