# Azure Savings Plans Analysis and Recommendations

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pandas as pd

logger = logging.getLogger(__name__)

class AzureSavingsPlansAnalyzer:
    """Analyze Azure usage and provide Savings Plans recommendations"""
    
    def __init__(self, credential, subscription_ids: List[str]):
        """
        Initialize Azure Savings Plans Analyzer
        
        Args:
            credential: Azure credential object  
            subscription_ids: List of subscription IDs to analyze
        """
        self.credential = credential
        self.subscription_ids = subscription_ids
        self.logger = logging.getLogger(__name__)
        
    def analyze_savings_plans_opportunities(self, usage_data: Dict, cost_data: Dict) -> Dict:
        """
        Analyze usage patterns for Savings Plans opportunities
        
        Args:
            usage_data: Historical usage data
            cost_data: Historical cost data from cost management
            
        Returns:
            Dictionary with Savings Plans recommendations
        """
        self.logger.info("Analyzing Savings Plans opportunities...")
        
        recommendations = {
            'compute_savings_plans': [],
            'azure_savings_plans': [],
            'summary': {},
            'comparison_matrix': {},
            'action_plan': []
        }
        
        # Analyze Compute Savings Plans
        compute_plans = self._analyze_compute_savings_plans(cost_data)
        recommendations['compute_savings_plans'] = compute_plans
        
        # Analyze Azure Savings Plans (broader coverage)
        azure_plans = self._analyze_azure_savings_plans(cost_data)
        recommendations['azure_savings_plans'] = azure_plans
        
        # Create comparison matrix
        recommendations['comparison_matrix'] = self._create_savings_plans_comparison(compute_plans, azure_plans)
        
        # Generate summary
        recommendations['summary'] = self._generate_savings_plans_summary(compute_plans + azure_plans)
        
        # Create action plan
        recommendations['action_plan'] = self._generate_savings_plans_action_plan(compute_plans + azure_plans)
        
        return recommendations
    
    def _analyze_compute_savings_plans(self, cost_data: Dict) -> List[Dict]:
        """
        Analyze Compute Savings Plans opportunities
        Covers: VMs, Container Instances, Azure Functions, Dedicated Hosts
        """
        compute_plans = []
        
        for sub_id in self.subscription_ids:
            sub_spending = cost_data.get('subscription_spending', {}).get(sub_id, {})
            
            # Calculate monthly compute spending
            monthly_compute_costs = []
            compute_services = ['Virtual Machines', 'Container Instances', 'Azure Functions', 'Dedicated Host']
            
            for month_data in sub_spending.values():
                monthly_compute = 0
                storage_costs = month_data.get('storage_costs', {})
                
                # Note: This is simplified - in reality you'd get actual compute costs
                # For demonstration, we'll estimate compute costs
                total_month_cost = month_data.get('total_cost', 0)
                estimated_compute = total_month_cost * 0.3  # Assume 30% is compute
                
                if estimated_compute > 0:
                    monthly_compute_costs.append(estimated_compute)
            
            if len(monthly_compute_costs) >= 2:
                avg_monthly_compute = sum(monthly_compute_costs) / len(monthly_compute_costs)
                consistency_score = self._calculate_spending_consistency(monthly_compute_costs)
                
                # Generate Compute Savings Plan recommendations
                if avg_monthly_compute > 200:  # Minimum threshold
                    plan_options = self._calculate_compute_savings_plan_options(avg_monthly_compute, consistency_score)
                    
                    for option in plan_options:
                        compute_plans.append({
                            'subscription_id': sub_id,
                            'plan_type': 'Compute Savings Plan',
                            'scope': option['scope'],
                            'term': option['term'],
                            'hourly_commitment': option['hourly_commitment'],
                            'monthly_commitment': option['monthly_commitment'],
                            'annual_commitment': option['annual_commitment'],
                            'current_monthly_spend': avg_monthly_compute,
                            'estimated_monthly_savings': option['monthly_savings'],
                            'estimated_annual_savings': option['annual_savings'],
                            'savings_percentage': option['savings_percentage'],
                            'covered_services': ['Virtual Machines', 'Container Instances', 'Azure Functions'],
                            'flexibility': option['flexibility'],
                            'consistency_score': consistency_score,
                            'confidence': option['confidence'],
                            'recommendation_priority': self._calculate_savings_priority(option, consistency_score)
                        })
        
        return compute_plans
    
    def _analyze_azure_savings_plans(self, cost_data: Dict) -> List[Dict]:
        """
        Analyze Azure Savings Plans opportunities (broader service coverage)
        Covers: Compute + Storage + Networking + Databases + more
        """
        azure_plans = []
        
        for sub_id in self.subscription_ids:
            sub_spending = cost_data.get('subscription_spending', {}).get(sub_id, {})
            
            # Calculate total Azure spending
            monthly_total_costs = []
            
            for month_data in sub_spending.values():
                total_cost = month_data.get('total_cost', 0)
                if total_cost > 0:
                    monthly_total_costs.append(total_cost)
            
            if len(monthly_total_costs) >= 2:
                avg_monthly_total = sum(monthly_total_costs) / len(monthly_total_costs)
                consistency_score = self._calculate_spending_consistency(monthly_total_costs)
                
                # Generate Azure Savings Plan recommendations
                if avg_monthly_total > 500:  # Higher threshold for broader plans
                    plan_options = self._calculate_azure_savings_plan_options(avg_monthly_total, consistency_score)
                    
                    for option in plan_options:
                        azure_plans.append({
                            'subscription_id': sub_id,
                            'plan_type': 'Azure Savings Plan',
                            'scope': option['scope'],
                            'term': option['term'],
                            'hourly_commitment': option['hourly_commitment'],
                            'monthly_commitment': option['monthly_commitment'],
                            'annual_commitment': option['annual_commitment'],
                            'current_monthly_spend': avg_monthly_total,
                            'estimated_monthly_savings': option['monthly_savings'],
                            'estimated_annual_savings': option['annual_savings'],
                            'savings_percentage': option['savings_percentage'],
                            'covered_services': ['Compute', 'Storage', 'Networking', 'Databases', 'Analytics'],
                            'flexibility': option['flexibility'],
                            'consistency_score': consistency_score,
                            'confidence': option['confidence'],
                            'recommendation_priority': self._calculate_savings_priority(option, consistency_score)
                        })
        
        return azure_plans
    
    def _calculate_compute_savings_plan_options(self, avg_monthly_spend: float, consistency_score: float) -> List[Dict]:
        """Calculate Compute Savings Plan options and savings"""
        options = []
        
        # Conservative commitment (70% of average spend)
        conservative_monthly = avg_monthly_spend * 0.7
        conservative_hourly = conservative_monthly / (30 * 24)
        
        # 1-Year Compute Savings Plan (conservative)
        savings_1yr_conservative = conservative_monthly * 0.17  # ~17% savings
        options.append({
            'scope': 'Conservative (70% of usage)',
            'term': '1 Year',
            'hourly_commitment': round(conservative_hourly, 2),
            'monthly_commitment': round(conservative_monthly, 2),
            'annual_commitment': round(conservative_monthly * 12, 2),
            'monthly_savings': round(savings_1yr_conservative, 2),
            'annual_savings': round(savings_1yr_conservative * 12, 2),
            'savings_percentage': 17,
            'flexibility': 'High - covers VMs, Containers, Functions across regions and sizes',
            'confidence': 'High' if consistency_score > 0.7 else 'Medium'
        })
        
        # 3-Year Compute Savings Plan (conservative)
        savings_3yr_conservative = conservative_monthly * 0.28  # ~28% savings
        options.append({
            'scope': 'Conservative (70% of usage)',
            'term': '3 Years',
            'hourly_commitment': round(conservative_hourly, 2),
            'monthly_commitment': round(conservative_monthly, 2),
            'annual_commitment': round(conservative_monthly * 12, 2),
            'monthly_savings': round(savings_3yr_conservative, 2),
            'annual_savings': round(savings_3yr_conservative * 12, 2),
            'savings_percentage': 28,
            'flexibility': 'High - covers VMs, Containers, Functions across regions and sizes',
            'confidence': 'High' if consistency_score > 0.8 else 'Medium'
        })
        
        # Aggressive commitment (90% of average spend) - only if high consistency
        if consistency_score > 0.8:
            aggressive_monthly = avg_monthly_spend * 0.9
            aggressive_hourly = aggressive_monthly / (30 * 24)
            
            # 3-Year Aggressive
            savings_3yr_aggressive = aggressive_monthly * 0.28
            options.append({
                'scope': 'Aggressive (90% of usage)',
                'term': '3 Years',
                'hourly_commitment': round(aggressive_hourly, 2),
                'monthly_commitment': round(aggressive_monthly, 2),
                'annual_commitment': round(aggressive_monthly * 12, 2),
                'monthly_savings': round(savings_3yr_aggressive, 2),
                'annual_savings': round(savings_3yr_aggressive * 12, 2),
                'savings_percentage': 28,
                'flexibility': 'High - covers VMs, Containers, Functions across regions and sizes',
                'confidence': 'Medium'  # Higher risk due to aggressive commitment
            })
        
        return options
    
    def _calculate_azure_savings_plan_options(self, avg_monthly_spend: float, consistency_score: float) -> List[Dict]:
        """Calculate Azure Savings Plan options (broader coverage)"""
        options = []
        
        # Conservative commitment (60% of average spend)
        conservative_monthly = avg_monthly_spend * 0.6
        conservative_hourly = conservative_monthly / (30 * 24)
        
        # 1-Year Azure Savings Plan (conservative)
        savings_1yr_conservative = conservative_monthly * 0.11  # ~11% savings
        options.append({
            'scope': 'Conservative (60% of total usage)',
            'term': '1 Year',
            'hourly_commitment': round(conservative_hourly, 2),
            'monthly_commitment': round(conservative_monthly, 2),
            'annual_commitment': round(conservative_monthly * 12, 2),
            'monthly_savings': round(savings_1yr_conservative, 2),
            'annual_savings': round(savings_1yr_conservative * 12, 2),
            'savings_percentage': 11,
            'flexibility': 'Highest - covers most Azure services across regions',
            'confidence': 'High' if consistency_score > 0.6 else 'Medium'
        })
        
        # 3-Year Azure Savings Plan (conservative)
        savings_3yr_conservative = conservative_monthly * 0.17  # ~17% savings
        options.append({
            'scope': 'Conservative (60% of total usage)',
            'term': '3 Years',
            'hourly_commitment': round(conservative_hourly, 2),
            'monthly_commitment': round(conservative_monthly, 2),
            'annual_commitment': round(conservative_monthly * 12, 2),
            'monthly_savings': round(savings_3yr_conservative, 2),
            'annual_savings': round(savings_3yr_conservative * 12, 2),
            'savings_percentage': 17,
            'flexibility': 'Highest - covers most Azure services across regions',
            'confidence': 'High' if consistency_score > 0.7 else 'Medium'
        })
        
        return options
    
    def _calculate_spending_consistency(self, monthly_costs: List[float]) -> float:
        """Calculate spending consistency score (0-1 scale)"""
        if len(monthly_costs) < 2:
            return 0
        
        mean_cost = sum(monthly_costs) / len(monthly_costs)
        if mean_cost == 0:
            return 0
        
        # Calculate coefficient of variation
        variance = sum((cost - mean_cost) ** 2 for cost in monthly_costs) / len(monthly_costs)
        std_dev = variance ** 0.5
        cv = std_dev / mean_cost
        
        # Convert to consistency score
        consistency = max(0, 1 - cv)
        return min(1, consistency)
    
    def _calculate_savings_priority(self, plan_option: Dict, consistency_score: float) -> str:
        """Calculate recommendation priority for savings plan"""
        annual_savings = plan_option.get('annual_savings', 0)
        savings_pct = plan_option.get('savings_percentage', 0)
        confidence = plan_option.get('confidence', 'Low')
        
        if confidence == 'High' and savings_pct > 15 and annual_savings > 2000:
            return 'High'
        elif confidence in ['High', 'Medium'] and savings_pct > 10 and annual_savings > 1000:
            return 'Medium'
        else:
            return 'Low'
    
    def _create_savings_plans_comparison(self, compute_plans: List[Dict], azure_plans: List[Dict]) -> Dict:
        """Create comparison matrix between Compute and Azure Savings Plans"""
        comparison = {
            'plan_types': [],
            'comparison_factors': [
                'Service Coverage',
                'Flexibility',
                'Savings Percentage',
                'Commitment Level',
                'Best For'
            ]
        }
        
        if compute_plans:
            best_compute = max(compute_plans, key=lambda x: x.get('estimated_annual_savings', 0))
            comparison['plan_types'].append({
                'type': 'Compute Savings Plan',
                'service_coverage': 'VMs, Container Instances, Functions',
                'flexibility': 'High (across regions, VM sizes)',
                'savings_percentage': f"{best_compute.get('savings_percentage', 0)}%",
                'commitment_level': f"${best_compute.get('monthly_commitment', 0):.0f}/month",
                'best_for': 'Consistent compute workloads',
                'annual_savings': best_compute.get('estimated_annual_savings', 0)
            })
        
        if azure_plans:
            best_azure = max(azure_plans, key=lambda x: x.get('estimated_annual_savings', 0))
            comparison['plan_types'].append({
                'type': 'Azure Savings Plan',
                'service_coverage': 'Compute + Storage + Networking + Databases',
                'flexibility': 'Highest (most Azure services)',
                'savings_percentage': f"{best_azure.get('savings_percentage', 0)}%",
                'commitment_level': f"${best_azure.get('monthly_commitment', 0):.0f}/month",
                'best_for': 'Diverse Azure service usage',
                'annual_savings': best_azure.get('estimated_annual_savings', 0)
            })
        
        return comparison
    
    def _generate_savings_plans_summary(self, all_plans: List[Dict]) -> Dict:
        """Generate summary statistics for Savings Plans recommendations"""
        if not all_plans:
            return {
                'total_plans': 0,
                'total_annual_savings': 0,
                'total_annual_commitment': 0,
                'high_priority_count': 0,
                'average_savings_percentage': 0
            }
        
        total_annual_savings = sum(plan.get('estimated_annual_savings', 0) for plan in all_plans)
        total_annual_commitment = sum(plan.get('annual_commitment', 0) for plan in all_plans)
        high_priority_count = sum(1 for plan in all_plans if plan.get('recommendation_priority') == 'High')
        
        savings_percentages = [plan.get('savings_percentage', 0) for plan in all_plans]
        avg_savings_pct = sum(savings_percentages) / len(savings_percentages) if savings_percentages else 0
        
        return {
            'total_plans': len(all_plans),
            'total_annual_savings': round(total_annual_savings, 2),
            'total_annual_commitment': round(total_annual_commitment, 2),
            'net_annual_benefit': round(total_annual_savings, 2),  # Savings plans don't have upfront costs
            'high_priority_count': high_priority_count,
            'medium_priority_count': sum(1 for plan in all_plans if plan.get('recommendation_priority') == 'Medium'),
            'low_priority_count': sum(1 for plan in all_plans if plan.get('recommendation_priority') == 'Low'),
            'average_savings_percentage': round(avg_savings_pct, 2),
            'compute_plans_count': sum(1 for plan in all_plans if plan.get('plan_type') == 'Compute Savings Plan'),
            'azure_plans_count': sum(1 for plan in all_plans if plan.get('plan_type') == 'Azure Savings Plan')
        }
    
    def _generate_savings_plans_action_plan(self, all_plans: List[Dict]) -> List[Dict]:
        """Generate prioritized action plan for implementing Savings Plans"""
        action_plan = []
        
        # Sort by priority and savings
        sorted_plans = sorted(all_plans,
                            key=lambda x: (
                                {'High': 3, 'Medium': 2, 'Low': 1}.get(x.get('recommendation_priority', 'Low'), 1),
                                x.get('estimated_annual_savings', 0)
                            ),
                            reverse=True)
        
        for i, plan in enumerate(sorted_plans[:5], 1):  # Top 5 recommendations
            action = {
                'priority_rank': i,
                'action_type': 'Purchase Savings Plan',
                'plan_type': plan.get('plan_type', 'Unknown'),
                'subscription_id': plan.get('subscription_id', 'Unknown'),
                'commitment_details': f"${plan.get('monthly_commitment', 0):.0f}/month ({plan.get('term', 'Unknown')})",
                'hourly_commitment': f"${plan.get('hourly_commitment', 0):.2f}/hour",
                'estimated_annual_savings': plan.get('estimated_annual_savings', 0),
                'savings_percentage': f"{plan.get('savings_percentage', 0)}%",
                'covered_services': ', '.join(plan.get('covered_services', [])),
                'flexibility_level': plan.get('flexibility', 'Unknown'),
                'confidence_level': plan.get('confidence', 'Unknown'),
                'next_steps': [
                    'Review historical usage to validate commitment level',
                    'Ensure budget approval for ongoing hourly commitment',
                    'Start with conservative commitment to minimize risk',
                    'Purchase Savings Plan through Azure portal or CLI',
                    'Monitor usage against commitment and adjust if needed',
                    'Set up alerts for commitment utilization'
                ]
            }
            action_plan.append(action)
        
        return action_plan

    def compare_reservations_vs_savings_plans(self, reservations_data: Dict, savings_plans_data: Dict) -> Dict:
        """
        Compare Reserved Instances vs Savings Plans to help choose the best option
        
        Args:
            reservations_data: Reservation recommendations
            savings_plans_data: Savings Plans recommendations
            
        Returns:
            Comparison analysis and recommendations
        """
        comparison = {
            'summary': {},
            'detailed_comparison': [],
            'recommendations': []
        }
        
        # Calculate totals
        ri_total_savings = reservations_data.get('total_potential_savings', 0)
        ri_upfront_cost = sum(
            rec.get('upfront_cost', 0) 
            for recs in [reservations_data.get('blob_storage_reservations', []), 
                        reservations_data.get('files_reservations', [])]
            for rec in recs
        )
        
        sp_total_savings = savings_plans_data.get('summary', {}).get('total_annual_savings', 0)
        sp_commitment = savings_plans_data.get('summary', {}).get('total_annual_commitment', 0)
        
        comparison['summary'] = {
            'reservations': {
                'annual_savings': ri_total_savings,
                'upfront_investment': ri_upfront_cost,
                'net_first_year': ri_total_savings - ri_upfront_cost,
                'flexibility': 'Low (specific services/regions)',
                'coverage': 'Storage services only'
            },
            'savings_plans': {
                'annual_savings': sp_total_savings,
                'upfront_investment': 0,
                'net_first_year': sp_total_savings,
                'flexibility': 'High (cross-service, cross-region)',
                'coverage': 'Broad service coverage'
            }
        }
        
        # Generate recommendations
        if ri_total_savings > sp_total_savings and ri_upfront_cost < ri_total_savings:
            comparison['recommendations'].append({
                'priority': 'High',
                'recommendation': 'Focus on Reserved Instances',
                'reasoning': 'Higher savings potential with manageable upfront costs'
            })
        elif sp_total_savings > ri_total_savings * 0.8:
            comparison['recommendations'].append({
                'priority': 'High', 
                'recommendation': 'Focus on Savings Plans',
                'reasoning': 'Competitive savings with higher flexibility and no upfront costs'
            })
        else:
            comparison['recommendations'].append({
                'priority': 'Medium',
                'recommendation': 'Hybrid Approach',
                'reasoning': 'Combine both strategies for maximum optimization'
            })
        
        return comparison