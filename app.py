# app.py - PRODUCTION VERSION
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

class Config:
    """Centralized configuration management"""
    
    APP_TITLE = "AI Model Eco & Ethics Calculator"
    APP_ICON = "🌍"
    VERSION = "1.0.0"
    AUTHOR = "Ary HH"
    AUTHOR_EMAIL = "aryhharyanto@proton.me"
    
    # Calculation constants
    CO2_PER_BILLION_PARAMS = 2.0  # kg CO2e
    INFERENCE_CO2_PER_1K_TOKENS = 0.5  # grams
    ENERGY_COST_PER_KWH = 0.10  # USD
    TREE_CO2_ABSORPTION_PER_YEAR = 20  # kg
    CAR_CO2_PER_KM = 0.12  # kg
    FLIGHT_TRANSATLANTIC_CO2 = 1000  # kg
    HOUSEHOLD_WATER_PER_DAY = 300  # liters
    US_HOME_ENERGY_PER_YEAR = 10800  # kWh
    
    # Data center locations with carbon intensity (gCO2e/kWh) and water usage (L/kWh)
    LOCATIONS = {
        "US-West (Oregon)": {"carbon": 350, "water": 2.5, "renewable_pct": 60},
        "US-East (Virginia)": {"carbon": 450, "water": 3.0, "renewable_pct": 40},
        "EU-West (Ireland)": {"carbon": 300, "water": 2.0, "renewable_pct": 70},
        "EU-Central (Germany)": {"carbon": 400, "water": 2.8, "renewable_pct": 55},
        "EU-North (Finland)": {"carbon": 200, "water": 1.8, "renewable_pct": 85},
        "Asia-Pacific (Singapore)": {"carbon": 500, "water": 4.5, "renewable_pct": 25},
        "Asia-East (Tokyo)": {"carbon": 480, "water": 3.5, "renewable_pct": 30},
        "Global Average": {"carbon": 450, "water": 3.0, "renewable_pct": 40}
    }
    
    # Hardware specifications
    HARDWARE = {
        "NVIDIA A100": {"tdp": 400, "efficiency": 1.0, "cost_per_hour": 3.0, "generation": "Ampere"},
        "NVIDIA H100": {"tdp": 700, "efficiency": 1.4, "cost_per_hour": 8.0, "generation": "Hopper"},
        "NVIDIA V100": {"tdp": 300, "efficiency": 0.7, "cost_per_hour": 2.0, "generation": "Volta"},
        "TPU v4": {"tdp": 350, "efficiency": 1.2, "cost_per_hour": 3.5, "generation": "TPU"},
        "TPU v5": {"tdp": 400, "efficiency": 1.5, "cost_per_hour": 4.5, "generation": "TPU"}
    }
    
    # Model type configurations
    MODEL_TYPES = {
        "Dense": {"efficiency_multiplier": 1.0, "risk_modifier": 0},
        "MoE (Mixture of Experts)": {"efficiency_multiplier": 0.8, "risk_modifier": 0.5}
    }

# =============================================================================
# DATA MODELS
# =============================================================================

class CalculationInput:
    """Input parameters for calculations"""
    def __init__(self, params_b, model_type, training_hours, tokens_per_day, 
                 inference_days, location, hardware, pue):
        self.params_b = params_b
        self.model_type = model_type
        self.training_hours = training_hours
        self.tokens_per_day = tokens_per_day
        self.inference_days = inference_days
        self.location = location
        self.hardware = hardware
        self.pue = pue
    
    def to_dict(self):
        return {
            "Model Parameters (B)": self.params_b,
            "Model Type": self.model_type,
            "Training Hours": self.training_hours,
            "Tokens per Day": self.tokens_per_day,
            "Inference Days": self.inference_days,
            "Location": self.location,
            "Hardware": self.hardware,
            "PUE": self.pue
        }

