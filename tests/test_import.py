# test_import.py
try:
    from escatastrolib import Calle
    print("Import successful")
except ModuleNotFoundError as e:
    print(f"ModuleNotFoundError: {e}")
except Exception as e:
    print(f"Error: {e}")
