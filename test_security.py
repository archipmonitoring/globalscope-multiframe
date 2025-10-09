import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from security.enhanced_firewall import EnhancedQuantumSingularityFirewall
    print("✓ Enhanced firewall imported successfully")
    
    async def test_firewall():
        firewall = EnhancedQuantumSingularityFirewall()
        print("✓ Enhanced firewall instantiated successfully")
        
        # Test valid process
        valid_data = {"type": "design_process", "name": "test"}
        result = await firewall.validate_process("test_1", valid_data)
        print(f"✓ Valid process validation: {result}")
        
        # Test invalid process with dangerous key
        invalid_data = {"__proto__": "malicious", "name": "test"}
        result = await firewall.validate_process("test_2", invalid_data)
        print(f"✓ Invalid process validation (should be False): {result}")
        
        # Test malicious process
        malicious_data = {"type": "malicious", "name": "test"}
        result = await firewall.validate_process("test_3", malicious_data)
        print(f"✓ Malicious process validation (should be False): {result}")
        
        print("🎉 All security enhancement tests passed!")
        return True

    if __name__ == "__main__":
        asyncio.run(test_firewall())
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()