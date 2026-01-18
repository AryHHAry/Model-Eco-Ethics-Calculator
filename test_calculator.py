# test_calculator.py - OPTIONAL: Unit tests
"""
Unit tests for AI Model Eco & Ethics Calculator
Run with: pytest test_calculator.py
"""

import pytest
from app import ImpactCalculator, CalculationInput, Config

class TestImpactCalculator:
    """Test cases for impact calculator"""
    
    def test_training_carbon_basic(self):
        """Test basic training carbon calculation"""
        co2, energy = ImpactCalculator.calculate_training_carbon(
            params_b=7.0,
            training_hours=1000,
            hardware_type="NVIDIA A100",
            pue=1.5,
            carbon_intensity=450,
            model_type="Dense"
        )
        
        # Should return positive values
        assert co2 > 0
        assert energy > 0
        
        # CO2 should be reasonable for 7B model
        assert 1000 < co2 < 50000
    
    def test_inference_carbon_basic(self):
        """Test basic inference carbon calculation"""
        co2, energy = ImpactCalculator.calculate_inference_carbon(
            tokens_per_day=10000000,
            days=365,
            params_b=7.0,
            hardware_type="NVIDIA A100",
            pue=1.5,
            carbon_intensity=450,
            model_type="Dense"
        )
        
        # Should return positive values
        assert co2 > 0
        assert energy > 0
    
    def test_water_calculation(self):
        """Test water usage calculation"""
        water = ImpactCalculator.calculate_water_usage(
            energy_kwh=1000,
            water_per_kwh=3.0
        )
        
        assert water == 3000.0
    
    def test_ethical_risk_scoring(self):
        """Test ethical risk score ranges"""
        # Small model
        score_small = ImpactCalculator.calculate_ethical_risk(0.5, "Dense")
        assert 1 <= score_small <= 3
        
        # Medium model
        score_medium = ImpactCalculator.calculate_ethical_risk(50, "Dense")
        assert 5 <= score_medium <= 7
        
        # Large model
        score_large = ImpactCalculator.calculate_ethical_risk(500, "Dense")
        assert 8 <= score_large <= 10
    
    def test_moe_efficiency(self):
        """Test MoE model efficiency modifier"""
        co2_dense, _ = ImpactCalculator.calculate_training_carbon(
            params_b=100,
            training_hours=1000,
            hardware_type="NVIDIA A100",
            pue=1.5,
            carbon_intensity=450,
            model_type="Dense"
        )
        
        co2_moe, _ = ImpactCalculator.calculate_training_carbon(
            params_b=100,
            training_hours=1000,
            hardware_type="NVIDIA A100",
            pue=1.5,
            carbon_intensity=450,
            model_type="MoE (Mixture of Experts)"
        )
        
        # MoE should be more efficient (lower CO2)
        assert co2_moe < co2_dense
    
    def test_location_impact(self):
        """Test location carbon intensity impact"""
        # Low carbon location
        co2_low, _ = ImpactCalculator.calculate_training_carbon(
            params_b=7.0,
            training_hours=1000,
            hardware_type="NVIDIA A100",
            pue=1.5,
            carbon_intensity=200,  # Finland
            model_type="Dense"
        )
        
        # High carbon location
        co2_high, _ = ImpactCalculator.calculate_training_carbon(
            params_b=7.0,
            training_hours=1000,
            hardware_type="NVIDIA A100",
            pue=1.5,
            carbon_intensity=500,  # Singapore
            model_type="Dense"
        )
        
        # Higher carbon intensity should result in more CO2
        assert co2_high > co2_low
    
    def test_full_calculation_pipeline(self):
        """Test complete calculation pipeline"""
        input_params = CalculationInput(
            params_b=7.0,
            model_type="Dense",
            training_hours=1000,
            tokens_per_day=10000000,
            inference_days=365,
            location="Global Average",
            hardware="NVIDIA A100",
            pue=1.5
        )
        
        result = ImpactCalculator.calculate_all(input_params)
        
        # Verify all fields are populated
        assert result.training_co2 > 0
        assert result.inference_co2 > 0
        assert result.total_co2 > 0
        assert result.total_water > 0
        assert result.total_energy > 0
        assert result.total_cost > 0
        assert 1 <= result.ethical_score <= 10
        assert len(result.ethical_explanation) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])