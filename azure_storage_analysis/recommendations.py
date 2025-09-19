# Cost optimization and recommendations logic for Azure Storage Analysis

import logging
from datetime import datetime, timedelta
from .utils import format_bytes, safe_divide

def generate_cost_recommendations(storage_data):
    """Generate cost optimization recommendations based on storage analysis"""
    recommendations = []
    
    # Analyze for old/unused data
    recommendations.extend(_analyze_old_data(storage_data))
    
    # Analyze for empty containers
    recommendations.extend(_analyze_empty_containers(storage_data))
    
    # Analyze storage tier opportunities
    recommendations.extend(_analyze_storage_tiers(storage_data))
    
    # Analyze redundancy settings
    recommendations.extend(_analyze_redundancy(storage_data))
    
    return recommendations

def _analyze_old_data(storage_data):
    """Analyze data age and recommend archival"""
    recommendations = []
    
    for account_data in storage_data:
        account_name = account_data.get('account_name', 'Unknown')
        
        # Check for data older than 90 days
        old_data_90_plus = account_data.get('blobs_90_plus_days', 0)
        if old_data_90_plus > 0:
            recommendations.append({
                'type': 'Archive Opportunity',
                'priority': 'High',
                'account': account_name,
                'description': f'Consider archiving {old_data_90_plus:,} blobs older than 90 days',
                'potential_savings': 'Up to 80% storage cost reduction',
                'action': 'Move to Archive tier or delete if no longer needed'
            })
        
        # Check for data 30-90 days old
        old_data_30_90 = account_data.get('blobs_30_90_days', 0)
        if old_data_30_90 > 0:
            recommendations.append({
                'type': 'Cool Tier Opportunity',
                'priority': 'Medium',
                'account': account_name,
                'description': f'Consider moving {old_data_30_90:,} blobs (30-90 days old) to Cool tier',
                'potential_savings': 'Up to 50% storage cost reduction',
                'action': 'Implement lifecycle management policy'
            })
    
    return recommendations

def _analyze_empty_containers(storage_data):
    """Analyze empty containers and recommend cleanup"""
    recommendations = []
    
    for account_data in storage_data:
        account_name = account_data.get('account_name', 'Unknown')
        containers = account_data.get('containers', [])
        
        empty_containers = [c for c in containers if c.get('blob_count', 0) == 0]
        
        if empty_containers:
            container_names = [c.get('name', 'Unknown') for c in empty_containers]
            recommendations.append({
                'type': 'Resource Cleanup',
                'priority': 'Low',
                'account': account_name,
                'description': f'Remove {len(empty_containers)} empty containers: {", ".join(container_names[:3])}{"..." if len(container_names) > 3 else ""}',
                'potential_savings': 'Reduced management overhead',
                'action': 'Delete unused containers to simplify management'
            })
    
    return recommendations

def _analyze_storage_tiers(storage_data):
    """Analyze storage tier usage and recommend optimizations"""
    recommendations = []
    
    for account_data in storage_data:
        account_name = account_data.get('account_name', 'Unknown')
        total_size_gb = account_data.get('total_size_gb', 0)
        
        # Recommend lifecycle management for large storage accounts
        if total_size_gb > 100:
            recommendations.append({
                'type': 'Lifecycle Management',
                'priority': 'High',
                'account': account_name,
                'description': f'Large storage usage ({total_size_gb:.1f} GB) detected',
                'potential_savings': 'Significant cost reduction through automated tier management',
                'action': 'Implement Azure Blob lifecycle management policies'
            })
        
        # Check for many small files
        containers = account_data.get('containers', [])
        total_small_blobs = sum(c.get('small_blobs_count', 0) for c in containers)
        total_blobs = sum(c.get('blob_count', 0) for c in containers)
        
        if total_blobs > 0:
            small_blob_ratio = safe_divide(total_small_blobs, total_blobs)
            if small_blob_ratio > 0.8 and total_blobs > 1000:
                recommendations.append({
                    'type': 'Storage Optimization',
                    'priority': 'Medium',
                    'account': account_name,
                    'description': f'{small_blob_ratio*100:.1f}% of blobs are small files',
                    'potential_savings': 'Consider blob compression or consolidation',
                    'action': 'Evaluate file consolidation or compression strategies'
                })
    
    return recommendations

def _analyze_redundancy(storage_data):
    """Analyze storage redundancy settings"""
    recommendations = []
    
    for account_data in storage_data:
        account_name = account_data.get('account_name', 'Unknown')
        sku = account_data.get('sku', 'Unknown')
        
        # Recommend LRS for non-critical data
        if 'GRS' in sku or 'ZRS' in sku:
            recommendations.append({
                'type': 'Redundancy Optimization',
                'priority': 'Medium',
                'account': account_name,
                'description': f'Account uses {sku} redundancy',
                'potential_savings': 'Consider LRS for non-critical data (up to 50% cost reduction)',
                'action': 'Evaluate if geo-redundancy is required for all data'
            })
    
    return recommendations

def generate_summary_statistics(storage_data):
    """Generate summary statistics for the analysis"""
    total_accounts = len(storage_data)
    total_containers = sum(len(account.get('containers', [])) for account in storage_data)
    total_blobs = sum(
        sum(container.get('blob_count', 0) for container in account.get('containers', []))
        for account in storage_data
    )
    total_size_gb = sum(account.get('total_size_gb', 0) for account in storage_data)
    
    return {
        'total_accounts': total_accounts,
        'total_containers': total_containers,
        'total_blobs': total_blobs,
        'total_size_gb': total_size_gb,
        'total_size_formatted': format_bytes(total_size_gb * 1024**3)
    }