class CalculationResult:
    """Results from calculations"""
    def __init__(self):
        self.training_co2 = 0
        self.training_energy = 0
        self.training_water = 0
        self.training_cost = 0
        
        self.inference_co2 = 0
        self.inference_energy = 0
        self.inference_water = 0
        self.inference_cost = 0
        
        self.total_co2 = 0
        self.total_energy = 0
        self.total_water = 0
        self.total_cost = 0
        
        self.ethical_score = 0
        self.ethical_explanation = ""
        
        self.timestamp = datetime.now().isoformat()
    
    def calculate_totals(self):
        self.total_co2 = self.training_co2 + self.inference_co2
        self.total_energy = self.training_energy + self.inference_energy
        self.total_water = self.training_water + self.inference_water
        self.total_cost = self.training_cost + self.inference_cost
    
    def to_dict(self):
        return {
            "training": {
                "co2_kg": self.training_co2,
                "energy_kwh": self.training_energy,
                "water_liters": self.training_water,
                "cost_usd": self.training_cost
            },
            "inference": {
                "co2_kg": self.inference_co2,
                "energy_kwh": self.inference_energy,
                "water_liters": self.inference_water,
                "cost_usd": self.inference_cost
            },
            "total": {
                "co2_kg": self.total_co2,
                "energy_kwh": self.total_energy,
                "water_liters": self.total_water,
                "cost_usd": self.total_cost
            },
            "ethical": {
                "score": self.ethical_score,
                "explanation": self.ethical_explanation
            },
            "timestamp": self.timestamp
        }

# =============================================================================
# CALCULATION ENGINE
# =============================================================================

class ImpactCalculator:
    """Core calculation engine - easily extensible and testable"""
    
    @staticmethod
    def calculate_training_carbon(params_b, training_hours, hardware_type, pue, 
                                  carbon_intensity, model_type):
        """Calculate training phase carbon emissions"""
        # Base emission from model size
        base_co2 = params_b * Config.CO2_PER_BILLION_PARAMS
        
        # Hardware specifications
        hw_specs = Config.HARDWARE[hardware_type]
        tdp = hw_specs["tdp"]
        efficiency_factor = hw_specs["efficiency"]
        
        # Model type efficiency
        model_efficiency = Config.MODEL_TYPES[model_type]["efficiency_multiplier"]
        
        # Energy consumption in kWh
        energy_kwh = (tdp * training_hours * pue) / 1000
        
        # Carbon from energy
        carbon_from_energy = (energy_kwh * carbon_intensity) / 1000  # kg CO2e
        
        # Total with efficiency adjustments
        total_co2 = (base_co2 + carbon_from_energy) * efficiency_factor * model_efficiency
        
        return total_co2, energy_kwh
    
    @staticmethod
    def calculate_inference_carbon(tokens_per_day, days, params_b, hardware_type, 
                                   pue, carbon_intensity, model_type):
        """Calculate inference phase carbon emissions"""
        # Size factor - larger models use more compute per token
        size_factor = 1 + (params_b / 100)
        
        # Model type efficiency
        model_efficiency = Config.MODEL_TYPES[model_type]["efficiency_multiplier"]
        
        # CO2 per 1000 tokens with scaling
        co2_per_1k_tokens = Config.INFERENCE_CO2_PER_1K_TOKENS * size_factor
        
        # Total tokens
        total_tokens = tokens_per_day * days
        
        # Carbon in kg
        carbon_kg = (total_tokens / 1000) * co2_per_1k_tokens / 1000 * model_efficiency
        
        # Energy estimate
        hw_specs = Config.HARDWARE[hardware_type]
        tdp = hw_specs["tdp"]
        
        # Rough estimate: 1 token ≈ 0.001 seconds on GPU
        compute_hours = (total_tokens * 0.001) / 3600
        energy_kwh = (tdp * compute_hours * pue) / 1000 * model_efficiency
        
        return carbon_kg, energy_kwh
    
    @staticmethod
    def calculate_water_usage(energy_kwh, water_per_kwh):
        """Calculate water consumption for cooling"""
        return energy_kwh * water_per_kwh
    
    @staticmethod
    def calculate_cost(energy_kwh, hardware_type):
        """Calculate financial cost"""
        hw_specs = Config.HARDWARE[hardware_type]
        base_rate = hw_specs["cost_per_hour"]
        tdp_kw = hw_specs["tdp"] / 1000
        
        # Compute hours
        compute_hours = energy_kwh / tdp_kw if tdp_kw > 0 else 0
        
        # Compute cost + energy cost
        compute_cost = compute_hours * base_rate
        energy_cost = energy_kwh * Config.ENERGY_COST_PER_KWH
        
        return compute_cost + energy_cost
    
    @staticmethod
    def calculate_ethical_risk(params_b, model_type):
        """Calculate ethical risk score (1-10)"""
        # Base score from size
        if params_b < 1:
            base_score = 2
        elif params_b < 10:
            base_score = 4
        elif params_b < 50:
            base_score = 6
        elif params_b < 100:
            base_score = 7
        elif params_b < 500:
            base_score = 8
        else:
            base_score = 9
        
        # Model type modifier
        risk_modifier = Config.MODEL_TYPES[model_type]["risk_modifier"]
        
        final_score = min(10, base_score + risk_modifier)
        
        return round(final_score, 1)
    
    @staticmethod
    def get_ethical_explanation(score):
        """Get explanation for ethical risk score"""
        if score <= 3:
            return "Low risk - Small models with limited capacity for amplifying biases."
        elif score <= 5:
            return "Moderate risk - Medium models may contain biases from training data."
        elif score <= 7:
            return "Elevated risk - Large models can amplify biases and lack transparency."
        else:
            return "High risk - Very large models have significant bias amplification potential and limited interpretability."
    
    @classmethod
    def calculate_all(cls, input_params: CalculationInput) -> CalculationResult:
        """Main calculation orchestrator"""
        result = CalculationResult()
        
        # Get location data
        location_data = Config.LOCATIONS[input_params.location]
        carbon_intensity = location_data["carbon"]
        water_per_kwh = location_data["water"]
        
        # Training calculations
        result.training_co2, result.training_energy = cls.calculate_training_carbon(
            input_params.params_b,
            input_params.training_hours,
            input_params.hardware,
            input_params.pue,
            carbon_intensity,
            input_params.model_type
        )
        result.training_water = cls.calculate_water_usage(result.training_energy, water_per_kwh)
        result.training_cost = cls.calculate_cost(result.training_energy, input_params.hardware)
        
        # Inference calculations
        result.inference_co2, result.inference_energy = cls.calculate_inference_carbon(
            input_params.tokens_per_day,
            input_params.inference_days,
            input_params.params_b,
            input_params.hardware,
            input_params.pue,
            carbon_intensity,
            input_params.model_type
        )
        result.inference_water = cls.calculate_water_usage(result.inference_energy, water_per_kwh)
        result.inference_cost = cls.calculate_cost(result.inference_energy, input_params.hardware)
        
        # Totals
        result.calculate_totals()
        
        # Ethical risk
        result.ethical_score = cls.calculate_ethical_risk(
            input_params.params_b,
            input_params.model_type
        )
        result.ethical_explanation = cls.get_ethical_explanation(result.ethical_score)
        
        return result

