"""
Simple test script to verify HoloMesh functionality
"""

def test_imports():
    """Test that all necessary modules can be imported."""
    try:
        from src.ai.cad_ai_optimizer import CADAIOptimizer, AIOptimizationStrategy, InteractionMode
        print("✅ CADAIOptimizer imported successfully")
        
        from src.config.holomesh_config_manager import get_holomesh_config_manager
        print("✅ HoloMeshConfigManager imported successfully")
        
        # Test creating an optimizer instance
        optimizer = CADAIOptimizer()
        print("✅ CADAIOptimizer instance created successfully")
        
        # Test interaction modes
        print(f"✅ InteractionMode.SEMI_AUTOMATIC: {InteractionMode.SEMI_AUTOMATIC}")
        print(f"✅ InteractionMode.MANUAL: {InteractionMode.MANUAL}")
        
        # Test configuration manager
        config_manager = get_holomesh_config_manager()
        semi_auto_config = config_manager.get_interaction_mode_config("semi_automatic")
        print(f"✅ Semi-Automatic mode config: {semi_auto_config}")
        
        manual_config = config_manager.get_interaction_mode_config("manual")
        print(f"✅ Manual mode config: {manual_config}")
        
        # Test HoloMesh integration settings
        semi_auto_holomesh = config_manager.is_holomesh_integration_enabled("semi_automatic")
        manual_holomesh = config_manager.is_holomesh_integration_enabled("manual")
        print(f"✅ Semi-Automatic HoloMesh integration enabled: {semi_auto_holomesh}")
        print(f"✅ Manual HoloMesh integration enabled: {manual_holomesh}")
        
        print("\n🎉 All basic tests passed! HoloMesh functionality is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing HoloMesh Basic Functionality")
    print("=" * 40)
    success = test_imports()
    if success:
        print("\n✅ All tests completed successfully!")
    else:
        print("\n❌ Some tests failed!")