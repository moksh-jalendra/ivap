import urllib.request
import os

print("Downloading sample traffic video...")
url = "https://test-videos.co.uk/vids/jellyfish/mp4/h264/360/Jellyfish_360_10s_1MB.mp4" # Just a fallback
# Actually let's try to get a ped/traffic video
# Pexels public videos often change URLs. Let's use a very reliable test URL.
url_traffic = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"

os.makedirs("test_vid", exist_ok=True)
output_path = "test_vid/sample.mp4"

try:
    urllib.request.urlretrieve(url_traffic, output_path)
    print(f"Successfully downloaded sample video to {output_path}")
except Exception as e:
    print(f"Error downloading video: {e}")
    print("Please manually place an MP4 file named 'sample.mp4' in the test_vid folder.")
