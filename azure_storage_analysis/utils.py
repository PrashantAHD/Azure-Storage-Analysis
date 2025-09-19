# Utility functions for Azure Storage Analysis

import logging
import re
from datetime import datetime, timedelta

def setup_logging():
    """Setup logging configuration for the analysis tool"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('azure_storage_analysis.log')
        ]
    )
    return logging.getLogger(__name__)

def format_bytes(bytes_value):
    """Convert bytes to human readable format"""
    if bytes_value == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_value >= 1024 and i < len(size_names) - 1:
        bytes_value /= 1024.0
        i += 1
    
    return f"{bytes_value:.2f} {size_names[i]}"

def parse_size_string(size_str):
    """Parse size string like '1.5 GB' to bytes"""
    if not size_str or size_str == "0 B":
        return 0
    
    pattern = r'(\d+\.?\d*)\s*([KMGT]?B)'
    match = re.match(pattern, size_str.upper())
    
    if not match:
        return 0
    
    value = float(match.group(1))
    unit = match.group(2)
    
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    return int(value * multipliers.get(unit, 1))

def calculate_age_in_days(last_modified):
    """Calculate age in days from last modified date"""
    if isinstance(last_modified, str):
        try:
            last_modified = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
        except:
            return 0
    
    return (datetime.now() - last_modified.replace(tzinfo=None)).days

def filter_by_pattern(items, pattern):
    """Filter items by glob pattern"""
    if not pattern:
        return items
    
    import fnmatch
    return [item for item in items if fnmatch.fnmatch(item, pattern)]

def safe_divide(numerator, denominator):
    """Safe division that returns 0 if denominator is 0"""
    return numerator / denominator if denominator != 0 else 0

def validate_storage_account_name(name):
    """Validate storage account name according to Azure rules"""
    if not name:
        return False, "Storage account name cannot be empty"
    
    if len(name) < 3 or len(name) > 24:
        return False, "Storage account name must be between 3 and 24 characters"
    
    if not name.islower():
        return False, "Storage account name must be lowercase"
    
    if not name.isalnum():
        return False, "Storage account name must contain only letters and numbers"
    
    return True, "Valid storage account name"

def get_timestamp():
    """Get current timestamp for file naming"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
