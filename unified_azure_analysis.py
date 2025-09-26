#!/usr/bin/env python3
"""
Unified Azure FinOps Analysis Engine
Handles both single and multi-subscription analysis with intelligent detection
Generates Excel CIR reports and prepares data for dashboard
"""

import os
import json
from datetime import datetime
from azure_storage_analysis.auth import initialize_azure_clients, initialize_multi_subscription_analysis
from azure_storage_analysis.core import get_storage_account_connection_string
from azure_storage_analysis.cost_management import AzureCostAnalyzer
from azure_storage_analysis.reservations import AzureReservationAnalyzer
from azure_storage_analysis.savings_plans import AzureSavingsPlansAnalyzer
from azure_storage_analysis.unified_reporting import create_comprehensive_excel_report

def run_unified_analysis():
    """
    Unified Azure analysis that automatically detects single vs multi-subscription
    and generates appropriate CIR reports
    """
    print("🔍 UNIFIED AZURE FINOPS ANALYSIS ENGINE")
    print("=" * 80)
    print("📋 Initializing Azure connections...")
    
    # Interactive subscription selection
    print("\n" + "=" * 80)
    print("========================== SUBSCRIPTION SELECTION ==========================")
    print("=" * 80)
    print("📋 Choose your analysis scope:")
    print("1. Single Subscription Analysis (detailed analysis)")
    print("2. Multi-Subscription Analysis (enterprise view)")
    print("3. Auto-detect (recommended)")
    
    while True:
        choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("❌ Please enter 1, 2, or 3")
    
    # Initialize based on choice
    if choice == '1':
        return run_single_subscription_analysis()
    elif choice == '2':
        return run_multi_subscription_analysis()
    else:
        return run_auto_detect_analysis()

def run_single_subscription_analysis():
    """Run detailed single subscription analysis"""
    print("\n🔍 SINGLE SUBSCRIPTION DETAILED ANALYSIS")
    print("=" * 80)
    
    try:
        # Initialize single subscription
        credential, subscription_id, resource_client, storage_client = initialize_azure_clients()
        print(f"✅ Connected to subscription: {subscription_id}")
        
        # Run analysis
        results = analyze_subscription(credential, subscription_id, resource_client, storage_client)
        
        # Generate Excel report
        excel_file = generate_excel_report(
            container_results=results['container_results'],
            file_share_results=results['file_share_results'],
            storage_data=results['storage_data'],
            recommendations=results['recommendations'],
            analysis_type='single'
        )
        
        # Save results for dashboard
        save_analysis_results(results, 'single')
        
        print(f"\n✅ SINGLE SUBSCRIPTION ANALYSIS COMPLETE!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ Single subscription analysis failed: {e}")
        return False

def run_multi_subscription_analysis():
    """Run enterprise multi-subscription analysis"""
    print("\n🏢 MULTI-SUBSCRIPTION ENTERPRISE ANALYSIS")
    print("=" * 80)
    
    try:
        # Initialize multi-subscription
        credential, subscription_ids = initialize_multi_subscription_analysis()
        print(f"✅ Connected to {len(subscription_ids)} subscriptions")
        
        all_results = {
            'subscriptions': {},
            'total_cost': 0,
            'analysis_date': datetime.now().isoformat(),
            'analysis_type': 'multi-subscription'
        }
        
        aggregated_containers = []
        aggregated_file_shares = []
        aggregated_storage_accounts = []
        
        # Analyze each subscription
        for i, sub_id in enumerate(subscription_ids, 1):
            print(f"\n📊 Analyzing subscription {i}/{len(subscription_ids)}: {sub_id}")
            print("-" * 60)
            
            try:
                _, _, resource_client, storage_client = initialize_azure_clients(subscription_id=sub_id)
                sub_results = analyze_subscription(credential, sub_id, resource_client, storage_client)
                
                all_results['subscriptions'][sub_id] = sub_results['storage_data']
                all_results['total_cost'] += sub_results['storage_data'].get('total_cost', 0)
                
                # Aggregate data for Excel report
                aggregated_containers.extend(sub_results['container_results'])
                aggregated_file_shares.extend(sub_results['file_share_results'])
                aggregated_storage_accounts.extend(sub_results['storage_data']['storage_accounts'])
                
            except Exception as e:
                print(f"⚠️  Error analyzing subscription {sub_id}: {e}")
        
        # Generate consolidated Excel report
        excel_file = generate_excel_report(
            container_results=aggregated_containers,
            file_share_results=aggregated_file_shares,
            storage_data={
                'subscription_ids': subscription_ids,
                'storage_accounts': aggregated_storage_accounts,
                'total_cost': all_results['total_cost'],
                'analysis_date': all_results['analysis_date'],
                'multi_subscription': True
            },
            recommendations=generate_multi_subscription_recommendations(all_results),
            analysis_type='multi'
        )
        
        # Save results for dashboard
        save_analysis_results(all_results, 'multi')
        
        print(f"\n✅ MULTI-SUBSCRIPTION ANALYSIS COMPLETE!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ Multi-subscription analysis failed: {e}")
        return False

