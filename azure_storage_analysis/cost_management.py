# Azure Cost Management and Historical Spending Analysis

import logging
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.mgmt.costmanagement import CostManagementClient
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
import json

class AzureCostAnalyzer:
    """Comprehensive Azure cost analysis including historical spending and recommendations"""
    
    def __init__(self, credential, subscription_ids):
        self.credential = credential
        self.subscription_ids = subscription_ids if isinstance(subscription_ids, list) else [subscription_ids]
        self.logger = logging.getLogger(__name__)
        
        # Initialize clients for each subscription
        self.consumption_clients = {}
        self.cost_clients = {}
        
        for sub_id in self.subscription_ids:
            try:
                self.consumption_clients[sub_id] = ConsumptionManagementClient(credential, sub_id)
                self.cost_clients[sub_id] = CostManagementClient(credential)
                self.logger.info(f"Initialized cost management clients for subscription {sub_id}")
            except Exception as e:
                self.logger.error(f"Failed to initialize clients for subscription {sub_id}: {e}")
    
    def get_monthly_storage_costs(self):
        """Get storage costs for the last 3 months with detailed analysis"""
        self.logger.info("Analyzing monthly storage costs...")
        
        # Calculate date ranges for analysis
        today = datetime.now()
        
        # Current analysis: July to August (since it's September now)
        current_end = datetime(today.year, 8, 31)  # End of August
        current_start = datetime(today.year, 7, 1)  # Start of July
        
        # Previous analysis: June to July
        previous_end = datetime(today.year, 7, 31)  # End of July
        previous_start = datetime(today.year, 6, 1)  # Start of June
        
        # Get baseline: May to June
        baseline_end = datetime(today.year, 6, 30)  # End of June
        baseline_start = datetime(today.year, 5, 1)  # Start of May
        
        all_costs = []
        
        for sub_id in self.subscription_ids:
            try:
                # Get costs for each period
                current_costs = self._get_costs_for_period(sub_id, current_start, current_end, "July-August")
                previous_costs = self._get_costs_for_period(sub_id, previous_start, previous_end, "June-July") 
                baseline_costs = self._get_costs_for_period(sub_id, baseline_start, baseline_end, "May-June")
                
                subscription_analysis = {
                    'subscription_id': sub_id,
                    'current_period': current_costs,
                    'previous_period': previous_costs,
                    'baseline_period': baseline_costs,
                    'analysis': self._analyze_cost_changes(current_costs, previous_costs, baseline_costs)
                }
                
                all_costs.append(subscription_analysis)
                
            except Exception as e:
                self.logger.error(f"Error getting costs for subscription {sub_id}: {e}")
                
        return all_costs
    
    def _get_costs_for_period(self, subscription_id, start_date, end_date, period_name):
        """Get detailed cost breakdown for a specific period"""
        try:
            scope = f"/subscriptions/{subscription_id}"
            
            # Query parameters for cost analysis
            query_body = {
                "type": "ActualCost",
                "timeframe": "Custom",
                "timePeriod": {
                    "from": start_date.strftime("%Y-%m-%dT00:00:00Z"),
                    "to": end_date.strftime("%Y-%m-%dT23:59:59Z")
                },
                "dataset": {
                    "granularity": "Monthly",
                    "aggregation": {
                        "totalCost": {
                            "name": "Cost",
                            "function": "Sum"
                        }
                    },
                    "grouping": [
                        {
                            "type": "Dimension",
                            "name": "ServiceName"
                        },
                        {
                            "type": "Dimension", 
                            "name": "ResourceType"
                        }
                    ],
                    "filter": {
                        "dimensions": {
                            "name": "ServiceName",
                            "operator": "In",
                            "values": ["Storage", "Azure Storage", "Blob Storage", "Files"]
                        }
                    }
                }
            }
            
            # Get cost data from Azure Cost Management API
            cost_client = self.cost_clients[subscription_id]
            result = cost_client.query.usage(scope=scope, parameters=query_body)
            
            # Parse results
            total_cost = 0
            service_breakdown = {}
            
            if hasattr(result, 'rows') and result.rows:
                for row in result.rows:
                    cost = float(row[0]) if row[0] else 0
                    service_name = row[1] if len(row) > 1 else "Unknown"
                    resource_type = row[2] if len(row) > 2 else "Unknown"
                    
                    total_cost += cost
                    
                    if service_name not in service_breakdown:
                        service_breakdown[service_name] = {
                            'total_cost': 0,
                            'resources': {}
                        }
                    
                    service_breakdown[service_name]['total_cost'] += cost
                    service_breakdown[service_name]['resources'][resource_type] = cost
            
            return {
                'period': period_name,
                'start_date': start_date,
                'end_date': end_date,
                'total_cost': total_cost,
                'service_breakdown': service_breakdown,
                'cost_per_day': total_cost / (end_date - start_date).days if total_cost > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error querying costs for {period_name}: {e}")
            return {
                'period': period_name,
                'start_date': start_date,
                'end_date': end_date,
                'total_cost': 0,
                'service_breakdown': {},
                'cost_per_day': 0,
                'error': str(e)
            }
    
    def _analyze_cost_changes(self, current, previous, baseline):
        """Analyze cost changes and identify reasons for variations"""
        analysis = {
            'trends': {},
            'change_drivers': [],
            'recommendations': []
        }
        
        # Calculate percentage changes
        current_cost = current.get('total_cost', 0)
        previous_cost = previous.get('total_cost', 0) 
        baseline_cost = baseline.get('total_cost', 0)
        
        # Current vs Previous change
        if previous_cost > 0:
            current_vs_previous_change = ((current_cost - previous_cost) / previous_cost) * 100
        else:
            current_vs_previous_change = 0
            
        # Previous vs Baseline change  
        if baseline_cost > 0:
            previous_vs_baseline_change = ((previous_cost - baseline_cost) / baseline_cost) * 100
        else:
            previous_vs_baseline_change = 0
        
        analysis['trends'] = {
            'current_total': current_cost,
            'previous_total': previous_cost,
            'baseline_total': baseline_cost,
            'current_vs_previous_change_pct': current_vs_previous_change,
            'previous_vs_baseline_change_pct': previous_vs_baseline_change,
            'current_vs_previous_change_amount': current_cost - previous_cost,
            'previous_vs_baseline_change_amount': previous_cost - baseline_cost
        }
        
        # Identify change drivers
        current_services = current.get('service_breakdown', {})
        previous_services = previous.get('service_breakdown', {})
        
        for service_name, service_data in current_services.items():
            prev_service_cost = previous_services.get(service_name, {}).get('total_cost', 0)
            curr_service_cost = service_data.get('total_cost', 0)
            
            if prev_service_cost > 0:
                service_change_pct = ((curr_service_cost - prev_service_cost) / prev_service_cost) * 100
                if abs(service_change_pct) > 10:  # Significant change threshold
                    analysis['change_drivers'].append({
                        'service': service_name,
                        'change_amount': curr_service_cost - prev_service_cost,
                        'change_percentage': service_change_pct,
                        'impact': 'increase' if service_change_pct > 0 else 'decrease'
                    })
        
        # Generate recommendations based on analysis
        if current_vs_previous_change > 20:
            analysis['recommendations'].append({
                'type': 'Cost Alert',
                'priority': 'High',
                'message': f'Storage costs increased by {current_vs_previous_change:.1f}% from previous period',
                'action': 'Review storage usage patterns and implement cost controls'
            })
        elif current_vs_previous_change > 10:
            analysis['recommendations'].append({
                'type': 'Cost Warning',
                'priority': 'Medium', 
                'message': f'Storage costs increased by {current_vs_previous_change:.1f}% from previous period',
                'action': 'Monitor usage trends and consider optimization'
            })
        
        if current_cost > 1000:  # High spend threshold
            analysis['recommendations'].append({
                'type': 'High Spend Alert',
                'priority': 'High',
                'message': f'High storage costs detected: ${current_cost:,.2f}',
                'action': 'Implement Reserved Instances or Savings Plans for cost reduction'
            })
        
        return analysis
    
    def get_vm_usage_patterns(self):
        """Analyze VM usage patterns for Reserved Instance recommendations"""
        self.logger.info("Analyzing VM usage patterns for Reserved Instance recommendations...")
        
        vm_recommendations = []
        
        for sub_id in self.subscription_ids:
            try:
                # Get VM usage data for the last 30 days
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
                
                scope = f"/subscriptions/{sub_id}"
                
                # Query for compute usage
                query_body = {
                    "type": "Usage",
                    "timeframe": "Custom",
                    "timePeriod": {
                        "from": start_date.strftime("%Y-%m-%dT00:00:00Z"),
                        "to": end_date.strftime("%Y-%m-%dT23:59:59Z")
                    },
                    "dataset": {
                        "granularity": "Daily",
                        "aggregation": {
                            "totalCost": {
                                "name": "Cost", 
                                "function": "Sum"
                            }
                        },
                        "grouping": [
                            {
                                "type": "Dimension",
                                "name": "ResourceId"
                            },
                            {
                                "type": "Dimension",
                                "name": "MeterName"
                            }
                        ],
                        "filter": {
                            "dimensions": {
                                "name": "ServiceName",
                                "operator": "In", 
                                "values": ["Virtual Machines", "Compute"]
                            }
                        }
                    }
                }
                
                cost_client = self.cost_clients[sub_id]
                result = cost_client.query.usage(scope=scope, parameters=query_body)
                
                # Analyze VM consistency for RI recommendations
                vm_usage = {}
                
                if hasattr(result, 'rows') and result.rows:
                    for row in result.rows:
                        resource_id = row[1] if len(row) > 1 else "Unknown"
                        meter_name = row[2] if len(row) > 2 else "Unknown"
                        cost = float(row[0]) if row[0] else 0
                        
                        if resource_id not in vm_usage:
                            vm_usage[resource_id] = {
                                'total_cost': 0,
                                'daily_costs': [],
                                'meter_name': meter_name
                            }
                        
                        vm_usage[resource_id]['total_cost'] += cost
                        vm_usage[resource_id]['daily_costs'].append(cost)
                
                # Generate RI recommendations
                for resource_id, usage_data in vm_usage.items():
                    if usage_data['total_cost'] > 100:  # Minimum threshold
                        consistency = self._calculate_usage_consistency(usage_data['daily_costs'])
                        
                        if consistency > 0.7:  # 70% consistency threshold
                            monthly_cost = usage_data['total_cost'] * (30/30)  # Normalize to monthly
                            ri_savings_1yr = monthly_cost * 0.4 * 12  # ~40% savings
                            ri_savings_3yr = monthly_cost * 0.6 * 36  # ~60% savings
                            
                            vm_recommendations.append({
                                'subscription_id': sub_id,
                                'resource_id': resource_id,
                                'meter_name': usage_data['meter_name'],
                                'monthly_cost': monthly_cost,
                                'consistency_score': consistency,
                                'ri_1yr_savings': ri_savings_1yr,
                                'ri_3yr_savings': ri_savings_3yr,
                                'recommendation': '3-year RI' if consistency > 0.85 else '1-year RI'
                            })
                
            except Exception as e:
                self.logger.error(f"Error analyzing VM patterns for subscription {sub_id}: {e}")
        
        return vm_recommendations
    
    def _calculate_usage_consistency(self, daily_costs):
        """Calculate consistency score for usage patterns (0-1 scale)"""
        if len(daily_costs) < 7:  # Need at least a week of data
            return 0
        
        # Calculate coefficient of variation (lower = more consistent)
        if len(daily_costs) > 0:
            mean_cost = sum(daily_costs) / len(daily_costs)
            if mean_cost > 0:
                variance = sum((x - mean_cost) ** 2 for x in daily_costs) / len(daily_costs)
                std_dev = variance ** 0.5
                cv = std_dev / mean_cost
                
                # Convert CV to consistency score (inverse relationship)
                consistency = max(0, 1 - cv)
                return min(1, consistency)
        
        return 0
    
    def get_savings_plan_recommendations(self):
        """Analyze and recommend Azure Savings Plans"""
        self.logger.info("Analyzing Savings Plan opportunities...")
        
        savings_recommendations = []
        
        for sub_id in self.subscription_ids:
            try:
                # Get compute spending for last 3 months
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)
                
                scope = f"/subscriptions/{sub_id}"
                
                query_body = {
                    "type": "ActualCost",
                    "timeframe": "Custom", 
                    "timePeriod": {
                        "from": start_date.strftime("%Y-%m-%dT00:00:00Z"),
                        "to": end_date.strftime("%Y-%m-%dT23:59:59Z")
                    },
                    "dataset": {
                        "granularity": "Monthly",
                        "aggregation": {
                            "totalCost": {
                                "name": "Cost",
                                "function": "Sum"
                            }
                        },
                        "grouping": [
                            {
                                "type": "Dimension",
                                "name": "ServiceName"
                            }
                        ],
                        "filter": {
                            "dimensions": {
                                "name": "ServiceName",
                                "operator": "In",
                                "values": ["Virtual Machines", "Compute", "Container Instances", "Functions"]
                            }
                        }
                    }
                }
                
                cost_client = self.cost_clients[sub_id]
                result = cost_client.query.usage(scope=scope, parameters=query_body)
                
                total_compute_spend = 0
                service_spend = {}
                
                if hasattr(result, 'rows') and result.rows:
                    for row in result.rows:
                        cost = float(row[0]) if row[0] else 0
                        service = row[1] if len(row) > 1 else "Unknown"
                        
                        total_compute_spend += cost
                        service_spend[service] = service_spend.get(service, 0) + cost
                
                # Calculate savings plan recommendations
                monthly_avg = total_compute_spend / 3  # 3 months average
                
                if monthly_avg > 500:  # Minimum threshold for savings plans
                    # Compute Savings Plan (covers VMs, Container Instances, Functions)
                    compute_eligible_spend = sum(
                        service_spend.get(service, 0) 
                        for service in ["Virtual Machines", "Container Instances", "Functions"]
                    ) / 3
                    
                    if compute_eligible_spend > 300:
                        compute_savings_1yr = compute_eligible_spend * 0.17 * 12  # ~17% savings
                        compute_savings_3yr = compute_eligible_spend * 0.28 * 36  # ~28% savings
                        
                        savings_recommendations.append({
                            'subscription_id': sub_id,
                            'plan_type': 'Compute Savings Plan',
                            'monthly_eligible_spend': compute_eligible_spend,
                            'recommended_hourly_commitment': compute_eligible_spend / 30 / 24,
                            'savings_1yr': compute_savings_1yr,
                            'savings_3yr': compute_savings_3yr,
                            'recommendation': '3-year plan' if compute_eligible_spend > 1000 else '1-year plan'
                        })
                    
                    # Azure Savings Plan (broader coverage)
                    if monthly_avg > 1000:
                        azure_savings_1yr = monthly_avg * 0.11 * 12  # ~11% savings
                        azure_savings_3yr = monthly_avg * 0.17 * 36  # ~17% savings
                        
                        savings_recommendations.append({
                            'subscription_id': sub_id,
                            'plan_type': 'Azure Savings Plan', 
                            'monthly_eligible_spend': monthly_avg,
                            'recommended_hourly_commitment': monthly_avg / 30 / 24,
                            'savings_1yr': azure_savings_1yr,
                            'savings_3yr': azure_savings_3yr,
                            'recommendation': '3-year plan' if monthly_avg > 2000 else '1-year plan'
                        })
                
            except Exception as e:
                self.logger.error(f"Error analyzing savings plans for subscription {sub_id}: {e}")
        
        return savings_recommendations