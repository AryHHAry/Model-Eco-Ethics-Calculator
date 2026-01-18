# Contributing to AI Model Eco & Ethics Calculator

Thank you for your interest in improving this project! While this is a proprietary educational tool, we welcome certain types of contributions.

## 🎯 What We Accept

### ✅ Welcome Contributions

1. **Bug Reports**
   - Calculation errors or inconsistencies
   - UI/UX issues
   - Deployment problems
   - Documentation errors

2. **Data Improvements**
   - Updated carbon intensity values (with sources)
   - New hardware specifications (with documentation)
   - Improved calculation formulas (with research citations)
   - Regional data corrections

3. **Documentation**
   - Typo fixes
   - Clarity improvements
   - Translation contributions
   - Tutorial additions

4. **Research References**
   - New peer-reviewed papers on AI environmental impact
   - Updated statistics and benchmarks
   - Methodology improvements

### ❌ Not Accepted

- Feature additions without prior approval
- Major architectural changes
- Commercial forks or derivatives
- Competing implementations

## 📝 How to Contribute

### Reporting Bugs

Create an issue with:
```markdown
**Bug Description:**
Clear description of the problem

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Python Version: [e.g., 3.11.5]
- Streamlit Version: [e.g., 1.31.0]
- Browser: [e.g., Chrome 120]

**Screenshots:**
If applicable
```

### Suggesting Data Updates

Email aryhharyanto@proton.me with:

- Proposed change
- Source/citation (peer-reviewed preferred)
- Rationale for update
- Impact on calculations

### Proposing Features

Before implementing:

1. Email aryhharyanto@proton.me with proposal
2. Wait for approval
3. Discuss implementation approach
4. Proceed if approved

## 🔬 Code Standards

If contributing code (with approval):

### Python Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Include unit tests
- Comment complex logic
```python
def calculate_metric(value: float, factor: float) -> float:
    """
    Calculate metric with given factor.
    
    Args:
        value: Input value to process
        factor: Multiplication factor
        
    Returns:
        Calculated metric value
        
    Raises:
        ValueError: If value or factor is negative
    """
    if value < 0 or factor < 0:
        raise ValueError("Values must be non-negative")
    
    return value * factor
```

### Testing

- Write tests for new calculations
- Ensure existing tests pass
- Aim for >80% coverage
```python
def test_calculation():
    result = calculate_metric(10.0, 2.0)
    assert result == 20.0
```

### Documentation

- Update README if needed
- Add docstrings to new functions
- Comment non-obvious code
- Update CHANGELOG

## 📊 Data Sources

All data updates must include:

1. **Primary source** (peer-reviewed paper, official report)
2. **Publication date** (prefer sources from last 2 years)
3. **Methodology** (how was data collected/calculated)
4. **Geographic/temporal scope** (where and when applicable)

Example:
```markdown
**Data Update:** EU-West (Ireland) carbon intensity

**Current Value:** 300 gCO2e/kWh
**Proposed Value:** 280 gCO2e/kWh

**Source:** 
- European Environment Agency (2025)
- "Electricity Carbon Intensity in EU Member States 2024"
- https://www.eea.europa.eu/...

**Rationale:**
Increased renewable energy penetration (wind farms)
from 65% to 75% in 2024-2025 period

**Impact:**
Reduces calculated CO2 for this region by ~7%
```

## 🌍 Translation Contributions

Interested in translating?

1. Contact aryhharyanto@proton.me
2. Specify language and your qualifications
3. We'll provide translation guidelines
4. Maintain technical accuracy

## ⚖️ Legal

By contributing, you agree that:

- Your contributions will be licensed under the same proprietary license
- Ary HH retains all rights to contributions
- You have the right to submit the contribution
- Contributions are provided without warranty

## 📧 Contact

**For all contribution inquiries:**

Ary HH  
aryhharyanto@proton.me

**Response time:**
- Bug reports: 2-5 business days
- Data updates: 1-2 weeks
- Feature requests: 2-4 weeks

## 🙏 Acknowledgments

Contributors who provide accepted improvements will be acknowledged in:

- CHANGELOG.md
- README.md (Contributors section)
- White paper (if significant methodology improvements)

Thank you for helping improve AI sustainability awareness!

---

**Last Updated:** January 18, 2026  
**Author:** Ary HH (aryhharyanto@proton.me)