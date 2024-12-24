import sys
import json

def detect_disease(image_path):
    """
    Placeholder for actual disease detection logic.
    Replace this with a real model or processing code.
    """
    # Simulated result
    disease_result = {
        "disease": "Leaf Spot",
        "confidence": "95%",
        "recommendation": "Use fungicides and ensure proper watering."
    }
    return disease_result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        result = detect_disease(image_path)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
