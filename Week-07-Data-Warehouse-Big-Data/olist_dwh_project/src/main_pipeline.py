import subprocess
import sys

def run_script(script_name):
    """Runs a Python script and checks for errors."""
    print(f"\n{'='*50}")
    print(f"🚀 Starting execution: {script_name}")
    print(f"{'='*50}")
    
    try:
        # Run scripts sequentially and check for errors
        result = subprocess.run([sys.executable, f"src/{script_name}"], check=True)
        print(f"✅ {script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ An error occurred while running {script_name}.")
        print(f"Exit code: {e.returncode}")
        # Stop the entire pipeline if a step fails (Handle Failures)
        sys.exit(1) 

if __name__ == "__main__":
    print("🌟 Starting Full Olist Data Pipeline (End-to-End) 🌟")
    
    # 1. Run Extraction and Load to Staging Phase
    run_script("extract.py")
    
    # 2. Run Transformation, Apply SCD, and Populate DWH Phase
    run_script("transform_load.py")
    
    print("\n🎉 Data pipeline executed successfully! The DWH is ready for analysis.")