def run_auto_detect_analysis():
    """Auto-detect and run appropriate analysis"""
    print("\n🤖 AUTO-DETECTING OPTIMAL ANALYSIS MODE")
    print("=" * 80)
    
    try:
        # Try to get available subscriptions
        credential, subscription_ids = initialize_multi_subscription_analysis()
        
        if len(subscription_ids) == 1:
            print(f"📋 Detected 1 subscription - switching to single subscription mode")
            return run_single_subscription_analysis()
        else:
            print(f"📋 Detected {len(subscription_ids)} subscriptions - using multi-subscription mode")
            return run_multi_subscription_analysis()
            
    except Exception as e:
        print(f"⚠️  Auto-detection failed, falling back to single subscription: {e}")
        return run_single_subscription_analysis()

def analyze_subscription(credential, subscription_id, resource_client, storage_client):
    """Core subscription analysis logic"""
    print(f"\n📦 DISCOVERING STORAGE ACCOUNTS...")
    print("-" * 60)
    
    # Initialize data collection
    container_results = []
    file_share_results = []
    storage_accounts = []
    
    try:
        # Get storage accounts
        accounts = list(storage_client.storage_accounts.list())
        
        for account in accounts:
            account_info = {
                'name': account.name,
                'location': account.location,
                'resource_group': account.id.split('/')[4],
                'kind': getattr(account.kind, 'value', str(account.kind)) if account.kind else 'Unknown',
                'sku_name': getattr(account.sku.name, 'value', str(account.sku.name)) if account.sku and account.sku.name else 'Unknown',
                'sku_tier': getattr(account.sku.tier, 'value', str(account.sku.tier)) if account.sku and account.sku.tier else 'Unknown',
                'primary_endpoints': {
                    'blob': account.primary_endpoints.blob if account.primary_endpoints else '',
                    'file': account.primary_endpoints.file if account.primary_endpoints else ''
                }
            }
            storage_accounts.append(account_info)
            
            print(f"   📦 {account.name}")
            print(f"      Location: {account.location}")
            print(f"      SKU: {account_info['sku_name']} ({account_info['sku_tier']})")
            
            # Analyze containers and file shares
            try:
                conn_str = get_storage_account_connection_string(
                    storage_client, account_info['resource_group'], account.name
                )
                
                if conn_str:
                    # Analyze blob containers
                    containers, file_shares = analyze_storage_account_details(
                        conn_str, account_info
                    )
                    container_results.extend(containers)
                    file_share_results.extend(file_shares)
                    
            except Exception as e:
                print(f"      ⚠️  Error accessing storage details: {str(e)[:50]}...")
        
        print(f"📊 Found {len(storage_accounts)} storage accounts")
        
    except Exception as e:
        print(f"❌ Error listing storage accounts: {e}")
    
    # Generate recommendations
    recommendations = generate_recommendations(storage_accounts)
    
    # Prepare storage data
    storage_data = {
        'subscription_id': subscription_id,
        'storage_accounts': storage_accounts,
        'total_cost': 0,  # Will be populated by cost analysis
        'analysis_date': datetime.now().isoformat()
    }
    
    return {
        'container_results': container_results,
        'file_share_results': file_share_results,
        'storage_data': storage_data,
        'recommendations': recommendations
    }

