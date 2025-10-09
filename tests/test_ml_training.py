"""
Unit tests for the ML Training Engine
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import numpy as np

from src.ai.ml_training_engine import MLTrainingEngine, ModelType


@pytest.mark.asyncio
async def test_ml_training_engine_initialization():
    """Test that the MLTrainingEngine initializes correctly."""
    engine = MLTrainingEngine()
    assert engine is not None
    assert hasattr(engine, 'models')
    assert hasattr(engine, 'training_history')
    assert isinstance(engine.models, dict)
    assert isinstance(engine.training_history, dict)


@pytest.mark.asyncio
async def test_collect_real_data():
    """Test real data collection functionality."""
    engine = MLTrainingEngine()
    
    # Sample chip IDs
    chip_ids = ["chip_001", "chip_002", "chip_003"]
    
    # Mock the analytics module
    with patch('src.ai.ml_training_engine.analytics') as mock_analytics:
        mock_analytics.analyze_trends = AsyncMock(return_value={
            "status": "success",
            "trends": [
                {
                    "chip_id": "chip_001",
                    "defect_rate": 0.01,
                    "yield": 0.99,
                    "energy_consumption": 0.008,
                    "timestamp": "2023-01-01T00:00:00"
                }
            ]
        })
        
        result = await engine.collect_real_data(chip_ids, hours=24)
        
        assert result["status"] == "success"
        assert "data_points" in result
        assert result["data_points"] >= 0
        assert "collected_at" in result


@pytest.mark.asyncio
async def test_preprocess_data():
    """Test data preprocessing functionality."""
    engine = MLTrainingEngine()
    
    # Sample raw data
    raw_data = {
        "data": [
            {
                "defect_rate": 0.01,
                "yield": 0.99,
                "energy_consumption": 0.008,
                "frequency": 3.5,
                "temperature": 25.0
            },
            {
                "defect_rate": 0.02,
                "yield": 0.98,
                "energy_consumption": 0.010,
                "frequency": 3.2,
                "temperature": 27.0
            }
        ]
    }
    
    result = await engine.preprocess_data(raw_data, target="defect_rate")
    
    assert result["status"] == "success"
    assert "X" in result
    assert "y" in result
    assert len(result["X"]) == len(raw_data["data"])
    assert len(result["y"]) == len(raw_data["data"])


@pytest.mark.asyncio
async def test_train_model():
    """Test model training functionality."""
    engine = MLTrainingEngine()
    
    # Sample preprocessed data
    preprocessed_data = {
        "X": [[0.1, 0.9, 0.008], [0.2, 0.8, 0.010]],
        "y": [0.01, 0.02],
        "features": ["yield", "frequency", "energy_consumption"],
        "target": "defect_rate"
    }
    
    result = await engine.train_model(preprocessed_data, ModelType.RANDOM_FOREST)
    
    assert result["status"] == "success"
    assert "model_id" in result
    assert "model_info" in result
    assert result["model_info"]["model_type"] == "random_forest"
    
    # Check that model is stored
    model_id = result["model_id"]
    model_info = engine.get_model_info(model_id)
    assert model_info["status"] == "success"


@pytest.mark.asyncio
async def test_evaluate_model():
    """Test model evaluation functionality."""
    engine = MLTrainingEngine()
    
    # First train a model
    preprocessed_data = {
        "X": [[0.1, 0.9, 0.008], [0.2, 0.8, 0.010]],
        "y": [0.01, 0.02],
        "features": ["yield", "frequency", "energy_consumption"],
        "target": "defect_rate"
    }
    
    train_result = await engine.train_model(preprocessed_data, ModelType.RANDOM_FOREST)
    model_id = train_result["model_id"]
    
    # Evaluate the model
    result = await engine.evaluate_model(model_id)
    
    assert result["status"] == "success"
    assert "performance" in result
    assert "accuracy" in result["performance"]


@pytest.mark.asyncio
async def test_predict_with_model():
    """Test model prediction functionality."""
    engine = MLTrainingEngine()
    
    # First train a model
    preprocessed_data = {
        "X": [[0.1, 0.9, 0.008], [0.2, 0.8, 0.010]],
        "y": [0.01, 0.02],
        "features": ["yield", "frequency", "energy_consumption"],
        "target": "defect_rate"
    }
    
    train_result = await engine.train_model(preprocessed_data, ModelType.RANDOM_FOREST)
    model_id = train_result["model_id"]
    
    # Make predictions
    input_data = [[0.15, 0.85, 0.009]]
    result = await engine.predict_with_model(model_id, input_data)
    
    assert result["status"] == "success"
    assert "predictions" in result
    assert len(result["predictions"]) == len(input_data)


@pytest.mark.asyncio
async def test_integrate_with_optimization():
    """Test model integration with optimization engines."""
    engine = MLTrainingEngine()
    
    # First train a model
    preprocessed_data = {
        "X": [[0.1, 0.9, 0.008], [0.2, 0.8, 0.010]],
        "y": [0.01, 0.02],
        "features": ["yield", "frequency", "energy_consumption"],
        "target": "defect_rate"
    }
    
    train_result = await engine.train_model(preprocessed_data, ModelType.RANDOM_FOREST)
    model_id = train_result["model_id"]
    
    # Integrate with optimization
    result = await engine.integrate_with_optimization(model_id, "minimize_defects")
    
    assert result["status"] == "success"
    assert "integration_details" in result
    assert result["integration_details"]["chip_optimization_engine"] == "connected"


@pytest.mark.asyncio
async def test_get_model_info():
    """Test getting model information."""
    engine = MLTrainingEngine()
    
    # First train a model
    preprocessed_data = {
        "X": [[0.1, 0.9, 0.008], [0.2, 0.8, 0.010]],
        "y": [0.01, 0.02],
        "features": ["yield", "frequency", "energy_consumption"],
        "target": "defect_rate"
    }
    
    train_result = await engine.train_model(preprocessed_data, ModelType.RANDOM_FOREST)
    model_id = train_result["model_id"]
    
    # Get model info
    result = engine.get_model_info(model_id)
    
    assert result["status"] == "success"
    assert "model_info" in result
    assert result["model_info"]["model_id"] == model_id


@pytest.mark.asyncio
async def test_list_models():
    """Test listing all models."""
    engine = MLTrainingEngine()
    
    # Train a couple of models
    preprocessed_data = {
        "X": [[0.1, 0.9, 0.008], [0.2, 0.8, 0.010]],
        "y": [0.01, 0.02],
        "features": ["yield", "frequency", "energy_consumption"],
        "target": "defect_rate"
    }
    
    await engine.train_model(preprocessed_data, ModelType.RANDOM_FOREST)
    await engine.train_model(preprocessed_data, ModelType.DECISION_TREE)
    
    # List models
    result = engine.list_models()
    
    assert result["status"] == "success"
    assert "models" in result
    assert result["total_models"] >= 2


@pytest.mark.asyncio
async def test_get_training_history():
    """Test getting training history."""
    engine = MLTrainingEngine()
    
    # Train a model
    preprocessed_data = {
        "X": [[0.1, 0.9, 0.008], [0.2, 0.8, 0.010]],
        "y": [0.01, 0.02],
        "features": ["yield", "frequency", "energy_consumption"],
        "target": "defect_rate"
    }
    
    train_result = await engine.train_model(preprocessed_data, ModelType.RANDOM_FOREST)
    process_id = train_result["process_id"]
    
    # Get training history
    result = engine.get_training_history(process_id)
    
    assert result["status"] == "success"
    assert isinstance(result["data"], list)


if __name__ == "__main__":
    pytest.main([__file__])