# utils.py - OPTIONAL: Utility functions
"""
Utility functions for AI Model Eco & Ethics Calculator
Helper functions for formatting, validation, and common operations
"""

import re
from typing import Dict, Any, Optional

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_params_billions(value: float) -> bool:
        """Validate parameter count is within reasonable range"""
        return 0.01 <= value <= 10000.0
    
    @staticmethod
    def validate_training_hours(value: int) -> bool:
        """Validate training hours"""
        return 1 <= value <= 1000000
    
    @staticmethod
    def validate_tokens(value: int) -> bool:
        """Validate token count"""
        return 0 <= value <= 10000000000
    
    @staticmethod
    def validate_pue(value: float) -> bool:
        """Validate PUE value"""
        return 1.0 <= value <= 3.0
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class Formatters:
    """Output formatting utilities"""
    
    @staticmethod
    def format_number(value: float, decimals: int = 0) -> str:
        """Format number with thousand separators"""
        if decimals == 0:
            return f"{value:,.0f}"
        return f"{value:,.{decimals}f}"
    
    @staticmethod
    def format_currency(value: float) -> str:
        """Format as USD currency"""
        return f"${value:,.2f}"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        """Format as percentage"""
        return f"{value:.1f}%"
    
    @staticmethod
    def format_scientific(value: float) -> str:
        """Format in scientific notation"""
        return f"{value:.2e}"
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"

class DataHelpers:
    """Data manipulation helpers"""
    
    @staticmethod
    def calculate_percentage_change(old_value: float, new_value: float) -> float:
        """Calculate percentage change between values"""
        if old_value == 0:
            return 0
        return ((new_value - old_value) / old_value) * 100
    
    @staticmethod
    def interpolate_value(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
        """Linear interpolation"""
        if x2 == x1:
            return y1
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    
    @staticmethod
    def moving_average(values: list, window: int = 3) -> list:
        """Calculate moving average"""
        if len(values) < window:
            return values
        result = []
        for i in range(len(values)):
            start = max(0, i - window + 1)
            end = i + 1
            result.append(sum(values[start:end]) / len(values[start:end]))
        return result

class ConversionHelpers:
    """Unit conversion helpers"""
    
    @staticmethod
    def kwh_to_mwh(kwh: float) -> float:
        """Convert kWh to MWh"""
        return kwh / 1000
    
    @staticmethod
    def kg_to_tons(kg: float) -> float:
        """Convert kg to metric tons"""
        return kg / 1000
    
    @staticmethod
    def liters_to_gallons(liters: float) -> float:
        """Convert liters to US gallons"""
        return liters * 0.264172
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def params_to_flops(params_billions: float, tokens: int = 1) -> float:
        """Estimate FLOPs from parameters and tokens"""
        # Rough estimate: 6 * params * tokens for transformer
        return 6 * params_billions * 1e9 * tokens