# =============================================================================
# VISUALIZATION & REPORTING
# =============================================================================

class ReportGenerator:
    """Generate visualizations and reports"""
    
    @staticmethod
    def generate_comparisons(result: CalculationResult):
        """Generate real-world comparison metrics"""
        comparisons = {
            "carbon": {
                "car_km": result.total_co2 / Config.CAR_CO2_PER_KM,
                "flights_transatlantic": result.total_co2 / Config.FLIGHT_TRANSATLANTIC_CO2,
                "trees_year": result.total_co2 / Config.TREE_CO2_ABSORPTION_PER_YEAR
            },
            "water": {
                "bottles_500ml": result.total_water / 0.5,
                "households_day": result.total_water / Config.HOUSEHOLD_WATER_PER_DAY
            },
            "energy": {
                "homes_year": result.total_energy / Config.US_HOME_ENERGY_PER_YEAR
            }
        }
        return comparisons
    
    @staticmethod
    def generate_recommendations(result: CalculationResult, input_params: CalculationInput):
        """Generate actionable recommendations"""
        recommendations = []
        
        if result.total_co2 > 10000:
            recommendations.append({
                "priority": "high",
                "category": "Model Size",
                "message": "Consider model compression techniques or distillation to reduce size"
            })
        
        if input_params.pue > 2.0:
            recommendations.append({
                "priority": "medium",
                "category": "Infrastructure",
                "message": "Data center PUE is high - consider more efficient facilities"
            })
        
        location_data = Config.LOCATIONS[input_params.location]
        if location_data["carbon"] > 400:
            recommendations.append({
                "priority": "medium",
                "category": "Location",
                "message": "Consider data centers in regions with renewable energy (lower carbon intensity)"
            })
        
        if result.ethical_score >= 7:
            recommendations.append({
                "priority": "high",
                "category": "Ethics",
                "message": "Implement robust bias testing, fairness audits, and transparency measures"
            })
        
        if input_params.params_b > 100:
            recommendations.append({
                "priority": "medium",
                "category": "Efficiency",
                "message": "Evaluate if a smaller model could achieve similar performance"
            })
        
        if location_data["renewable_pct"] < 50:
            recommendations.append({
                "priority": "low",
                "category": "Sustainability",
                "message": f"Current location uses only {location_data['renewable_pct']}% renewable energy"
            })
        
        return recommendations
    
    @staticmethod
    def export_json(input_params: CalculationInput, result: CalculationResult):
        """Export results as JSON"""
        export_data = {
            "metadata": {
                "version": Config.VERSION,
                "author": Config.AUTHOR,
                "timestamp": result.timestamp
            },
            "input": input_params.to_dict(),
            "results": result.to_dict(),
            "comparisons": ReportGenerator.generate_comparisons(result)
        }
        return json.dumps(export_data, indent=2)

