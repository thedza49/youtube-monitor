import os
import yaml
import json

def test_foundation():
    # Use relative pathing based on the test file location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'config', 'channels.yaml')
    data_path = os.path.join(base_dir, 'data', 'seen_videos.json')

    print(f"Checking config: {config_path}")
    assert os.path.exists(config_path), f"config/channels.yaml missing at {config_path}"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        assert 'channels' in config, "channels key missing in config"
        assert len(config['channels']) > 0, "No channels in config"
        print("✓ Config loaded successfully")

    print(f"Checking data: {data_path}")
    assert os.path.exists(data_path), f"data/seen_videos.json missing at {data_path}"
    with open(data_path, 'r') as f:
        data = json.load(f)
        assert isinstance(data, list), "seen_videos.json should be a list"
        print("✓ Data file loaded successfully")

    print("\nFoundation Test Passed!")

if __name__ == "__main__":
    try:
        test_foundation()
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
