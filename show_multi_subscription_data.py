#!/usr/bin/env python3
"""
Multi-Subscription Azure FinOps Analysis
Enhanced version with support for multiple Azure subscriptions
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.append('.')

from azure_storage_analysis.auth import initialize_multi_subscription_analysis, get_all_storage_accounts_multi_subscription
from azure_storage_analysis.cost_management import AzureCostAnalyzer
from azure_storage_analysis.reservations import AzureReservationAnalyzer
from azure_storage_analysis.savings_plans import AzureSavingsPlansAnalyzer

def get_multi_subscription_analysis():
    """Get detailed analysis across multiple Azure subscriptions"""
    
    print("🔍 MULTI-SUBSCRIPTION AZURE FINOPS CIR ANALYSIS")
    print("=" * 80)
    
    try:
        # Initialize multi-subscription Azure clients
        print("📋 Initializing multi-subscription Azure connections...")
        
        # This will present a menu if multiple subscriptions are available
        credential, subscription_ids = initialize_multi_subscription_analysis()
        
        if not subscription_ids:
            print("❌ No subscriptions found or accessible")
            return None
            
        print(f"✅ Connected to {len(subscription_ids)} subscription(s)")
        
        # Aggregate results across all subscriptions
        all_results = {
            'subscriptions': {},
            'total_storage_accounts': 0,
            'total_cost': 0,
            'aggregated_recommendations': [],
            'analysis_date': datetime.now().isoformat()
        }
        
        for sub_id in subscription_ids:
            print(f"\n📦 ANALYZING SUBSCRIPTION: {sub_id}")
            print("-" * 60)
            
            try:
                # Get storage accounts for this subscription
                storage_accounts = get_all_storage_accounts_multi_subscription(credential, [sub_id])
                
                if storage_accounts:
                    storage_account_data = []
                    for account in storage_accounts:
                        account_info = {
                            'name': account.name,
                            'location': account.location,
                            'resource_group': account.id.split('/')[4],
                            'kind': account.kind,
                            'sku_name': account.sku.name,
                            'sku_tier': account.sku.tier,
                            'creation_time': str(account.creation_time) if hasattr(account, 'creation_time') else 'Unknown',
                            'subscription_id': sub_id,
                            'primary_endpoints': {
                                'blob': account.primary_endpoints.blob if account.primary_endpoints else None,
                                'file': account.primary_endpoints.file if account.primary_endpoints else None
                            }
                        }
                        storage_account_data.append(account_info)
                    
                    print(f"📊 Found {len(storage_account_data)} storage accounts")
                    for i, account in enumerate(storage_account_data, 1):
                        print(f"   {i}. 📦 {account['name']} ({account['location']}) - {account['sku_name']}")
                
                # Cost Analysis per subscription
                print(f"\n💰 COST ANALYSIS FOR {sub_id[:8]}...")
                try:
                    cost_analyzer = AzureCostAnalyzer(credential, sub_id)
                    
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=90)
                    
                    # This might need adjustment based on your cost analyzer implementation
                    storage_costs = cost_analyzer.get_monthly_storage_costs()
                    
                    sub_total_cost = 0
                    if storage_costs:
                        for cost_item in storage_costs:
                            if isinstance(cost_item, dict):
                                amount = cost_item.get('cost', 0) or cost_item.get('PreTaxCost', 0)
                                if amount:
                                    sub_total_cost += float(amount)
                    
                    print(f"💵 Subscription Cost (90 days): ${sub_total_cost:.2f}")
                    all_results['total_cost'] += sub_total_cost
                    
                except Exception as e:
                    print(f"⚠️  Cost analysis failed for {sub_id[:8]}: {e}")
                    sub_total_cost = 0
                
                # Store subscription results
                all_results['subscriptions'][sub_id] = {
                    'storage_accounts': storage_account_data,
                    'account_count': len(storage_account_data),
                    'cost_90_days': sub_total_cost,
                    'regions': list(set([acc['location'] for acc in storage_account_data]))
                }
                
                all_results['total_storage_accounts'] += len(storage_account_data)
                
            except Exception as e:
                print(f"❌ Error analyzing subscription {sub_id}: {e}")
                continue
        
        # Generate multi-subscription recommendations
        print(f"\n💡 MULTI-SUBSCRIPTION RECOMMENDATIONS")
        print("-" * 60)
        
        recommendations = []
        
        # Cross-subscription optimization opportunities
        if all_results['total_storage_accounts'] > 1:
            recommendations.append({
                'type': 'Multi-Subscription Optimization',
                'title': 'Cross-Subscription Storage Consolidation',
                'description': f'Analyze {all_results["total_storage_accounts"]} storage accounts across {len(subscription_ids)} subscriptions for consolidation opportunities',
                'priority': 'Medium',
                'potential_savings': 'TBD - Requires cross-subscription analysis'
            })
        
        if len(subscription_ids) > 1:
            recommendations.append({
                'type': 'Cost Management',
                'title': 'Multi-Subscription Cost Monitoring',
                'description': f'Implement unified cost tracking across {len(subscription_ids)} subscriptions',
                'priority': 'High',
                'potential_savings': '15-25% through better visibility'
            })
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. 🎯 {rec['title']}")
            print(f"      Type: {rec['type']}")
            print(f"      Priority: {rec['priority']}")
            print(f"      Description: {rec['description']}")
            print(f"      Potential Savings: {rec['potential_savings']}")
            print()
        
        all_results['aggregated_recommendations'] = recommendations
        
        # Multi-Subscription Summary
        print(f"\n📈 MULTI-SUBSCRIPTION ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"🔸 Subscriptions Analyzed: {len(subscription_ids)}")
        print(f"🔸 Total Storage Accounts: {all_results['total_storage_accounts']}")
        print(f"🔸 Total 90-Day Costs: ${all_results['total_cost']:.2f}")
        print(f"🔸 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔸 Recommendations: {len(recommendations)}")
        
        # Regional distribution across subscriptions
        all_regions = set()
        for sub_data in all_results['subscriptions'].values():
            all_regions.update(sub_data['regions'])
        print(f"🔸 Regions: {', '.join(sorted(all_regions))}")
        
        # Generate Multi-Subscription CIR Excel Report
        print(f"\n📋 GENERATING MULTI-SUBSCRIPTION CIR EXCEL REPORT")
        print("-" * 60)
        
        try:
            from azure_storage_analysis.unified_reporting import create_comprehensive_excel_report
            
            # Aggregate all storage accounts for Excel report
            all_storage_accounts = []
            for sub_data in all_results['subscriptions'].values():
                all_storage_accounts.extend(sub_data['storage_accounts'])
            
            # Generate multi-subscription Excel report
            excel_file = create_comprehensive_excel_report(
                container_results=[],  # Will be populated with actual container data
                file_share_results=[],  # Will be populated with actual file share data
                storage_data={
                    'subscription_ids': subscription_ids,
                    'storage_accounts': all_storage_accounts,
                    'total_cost': all_results['total_cost'],
                    'analysis_date': all_results['analysis_date'],
                    'multi_subscription': True
                },
                recommendations=all_results['aggregated_recommendations'],
                cost_analysis={'total_cost': all_results['total_cost']},
                reservations_analysis=[],
                savings_plans_analysis=[]
            )
            
            print(f"✅ Multi-Subscription CIR Excel Report Generated: {excel_file}")
            print(f"📊 Report includes: Cross-subscription analysis, Aggregated costs, Multi-sub recommendations")
            
        except Exception as e:
            print(f"⚠️  Multi-subscription Excel report generation failed: {e}")
            print("💡 JSON data will still be saved for dashboard use")
        
        print(f"\n✅ MULTI-SUBSCRIPTION ANALYSIS COMPLETE!")
        print("=" * 80)
        
        return all_results
        
    except Exception as e:
        print(f"❌ Error during multi-subscription analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = get_multi_subscription_analysis()
    
    if results:
        # Save to JSON file for dashboard consumption
        output_file = f"multi_subscription_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Multi-subscription results saved to: {output_file}")
        except Exception as e:
            print(f"⚠️  Could not save results file: {e}")
    else:
        print("❌ Multi-subscription analysis failed")