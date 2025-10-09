#!/usr/bin/env python3
"""
Script to run enhanced validation of Singularity Dashboard implementation
"""
import asyncio
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main():
    """Main function to run enhanced validation"""
    try:
        # Import and run the enhanced validator
        with open('monitoring/enhanced_validation.py', 'r') as f:
            exec(f.read())
        # Get the EnhancedValidator class
        EnhancedValidator = locals()['EnhancedValidator']
        
        print("🚀 Running Enhanced Validation for Singularity Dashboard...")
        print("=" * 60)
        
        validator = EnhancedValidator()
        results = await validator.run_all_validations()
        report = validator.generate_report(results)
        print(report)
        
        # Return appropriate exit code
        all_passed = all(result["status"] == "pass" for result in results.values())
        return 0 if all_passed else 1
        
    except Exception as e:
        print(f"❌ Error running enhanced validation: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)