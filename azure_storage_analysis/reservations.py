# Azure Reserved Instances Analysis and Recommendations

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pandas as pd

logger = logging.getLogger(__name__)

class AzureReservationAnalyzer:
    """Analyze Azure usage patterns and provide Reserved Instance recommendations"""
    
    def __init__(self, credential, subscription_ids: List[str]):
        """
        Initialize Azure Reservation Analyzer
        
        Args:
            credential: Azure credential object
            subscription_ids: List of subscription IDs to analyze
        """
        self.credential = credential
        self.subscription_ids = subscription_ids
        self.logger = logging.getLogger(__name__)
        
    def analyze_storage_reservation_opportunities(self, usage_data: Dict) -> Dict:
        """
        Analyze storage usage patterns for reservation opportunities
        
        Args:
            usage_data: Historical storage usage data from cost management
            
        Returns:
            Dictionary with storage reservation recommendations
        """
        self.logger.info("Analyzing storage reservation opportunities...")
        
        recommendations = {
            'blob_storage_reservations': [],
            'files_reservations': [], 
            'summary': {},
            'total_potential_savings': 0
        }
        
        # Analyze Blob Storage reservations
        blob_recommendations = self._analyze_blob_storage_reservations(usage_data)
        recommendations['blob_storage_reservations'] = blob_recommendations
        
        # Analyze Azure Files reservations
        files_recommendations = self._analyze_files_reservations(usage_data)
        recommendations['files_reservations'] = files_recommendations
        
        # Calculate total potential savings
        total_savings = sum(rec.get('annual_savings', 0) for rec in blob_recommendations + files_recommendations)
        recommendations['total_potential_savings'] = total_savings
        
        # Generate summary
        recommendations['summary'] = self._generate_reservation_summary(blob_recommendations + files_recommendations)
        
        return recommendations
    
    def _analyze_blob_storage_reservations(self, usage_data: Dict) -> List[Dict]:
        """Analyze Blob Storage usage for reservation opportunities"""
        blob_recommendations = []
        
        for sub_id in self.subscription_ids:
            sub_usage = usage_data.get('subscription_spending', {}).get(sub_id, {})
            
            # Calculate average monthly Blob Storage costs
            blob_costs = []
            for month_data in sub_usage.values():
                storage_costs = month_data.get('storage_costs', {})
                blob_cost = storage_costs.get('Azure Blob Storage', 0)
                if blob_cost > 0:
                    blob_costs.append(blob_cost)
            
            if len(blob_costs) >= 2:  # Need at least 2 months of data
                avg_monthly_cost = sum(blob_costs) / len(blob_costs)
                consistency_score = self._calculate_cost_consistency(blob_costs)
                
                # Recommend reservation if cost is significant and consistent
                if avg_monthly_cost > 100 and consistency_score > 0.7:
                    # Calculate reservation tiers and savings
                    reservation_tiers = self._calculate_blob_reservation_tiers(avg_monthly_cost)
                    
                    for tier in reservation_tiers:
                        if tier['confidence'] >= 'Medium':
                            blob_recommendations.append({
                                'subscription_id': sub_id,
                                'service': 'Azure Blob Storage',
                                'reservation_type': tier['type'],
                                'storage_type': tier['storage_type'],
                                'redundancy': tier['redundancy'],
                                'capacity_tb': tier['capacity_tb'],
                                'term': tier['term'],
                                'monthly_cost_current': avg_monthly_cost,
                                'monthly_cost_reserved': tier['reserved_monthly_cost'],
                                'monthly_savings': tier['monthly_savings'],
                                'annual_savings': tier['annual_savings'],
                                'upfront_cost': tier['upfront_cost'],
                                'payback_months': tier['payback_months'],
                                'consistency_score': consistency_score,
                                'confidence': tier['confidence'],
                                'recommendation_priority': self._calculate_priority(tier)
                            })
        
        return blob_recommendations
    
    def _analyze_files_reservations(self, usage_data: Dict) -> List[Dict]:
        """Analyze Azure Files usage for reservation opportunities"""
        files_recommendations = []
        
        for sub_id in self.subscription_ids:
            sub_usage = usage_data.get('subscription_spending', {}).get(sub_id, {})
            
            # Calculate average monthly Azure Files costs
            files_costs = []
            for month_data in sub_usage.values():
                storage_costs = month_data.get('storage_costs', {})
                files_cost = storage_costs.get('Azure Files', 0)
                if files_cost > 0:
                    files_costs.append(files_cost)
            
            if len(files_costs) >= 2:  # Need at least 2 months of data
                avg_monthly_cost = sum(files_costs) / len(files_costs)
                consistency_score = self._calculate_cost_consistency(files_costs)
                
                # Recommend reservation if cost is significant and consistent
                if avg_monthly_cost > 50 and consistency_score > 0.6:
                    # Calculate Azure Files reservation options
                    reservation_options = self._calculate_files_reservation_options(avg_monthly_cost)
                    
                    for option in reservation_options:
                        if option['confidence'] >= 'Medium':
                            files_recommendations.append({
                                'subscription_id': sub_id,
                                'service': 'Azure Files',
                                'reservation_type': option['type'],
                                'tier': option['tier'],
                                'capacity_tb': option['capacity_tb'],
                                'term': option['term'],
                                'monthly_cost_current': avg_monthly_cost,
                                'monthly_cost_reserved': option['reserved_monthly_cost'],
                                'monthly_savings': option['monthly_savings'],
                                'annual_savings': option['annual_savings'],
                                'upfront_cost': option['upfront_cost'],
                                'payback_months': option['payback_months'],
                                'consistency_score': consistency_score,
                                'confidence': option['confidence'],
                                'recommendation_priority': self._calculate_priority(option)
                            })
        
        return files_recommendations
    
    def _calculate_blob_reservation_tiers(self, avg_monthly_cost: float) -> List[Dict]:
        """Calculate Blob Storage reservation options and savings"""
        # Estimated pricing based on typical Azure Blob Storage reserved capacity pricing
        # These would typically come from Azure Pricing APIs
        
        reservation_tiers = []
        
        # Estimate current usage in TB based on cost (rough approximation)
        estimated_tb = avg_monthly_cost / 20  # Approximate $20/TB/month for hot storage
        
        # Standard LRS Hot Storage - 1 Year
        if estimated_tb >= 1:
            capacity_1yr = max(1, round(estimated_tb * 0.8))  # Conservative estimate
            reserved_monthly_1yr = capacity_1yr * 16  # ~20% savings
            monthly_savings_1yr = avg_monthly_cost - reserved_monthly_1yr
            annual_savings_1yr = monthly_savings_1yr * 12
            upfront_1yr = capacity_1yr * 192  # Annual upfront cost
            
            if monthly_savings_1yr > 0:
                reservation_tiers.append({
                    'type': 'Blob Storage Reserved Capacity',
                    'storage_type': 'Hot',
                    'redundancy': 'LRS',
                    'capacity_tb': capacity_1yr,
                    'term': '1 Year',
                    'reserved_monthly_cost': reserved_monthly_1yr,
                    'monthly_savings': monthly_savings_1yr,
                    'annual_savings': annual_savings_1yr,
                    'upfront_cost': upfront_1yr,
                    'payback_months': 12,
                    'savings_percentage': (monthly_savings_1yr / avg_monthly_cost) * 100,
                    'confidence': 'High' if monthly_savings_1yr > avg_monthly_cost * 0.15 else 'Medium'
                })
        
        # Standard LRS Hot Storage - 3 Years
        if estimated_tb >= 2:
            capacity_3yr = max(2, round(estimated_tb * 0.9))
            reserved_monthly_3yr = capacity_3yr * 12  # ~40% savings
            monthly_savings_3yr = avg_monthly_cost - reserved_monthly_3yr
            annual_savings_3yr = monthly_savings_3yr * 12
            upfront_3yr = capacity_3yr * 432  # 3-year upfront cost
            
            if monthly_savings_3yr > 0:
                reservation_tiers.append({
                    'type': 'Blob Storage Reserved Capacity',
                    'storage_type': 'Hot',
                    'redundancy': 'LRS',
                    'capacity_tb': capacity_3yr,
                    'term': '3 Years',
                    'reserved_monthly_cost': reserved_monthly_3yr,
                    'monthly_savings': monthly_savings_3yr,
                    'annual_savings': annual_savings_3yr,
                    'upfront_cost': upfront_3yr,
                    'payback_months': 36,
                    'savings_percentage': (monthly_savings_3yr / avg_monthly_cost) * 100,
                    'confidence': 'High' if monthly_savings_3yr > avg_monthly_cost * 0.25 else 'Medium'
                })
        
        return reservation_tiers
    
    def _calculate_files_reservation_options(self, avg_monthly_cost: float) -> List[Dict]:
        """Calculate Azure Files reservation options"""
        reservation_options = []
        
        # Estimate current usage based on cost
        estimated_tb = avg_monthly_cost / 60  # Approximate $60/TB/month for premium files
        
        # Premium Files - 1 Year
        if estimated_tb >= 0.5:
            capacity_1yr = max(1, round(estimated_tb))
            reserved_monthly_1yr = capacity_1yr * 48  # ~20% savings
            monthly_savings_1yr = avg_monthly_cost - reserved_monthly_1yr
            annual_savings_1yr = monthly_savings_1yr * 12
            upfront_1yr = capacity_1yr * 576  # Annual upfront
            
            if monthly_savings_1yr > 0:
                reservation_options.append({
                    'type': 'Azure Files Reserved Capacity',
                    'tier': 'Premium',
                    'capacity_tb': capacity_1yr,
                    'term': '1 Year',
                    'reserved_monthly_cost': reserved_monthly_1yr,
                    'monthly_savings': monthly_savings_1yr,
                    'annual_savings': annual_savings_1yr,
                    'upfront_cost': upfront_1yr,
                    'payback_months': 12,
                    'savings_percentage': (monthly_savings_1yr / avg_monthly_cost) * 100,
                    'confidence': 'High' if monthly_savings_1yr > avg_monthly_cost * 0.15 else 'Medium'
                })
        
        # Premium Files - 3 Years  
        if estimated_tb >= 1:
            capacity_3yr = max(1, round(estimated_tb))
            reserved_monthly_3yr = capacity_3yr * 36  # ~40% savings
            monthly_savings_3yr = avg_monthly_cost - reserved_monthly_3yr
            annual_savings_3yr = monthly_savings_3yr * 12
            upfront_3yr = capacity_3yr * 1296  # 3-year upfront
            
            if monthly_savings_3yr > 0:
                reservation_options.append({
                    'type': 'Azure Files Reserved Capacity',
                    'tier': 'Premium',
                    'capacity_tb': capacity_3yr,
                    'term': '3 Years',
                    'reserved_monthly_cost': reserved_monthly_3yr,
                    'monthly_savings': monthly_savings_3yr,
                    'annual_savings': annual_savings_3yr,
                    'upfront_cost': upfront_3yr,
                    'payback_months': 36,
                    'savings_percentage': (monthly_savings_3yr / avg_monthly_cost) * 100,
                    'confidence': 'High' if monthly_savings_3yr > avg_monthly_cost * 0.25 else 'Medium'
                })
        
        return reservation_options
    
    def _calculate_cost_consistency(self, costs: List[float]) -> float:
        """
        Calculate consistency score for cost patterns (0-1 scale)
        Higher score means more predictable costs = better for reservations
        """
        if len(costs) < 2:
            return 0
        
        mean_cost = sum(costs) / len(costs)
        if mean_cost == 0:
            return 0
        
        # Calculate coefficient of variation
        variance = sum((cost - mean_cost) ** 2 for cost in costs) / len(costs)
        std_dev = variance ** 0.5
        cv = std_dev / mean_cost
        
        # Convert to consistency score (0-1, where 1 = perfectly consistent)
        consistency = max(0, 1 - cv)
        return min(1, consistency)
    
    def _calculate_priority(self, reservation: Dict) -> str:
        """Calculate recommendation priority based on savings and confidence"""
        monthly_savings = reservation.get('monthly_savings', 0)
        savings_pct = reservation.get('savings_percentage', 0)
        confidence = reservation.get('confidence', 'Low')
        
        if confidence == 'High' and savings_pct > 20 and monthly_savings > 100:
            return 'High'
        elif confidence in ['High', 'Medium'] and savings_pct > 15 and monthly_savings > 50:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_reservation_summary(self, all_recommendations: List[Dict]) -> Dict:
        """Generate summary statistics for all reservation recommendations"""
        if not all_recommendations:
            return {
                'total_recommendations': 0,
                'total_annual_savings': 0,
                'total_upfront_cost': 0,
                'high_priority_count': 0,
                'average_savings_percentage': 0
            }
        
        total_annual_savings = sum(rec.get('annual_savings', 0) for rec in all_recommendations)
        total_upfront_cost = sum(rec.get('upfront_cost', 0) for rec in all_recommendations)
        high_priority_count = sum(1 for rec in all_recommendations if rec.get('recommendation_priority') == 'High')
        
        savings_percentages = [rec.get('savings_percentage', 0) for rec in all_recommendations if rec.get('savings_percentage', 0) > 0]
        avg_savings_pct = sum(savings_percentages) / len(savings_percentages) if savings_percentages else 0
        
        return {
            'total_recommendations': len(all_recommendations),
            'total_annual_savings': round(total_annual_savings, 2),
            'total_upfront_cost': round(total_upfront_cost, 2),
            'net_savings_year_1': round(total_annual_savings - total_upfront_cost, 2),
            'roi_percentage': round(((total_annual_savings - total_upfront_cost) / total_upfront_cost) * 100, 2) if total_upfront_cost > 0 else 0,
            'high_priority_count': high_priority_count,
            'medium_priority_count': sum(1 for rec in all_recommendations if rec.get('recommendation_priority') == 'Medium'),
            'low_priority_count': sum(1 for rec in all_recommendations if rec.get('recommendation_priority') == 'Low'),
            'average_savings_percentage': round(avg_savings_pct, 2)
        }

    def generate_reservation_action_plan(self, recommendations: Dict) -> List[Dict]:
        """Generate prioritized action plan for implementing reservations"""
        action_plan = []
        
        all_recommendations = (recommendations.get('blob_storage_reservations', []) + 
                             recommendations.get('files_reservations', []))
        
        # Sort by priority and savings
        sorted_recs = sorted(all_recommendations, 
                           key=lambda x: (
                               {'High': 3, 'Medium': 2, 'Low': 1}.get(x.get('recommendation_priority', 'Low'), 1),
                               x.get('annual_savings', 0)
                           ), 
                           reverse=True)
        
        for i, rec in enumerate(sorted_recs[:10], 1):  # Top 10 recommendations
            action = {
                'priority_rank': i,
                'action_type': 'Purchase Reservation',
                'service': rec.get('service', 'Unknown'),
                'subscription_id': rec.get('subscription_id', 'Unknown'),
                'reservation_details': f"{rec.get('capacity_tb', 'Unknown')} TB {rec.get('reservation_type', 'Unknown')} - {rec.get('term', 'Unknown')}",
                'investment_required': rec.get('upfront_cost', 0),
                'monthly_savings': rec.get('monthly_savings', 0),
                'annual_savings': rec.get('annual_savings', 0),
                'payback_period': f"{rec.get('payback_months', 0)} months",
                'confidence_level': rec.get('confidence', 'Unknown'),
                'next_steps': [
                    'Review historical usage patterns',
                    'Validate capacity requirements',
                    'Obtain budget approval for upfront cost',
                    f"Purchase {rec.get('reservation_type', 'reservation')} through Azure portal",
                    'Monitor usage against reservation capacity'
                ]
            }
            action_plan.append(action)
        
        return action_plan