def analyze_storage_account_details(conn_str, account_info):
    """Analyze containers and file shares for a storage account"""
    containers = []
    file_shares = []
    
    try:
        # Analyze blob containers
        from azure.storage.blob import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        
        container_list = list(blob_service_client.list_containers())
        print(f"      Containers: {len(container_list)}")
        
        for container in container_list[:5]:  # Limit to first 5 for performance
            try:
                container_client = blob_service_client.get_container_client(container['name'])
                blob_count = 0
                total_size = 0
                
                # Sample first 10 blobs
                for i, blob in enumerate(container_client.list_blobs()):
                    if i >= 10:
                        break
                    blob_count += 1
                    if hasattr(blob, 'size') and blob.size:
                        total_size += blob.size
                
                containers.append({
                    'account_name': account_info['name'],
                    'resource_group': account_info['resource_group'],
                    'container_name': container['name'],
                    'blob_count': blob_count,
                    'total_size_bytes': total_size,
                    'total_size_gb': total_size / (1024*1024*1024) if total_size > 0 else 0,
                    'last_modified': str(container.get('last_modified', '')),
                    'access_tier': 'Hot',
                    'sku': account_info['sku_name'],
                    'location': account_info['location']
                })
                
                if blob_count > 0:
                    print(f"         📁 {container['name']}: {blob_count} blobs, {total_size/(1024*1024):.1f}MB")
                
            except Exception as e:
                print(f"         ⚠️  Error reading container {container['name']}: {str(e)[:30]}...")
        
        # Analyze file shares
        from azure.storage.fileshare import ShareServiceClient
        file_service_client = ShareServiceClient.from_connection_string(conn_str)
        shares = list(file_service_client.list_shares())
        
        if shares:
            print(f"      File Shares: {len(shares)}")
            for share in shares:
                file_shares.append({
                    'account_name': account_info['name'],
                    'resource_group': account_info['resource_group'],
                    'share_name': share['name'],
                    'file_count': 0,
                    'total_size_gb': share.get('quota', 0),
                    'quota': share.get('quota', 0),
                    'last_modified': str(share.get('last_modified', '')),
                    'sku': account_info['sku_name'],
                    'location': account_info['location']
                })
                print(f"         📂 {share['name']}")
        
    except Exception as e:
        print(f"      ⚠️  Error analyzing storage account: {str(e)[:50]}...")
    
    return containers, file_shares

def generate_recommendations(storage_accounts):
    """Generate cost optimization recommendations"""
    recommendations = []
    
    if len(storage_accounts) > 0:
        recommendations.append({
            'type': 'Cost Optimization',
            'title': 'Review Storage Account SKUs',
            'description': f'Analyze {len(storage_accounts)} storage accounts for right-sizing opportunities',
            'priority': 'Medium',
            'potential_savings': 'TBD - Requires detailed usage analysis'
        })
    
    if len(storage_accounts) > 2:
        recommendations.append({
            'type': 'Management',
            'title': 'Consolidate Storage Accounts',
            'description': f'Consider consolidating {len(storage_accounts)} storage accounts to reduce management overhead',
            'priority': 'Low',
            'potential_savings': 'Operational efficiency gains'
        })
    
    return recommendations

def generate_multi_subscription_recommendations(all_results):
    """Generate recommendations for multi-subscription analysis"""
    recommendations = []
    
    total_subscriptions = len(all_results['subscriptions'])
    total_accounts = sum(len(sub_data.get('storage_accounts', [])) 
                        for sub_data in all_results['subscriptions'].values())
    
    recommendations.append({
        'type': 'Enterprise Management',
        'title': 'Multi-Subscription Governance',
        'description': f'Implement governance across {total_subscriptions} subscriptions and {total_accounts} storage accounts',
        'priority': 'High',
        'potential_savings': 'Significant operational efficiency'
    })
    
    if all_results['total_cost'] > 1000:
        recommendations.append({
            'type': 'Cost Optimization',
            'title': 'Enterprise Cost Review',
            'description': f'Review ${all_results["total_cost"]:.2f} in storage costs across all subscriptions',
            'priority': 'High',
            'potential_savings': f'Potential 15-30% savings (${all_results["total_cost"] * 0.15:.2f} - ${all_results["total_cost"] * 0.30:.2f})'
        })
    
    return recommendations

def generate_excel_report(container_results, file_share_results, storage_data, recommendations, analysis_type):
    """Generate comprehensive Excel CIR report"""
    print(f"\n📋 GENERATING {analysis_type.upper()} CIR EXCEL REPORT")
    print("-" * 60)
    
    try:
        excel_file = create_comprehensive_excel_report(
            container_results=container_results,
            file_share_results=file_share_results,
            storage_data=storage_data,
            recommendations=recommendations,
            cost_analysis={},
            reservations_analysis=[],
            savings_plans_analysis=[]
        )
        
        print(f"✅ CIR Excel Report Generated: {excel_file}")
        print(f"📊 Report includes: Cost Intelligence, Recommendations, Storage Analysis")
        return excel_file
        
    except Exception as e:
        print(f"⚠️  Excel report generation failed: {e}")
        return None

def save_analysis_results(results, analysis_type):
    """Save analysis results for dashboard consumption"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if analysis_type == 'single':
        filename = f"detailed_analysis_results_{timestamp}.json"
        data_to_save = results['storage_data']
    else:
        filename = f"multi_subscription_analysis_{timestamp}.json"
        data_to_save = results
    
    try:
        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=2, default=str)
        print(f"💾 Analysis results saved to: {filename}")
        return filename
    except Exception as e:
        print(f"⚠️  Failed to save results: {e}")
        return None

if __name__ == "__main__":
    success = run_unified_analysis()
    if success:
        print(f"\n🎉 Unified analysis completed successfully!")
        print("📊 Ready for dashboard: python real_data_dashboard.py")
    else:
        print(f"\n❌ Analysis failed - please check error messages above")