# =============================================================================
# UI COMPONENTS
# =============================================================================

class UIComponents:
    """Reusable UI components"""
    
    @staticmethod
    def render_custom_css():
        """Apply custom CSS styling"""
        st.markdown("""
        <style>
            .main {
                padding: 2rem;
            }
            .stAlert {
                margin: 1rem 0;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 10px;
                color: white;
                margin: 1rem 0;
            }
            .warning-box {
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 1rem;
                margin: 1rem 0;
                border-radius: 5px;
            }
            .result-box {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border: 1px solid #dee2e6;
            }
            .footer {
                text-align: center;
                padding: 2rem;
                margin-top: 3rem;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 0.5rem;
            }
            .subtitle {
                color: #7f8c8d;
                font-size: 1.1rem;
                margin-bottom: 2rem;
            }
            .recommendation-high {
                border-left: 4px solid #dc3545;
            }
            .recommendation-medium {
                border-left: 4px solid #ffc107;
            }
            .recommendation-low {
                border-left: 4px solid #28a745;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render application header"""
        st.title(f"{Config.APP_ICON} {Config.APP_TITLE}")
        st.markdown(f'<p class="subtitle">Estimate environmental impact and ethical risks of large AI models (v{Config.VERSION})</p>', 
                   unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Important:</strong> These are rough estimates for educational purposes only. 
            Actual impacts vary significantly based on infrastructure, optimization, and usage patterns. 
            Not a replacement for professional environmental auditing.
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_input_form():
        """Render input form and return parameters"""
        st.header("📊 Model Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Model Configuration")
            params_input = st.number_input(
                "Model Parameters (Billions)", 
                min_value=0.1, 
                max_value=10000.0, 
                value=7.0, 
                step=0.1,
                help="Total number of parameters in billions (e.g., GPT-3 = 175B)"
            )
            
            model_type = st.selectbox(
                "Model Type", 
                list(Config.MODEL_TYPES.keys()),
                help="Dense models use all parameters; MoE activates subset per input"
            )
            
            st.subheader("Training")
            training_hours = st.number_input(
                "Training Duration (GPU hours)", 
                min_value=1, 
                max_value=1000000, 
                value=1000, 
                step=100,
                help="Total GPU hours for training (e.g., 100 GPUs × 10 hours = 1000)"
            )
        
        with col2:
            st.subheader("Infrastructure")
            location = st.selectbox(
                "Data Center Location", 
                list(Config.LOCATIONS.keys()),
                help="Location affects carbon intensity and water usage"
            )
            
            # Show location details
            loc_data = Config.LOCATIONS[location]
            st.caption(f"🌱 Renewable: {loc_data['renewable_pct']}% | 💨 Carbon: {loc_data['carbon']}g/kWh | 💧 Water: {loc_data['water']}L/kWh")
            
            hardware = st.selectbox(
                "Hardware Type", 
                list(Config.HARDWARE.keys()),
                help="GPU/TPU type affects power consumption and efficiency"
            )
            
            # Show hardware details
            hw_data = Config.HARDWARE[hardware]
            st.caption(f"⚡ TDP: {hw_data['tdp']}W | 🚀 Generation: {hw_data['generation']} | 💰 ${hw_data['cost_per_hour']}/hr")
            
            pue = st.slider(
                "PUE (Power Usage Effectiveness)", 
                min_value=1.0, 
                max_value=3.0, 
                value=1.5, 
                step=0.1,
                help="1.0 = perfect efficiency, typical datacenters: 1.2-2.0"
            )
            
            st.subheader("Inference")
            tokens_per_day = st.number_input(
                "Tokens per Day", 
                min_value=0, 
                max_value=10000000000, 
                value=10000000, 
                step=1000000,
                help="Total tokens processed daily (input + output)"
            )
            
            inference_days = st.number_input(
                "Inference Period (days)", 
                min_value=1, 
                max_value=3650, 
                value=365, 
                step=1,
                help="Duration of model deployment"
            )
        
        return CalculationInput(
            params_input, model_type, training_hours, tokens_per_day,
            inference_days, location, hardware, pue
        )
    
    @staticmethod
    def render_results(result: CalculationResult, comparisons: dict, recommendations: list):
        """Render calculation results"""
        st.header("📈 Results")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total CO₂", f"{result.total_co2:,.0f} kg")
        with col2:
            st.metric("Total Water", f"{result.total_water:,.0f} L")
        with col3:
            st.metric("Total Energy", f"{result.total_energy:,.0f} kWh")
        with col4:
            st.metric("Estimated Cost", f"${result.total_cost:,.0f}")
        
        # Detailed breakdown
        st.subheader("🔬 Detailed Breakdown")
        
        breakdown_data = {
            "Phase": ["Training", "Inference", "Total"],
            "CO₂ (kg)": [
                f"{result.training_co2:,.0f}", 
                f"{result.inference_co2:,.0f}", 
                f"{result.total_co2:,.0f}"
            ],
            "Water (L)": [
                f"{result.training_water:,.0f}", 
                f"{result.inference_water:,.0f}", 
                f"{result.total_water:,.0f}"
            ],
            "Energy (kWh)": [
                f"{result.training_energy:,.0f}", 
                f"{result.inference_energy:,.0f}", 
                f"{result.total_energy:,.0f}"
            ],
            "Cost ($)": [
                f"{result.training_cost:,.0f}", 
                f"{result.inference_cost:,.0f}", 
                f"{result.total_cost:,.0f}"
            ]
        }
        
        df = pd.DataFrame(breakdown_data)
        st.table(df)
        
        # Visualizations
        st.subheader("📊 Impact Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CO2 breakdown chart
            chart_data = pd.DataFrame({
                "Phase": ["Training", "Inference"],
                "CO₂ (kg)": [result.training_co2, result.inference_co2]
            })
            st.bar_chart(chart_data.set_index("Phase"))
            st.caption("Carbon Emissions by Phase")
        
        with col2:
            # Resource usage chart
            resource_data = pd.DataFrame({
                "Resource": ["Energy (kWh)", "Water (L)", "CO₂ (kg)"],
                "Training": [result.training_energy, result.training_water, result.training_co2],
                "Inference": [result.inference_energy, result.inference_water, result.inference_co2]
            })
            st.bar_chart(resource_data.set_index("Resource"))
            st.caption("Resource Usage Comparison")
        
        # Comparisons
        st.subheader("🌎 Real-World Comparisons")
        
        comparison_col1, comparison_col2 = st.columns(2)
        
        with comparison_col1:
            st.markdown(f"""
            <div class="result-box">
                <h4>🚗 Carbon Footprint Equivalents</h4>
                <ul>
                    <li><strong>{comparisons['carbon']['car_km']:,.0f} km</strong> driven by average car</li>
                    <li><strong>{comparisons['carbon']['flights_transatlantic']:.1f}</strong> transatlantic flights</li>
                    <li><strong>{comparisons['carbon']['trees_year']:,.0f}</strong> trees needed for 1 year to offset</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with comparison_col2:
            st.markdown(f"""
            <div class="result-box">
                <h4>💧 Resource Equivalents</h4>
                <ul>
                    <li><strong>{comparisons['water']['bottles_500ml']:,.0f}</strong> 500ml water bottles</li>
                    <li><strong>{comparisons['water']['households_day']:.1f}</strong> household-days of water</li>
                    <li><strong>{comparisons['energy']['homes_year']:.2f}</strong> US homes powered for 1 year</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Ethical risk score
        st.subheader("⚖️ Ethical Risk Assessment")
        
        risk_color = "🟢" if result.ethical_score <= 3 else "🟡" if result.ethical_score <= 6 else "🔴"
        
        st.markdown(f"""
        <div class="result-box">
            <h4>{risk_color} Ethical Risk Score: {result.ethical_score}/10</h4>
            <p><strong>Assessment:</strong> {result.ethical_explanation}</p>
            <p><em>Note: This score is a simplified proxy based on model size and complexity. 
            Actual ethical risks depend on training data, deployment context, safeguards, 
            and ongoing monitoring. Larger models tend to amplify biases present in training data 
            and have reduced interpretability.</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        if recommendations:
            for rec in recommendations:
                priority_class = f"recommendation-{rec['priority']}"
                icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                st.markdown(f"""
                <div class="result-box {priority_class}">
                    {icon} <strong>{rec['category']}:</strong> {rec['message']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Your configuration shows relatively efficient resource usage!")
    
    @staticmethod
    def render_export_options(input_params: CalculationInput, result: CalculationResult):
        """Render export options"""
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # JSON export
            json_data = ReportGenerator.export_json(input_params, result)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"ai_impact_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # CSV export
            csv_data = pd.DataFrame([{
                "Timestamp": result.timestamp,
                "Model_Parameters_B": input_params.params_b,
                "Training_CO2_kg": result.training_co2,
                "Inference_CO2_kg": result.inference_co2,
                "Total_CO2_kg": result.total_co2,
                "Total_Water_L": result.total_water,
                "Total_Energy_kWh": result.total_energy,
                "Total_Cost_USD": result.total_cost,
                "Ethical_Score": result.ethical_score
            }]).to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"ai_impact_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    @staticmethod
    def render_footer():
        """Render application footer"""
        st.markdown(f"""
        <div class="footer">
            <p><strong>Created by {Config.AUTHOR}</strong> (<a href="mailto:{Config.AUTHOR_EMAIL}">{Config.AUTHOR_EMAIL}</a>)</p>
            <p>Untuk edukasi dampak lingkungan & etika AI</p>
            <p style="font-size: 0.9rem; margin-top: 1rem;">
                Version {Config.VERSION} | Based on research and estimates from 2023-2025 studies on AI environmental impact.
                <br>Sources include papers on carbon emissions from training large language models,
                data center water usage, and ethical considerations of AI scale.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply custom styling
    UIComponents.render_custom_css()
    
    # Render header
    UIComponents.render_header()
    
    # Render input form
    input_params = UIComponents.render_input_form()
    
    # Calculate button
    if st.button("🔍 Calculate Impact", type="primary", use_container_width=True):
        
        with st.spinner("Calculating environmental impact..."):
            # Perform calculations
            result = ImpactCalculator.calculate_all(input_params)
            
            # Generate comparisons and recommendations
            comparisons = ReportGenerator.generate_comparisons(result)
            recommendations = ReportGenerator.generate_recommendations(result, input_params)
            
            # Store in session state for persistence
            st.session_state['last_result'] = result
            st.session_state['last_comparisons'] = comparisons
            st.session_state['last_recommendations'] = recommendations
            st.session_state['last_input'] = input_params
        
        # Render results
        UIComponents.render_results(result, comparisons, recommendations)
        
        # Render export options
        UIComponents.render_export_options(input_params, result)
    
    # Display previous results if available
    elif 'last_result' in st.session_state:
        st.info("📊 Showing previous calculation results. Modify parameters and click 'Calculate Impact' to recalculate.")
        
        UIComponents.render_results(
            st.session_state['last_result'],
            st.session_state['last_comparisons'],
            st.session_state['last_recommendations']
        )
        
        UIComponents.render_export_options(
            st.session_state['last_input'],
            st.session_state['last_result']
        )
    
    # Render footer
    UIComponents.render_footer()
    
    # Sidebar with additional info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown(f"""
        **Version:** {Config.VERSION}
        
        **Purpose:** Educational tool for estimating environmental impact and ethical risks of large AI models.
        
        **Methodology:**
        - Training CO₂: Based on parameter count and energy consumption
        - Inference CO₂: Scaled by model size and token volume
        - Water: Data center cooling requirements
        - Ethics: Proxy score based on model complexity
        
        **Limitations:**
        - Simplified estimates
        - Does not capture all optimizations
        - Regional variations apply
        - Not for compliance reporting
        
        **Sources:**
        - Strubell et al. (2019)
        - Patterson et al. (2021)
        - Luccioni et al. (2023)
        - Li et al. (2023)
        """)
        
        st.header("🔗 Resources")
        st.markdown("""
        - [Anthropic Research](https://www.anthropic.com/research)
        - [Green Software Foundation](https://greensoftware.foundation/)
        - [ML CO2 Impact](https://mlco2.github.io/impact/)
        - [Electricity Maps](https://app.electricitymaps.com/)
        """)
        
        st.header("📧 Contact")
        st.markdown(f"""
        For feedback or questions:
        
        **{Config.AUTHOR}**  
        [{Config.AUTHOR_EMAIL}](mailto:{Config.AUTHOR_EMAIL})
        """)

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()