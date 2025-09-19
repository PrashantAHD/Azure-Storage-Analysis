# This file marks the azure_storage_analysis directory as a Python package.

"""
Azure Storage Analysis Package

This package provides comprehensive analysis of Azure Storage accounts including:
- Blob Storage containers and blobs analysis
- Azure Files shares and files analysis  
- Cost optimization recommendations
- Detailed usage reports and Excel exports

Main modules:
- core: Main analysis engine and orchestration
- auth: Azure authentication and resource discovery
- reporting: Excel/CSV report generation
- recommendations: Cost optimization recommendations
- utils: Utility functions and helpers
"""

__version__ = "3.0.0"
__author__ = "Prashant Kumar"
__email__ = "prashant.kumar@ahead.com"

# Import main functions for easy access
from .core import get_azure_storage_analysis_enhanced, main
from .utils import setup_logging, format_bytes
from .recommendations import generate_cost_recommendations

__all__ = [
    'get_azure_storage_analysis_enhanced',
    'main', 
    'setup_logging',
    'format_bytes',
    'generate_cost_recommendations'
]
