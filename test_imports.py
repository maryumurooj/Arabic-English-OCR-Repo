# test_imports.py (in project root)
try:
    from app.models.response_models import ExtractionResponse
    print("✅ response_models imported successfully")
except Exception as e:
    print(f"❌ Error importing response_models: {e}")

try:
    from app.controllers import extraction_controller
    print("✅ extraction_controller imported successfully")
except Exception as e:
    print(f"❌ Error importing extraction_controller: {e}")

try:
    from app.main import app
    print("✅ main app imported successfully")
except Exception as e:
    print(f"❌ Error importing main: {e}")

