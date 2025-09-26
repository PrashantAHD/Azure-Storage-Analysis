#!/usr/bin/env python3
"""
Raw Data Analyzer - Show detailed Azure analysis results
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.append('.')

from azure_storage_analysis.auth import initialize_azure_clients
from azure_storage_analysis.cost_management import AzureCostAnalyzer
from azure_storage_analysis.reservations import AzureReservationAnalyzer
from azure_storage_analysis.savings_plans import AzureSavingsPlansAnalyzer

def get_detailed_analysis():
    """Get detailed analysis with raw data display"""
    
    print("🔍 DETAILED AZURE FINOPS RAW DATA ANALYSIS")
    print("=" * 80)
    
    try:
        # Initialize Azure clients
        print("📋 Initializing Azure connections...")
        credential, subscription_id, resource_client, storage_client = initialize_azure_clients()
        print(f"✅ Connected to subscription: {subscription_id}")
        
        # Get all storage accounts
        print(f"\n📦 DISCOVERING STORAGE ACCOUNTS...")
        print("-" * 60)
        
        storage_accounts = []
        try:
            for account in storage_client.storage_accounts.list():
                account_info = {
                    'name': account.name,
                    'location': account.location,
                    'resource_group': account.id.split('/')[4],  # Extract RG from resource ID
                    'kind': account.kind,
                    'sku_name': account.sku.name,
                    'sku_tier': account.sku.tier,
                    'creation_time': str(account.creation_time) if hasattr(account, 'creation_time') else 'Unknown',
                    'primary_endpoints': {
                        'blob': account.primary_endpoints.blob if account.primary_endpoints else None,
                        'file': account.primary_endpoints.file if account.primary_endpoints else None
                    }
                }
                storage_accounts.append(account_info)
                
        except Exception as e:
            print(f"❌ Error listing storage accounts: {e}")
        
        print(f"📊 Found {len(storage_accounts)} storage accounts")
        
        # Initialize data collection for Excel report
        container_results = []
        file_share_results = []
        
        # Display storage account details
        for i, account in enumerate(storage_accounts, 1):
            print(f"\n   {i}. 📦 {account['name']}")
            print(f"      Location: {account['location']}")
            print(f"      Resource Group: {account['resource_group']}")
            print(f"      Kind: {account['kind']}")
            print(f"      SKU: {account['sku_name']} ({account['sku_tier']})")
            print(f"      Blob Endpoint: {account['primary_endpoints']['blob']}")
            print(f"      File Endpoint: {account['primary_endpoints']['file']}")
            
            # Try to get containers for this account
            try:
                from azure_storage_analysis.core import get_storage_account_connection_string
                conn_str = get_storage_account_connection_string(
                    storage_client, 
                    account['resource_group'], 
                    account['name']
                )
                
                if conn_str:
                    from azure.storage.blob import BlobServiceClient
                    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
                    
                    containers = list(blob_service_client.list_containers())
                    print(f"      Containers: {len(containers)}")
                    
                    for j, container in enumerate(containers[:3], 1):  # Show first 3
                        print(f"         {j}. 📁 {container['name']}")
                        print(f"            Last Modified: {container.get('last_modified', 'Unknown')}")
                        
                        # Count blobs in container and collect data for Excel
                        blob_count = 0
                        total_size = 0
                        sample_blobs = []
                        
                        try:
                            container_client = blob_service_client.get_container_client(container['name'])
                            
                            # Sample first 10 blobs for size calculation
                            for k, blob in enumerate(container_client.list_blobs()):
                                if k >= 10:  # Limit to first 10 for speed
                                    break
                                blob_count += 1
                                if hasattr(blob, 'size') and blob.size:
                                    total_size += blob.size
                                
                                # Collect blob data for Excel
                                sample_blobs.append({
                                    'name': blob.name,
                                    'size': getattr(blob, 'size', 0),
                                    'last_modified': getattr(blob, 'last_modified', None),
                                    'content_type': getattr(blob, 'content_type', 'Unknown')
                                })
                            
                            print(f"            Sample Blobs: {blob_count} (showing first 10)")
                            if total_size > 0:
                                print(f"            Sample Size: {total_size / (1024*1024):.2f} MB")
                            
                            # Store container data for Excel report
                            container_results.append({
                                'account_name': account['name'],
                                'resource_group': account['resource_group'],
                                'container_name': container['name'],
                                'blob_count': blob_count,
                                'total_size_bytes': total_size,
                                'total_size_mb': total_size / (1024*1024) if total_size > 0 else 0,
                                'total_size_gb': total_size / (1024*1024*1024) if total_size > 0 else 0,
                                'last_modified': str(container.get('last_modified', '')),
                                'access_tier': 'Hot',  # Default assumption for display
                                'sample_blobs': sample_blobs,
                                'sku': account['sku_name'],
                                'location': account['location']
                            })
                                
                        except Exception as e:
                            print(f"            Error reading container: {str(e)[:50]}...")
                    
                    # Also check for File Shares
                    try:
                        from azure.storage.fileshare import ShareServiceClient
                        file_service_client = ShareServiceClient.from_connection_string(conn_str)
                        shares = list(file_service_client.list_shares())
                        
                        if shares:
                            print(f"      File Shares: {len(shares)}")
                            for share in shares[:3]:  # Show first 3
                                print(f"         📂 {share['name']}")
                                
                                # Store file share data for Excel report
                                file_share_results.append({
                                    'account_name': account['name'],
                                    'resource_group': account['resource_group'],
                                    'share_name': share['name'],
                                    'file_count': 0,  # Would need additional API call to count files
                                    'total_size_gb': share.get('quota', 0),  # Using quota as size approximation
                                    'quota': share.get('quota', 0),
                                    'last_modified': str(share.get('last_modified', '')),
                                    'sku': account['sku_name'],
                                    'location': account['location']
                                })
                                
                    except Exception as e:
                        pass  # File shares may not be supported
                
            except Exception as e:
                print(f"      Error accessing containers: {str(e)[:50]}...")
        
        # Cost Analysis
        print(f"\n💰 COST ANALYSIS")
        print("-" * 60)
        
        try:
            cost_analyzer = AzureCostAnalyzer(credential, subscription_id)
            
            # Get last 3 months of cost data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            print(f"📅 Analyzing costs from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # Storage costs
            storage_costs = cost_analyzer.get_storage_costs(
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            
            if storage_costs:
                print(f"✅ Retrieved storage cost data")
                
                # Process cost data
                total_cost = 0
                service_costs = {}
                
                for cost_item in storage_costs:
                    if isinstance(cost_item, dict):
                        amount = cost_item.get('cost', 0) or cost_item.get('PreTaxCost', 0)
                        service = cost_item.get('ServiceName', 'Unknown')
                        
                        if amount:
                            total_cost += float(amount)
                            service_costs[service] = service_costs.get(service, 0) + float(amount)
                
                print(f"💵 Total Storage Costs (90 days): ${total_cost:.2f}")
                print(f"💵 Monthly Average: ${total_cost / 3:.2f}")
                
                if service_costs:
                    print(f"\n📊 Cost by Service:")
                    for service, cost in sorted(service_costs.items(), key=lambda x: x[1], reverse=True):
                        print(f"   • {service}: ${cost:.2f}")
            else:
                print("⚠️  No storage cost data available")
                
        except Exception as e:
            print(f"❌ Error in cost analysis: {e}")
        
        # Reservations Analysis
        print(f"\n🏷️  RESERVATIONS ANALYSIS")
        print("-" * 60)
        
        try:
            reservation_analyzer = AzureReservationAnalyzer(credential, subscription_id)
            reservations = reservation_analyzer.get_reservations()
            
            if reservations:
                print(f"✅ Found {len(reservations)} reservations")
                for i, reservation in enumerate(reservations[:3], 1):
                    print(f"   {i}. {reservation.get('displayName', 'Unknown')}")
                    print(f"      Status: {reservation.get('provisioningState', 'Unknown')}")
                    print(f"      Scope: {reservation.get('appliedScopeType', 'Unknown')}")
            else:
                print("📋 No reservations found")
                
        except Exception as e:
            print(f"❌ Error in reservations analysis: {e}")
        
        # Savings Plans Analysis
        print(f"\n💡 SAVINGS PLANS ANALYSIS")
        print("-" * 60)
        
        try:
            savings_analyzer = AzureSavingsPlansAnalyzer(credential, subscription_id)
            savings_plans = savings_analyzer.get_savings_plans()
            
            if savings_plans:
                print(f"✅ Found {len(savings_plans)} savings plans")
                for i, plan in enumerate(savings_plans[:3], 1):
                    print(f"   {i}. {plan.get('displayName', 'Unknown')}")
                    print(f"      Status: {plan.get('provisioningState', 'Unknown')}")
                    print(f"      Commitment: {plan.get('commitment', {}).get('amount', 'Unknown')}")
            else:
                print("📋 No savings plans found")
                
        except Exception as e:
            print(f"❌ Error in savings plans analysis: {e}")
        
        # Generate Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 60)
        
        recommendations = []
        
        # Basic recommendations based on findings
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
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. 🎯 {rec['title']}")
            print(f"      Type: {rec['type']}")
            print(f"      Priority: {rec['priority']}")
            print(f"      Description: {rec['description']}")
            print(f"      Potential Savings: {rec['potential_savings']}")
            print()
        
        # Summary
        print(f"\n📈 ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"🔸 Subscription: {subscription_id}")
        print(f"🔸 Storage Accounts: {len(storage_accounts)}")
        print(f"🔸 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔸 Recommendations: {len(recommendations)}")
        
        if 'total_cost' in locals():
            print(f"🔸 90-Day Storage Costs: ${total_cost:.2f}")
            print(f"🔸 Monthly Average: ${total_cost / 3:.2f}")
        
        print(f"\n✅ DETAILED ANALYSIS COMPLETE!")
        print("=" * 80)
        
        # Generate CIR Excel Report
        print(f"\n📋 GENERATING CIR EXCEL REPORT")
        print("-" * 60)
        
        try:
            from azure_storage_analysis.unified_reporting import create_comprehensive_excel_report
            
            # Prepare data for Excel report
            excel_data = {
                'subscription_id': subscription_id,
                'storage_accounts': storage_accounts,
                'total_cost': locals().get('total_cost', 0),
                'service_costs': locals().get('service_costs', {}),
                'recommendations': recommendations,
                'analysis_date': datetime.now().isoformat()
            }
            
            # Generate Excel report with actual collected data
            excel_file = create_comprehensive_excel_report(
                container_results=container_results,
                file_share_results=file_share_results,
                storage_data=excel_data,
                recommendations=recommendations,
                cost_analysis=locals().get('service_costs', {}),
                reservations_analysis=locals().get('reservations', []),
                savings_plans_analysis=locals().get('savings_plans', [])
            )
            
            print(f"✅ CIR Excel Report Generated: {excel_file}")
            print(f"📊 Report includes: Cost Intelligence, Recommendations, Storage Analysis")
            
        except Exception as e:
            print(f"⚠️  Excel report generation failed: {e}")
            print("💡 JSON data will still be saved for dashboard use")
        
        # Return structured data
        return {
            'subscription_id': subscription_id,
            'storage_accounts': storage_accounts,
            'total_cost': locals().get('total_cost', 0),
            'service_costs': locals().get('service_costs', {}),
            'reservations': locals().get('reservations', []),
            'savings_plans': locals().get('savings_plans', []),
            'recommendations': recommendations,
            'analysis_date': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = get_detailed_analysis()
    
    if results:
        # Save to JSON file for further analysis
        output_file = f"detailed_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Detailed results saved to: {output_file}")
        except Exception as e:
            print(f"⚠️  Could not save results file: {e}")