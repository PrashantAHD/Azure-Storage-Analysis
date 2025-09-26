#!/usr/bin/env python3
"""
Multi-Subscription CIR Dashboard
Enhanced version that can display data from multiple Azure subscriptions
"""

from flask import Flask, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

def load_multi_subscription_data():
    """Load multi-subscription Azure analysis data"""
    try:
        # Try to load multi-subscription data first
        json_files = [f for f in os.listdir('.') if f.startswith('multi_subscription_analysis_') and f.endswith('.json')]
        if json_files:
            latest_file = max(json_files, key=os.path.getctime)
            print(f"Loading multi-subscription data from: {latest_file}")
            
            with open(latest_file, 'r') as f:
                data = json.load(f)
            
            return data, True  # True indicates multi-subscription data
        
        # Fallback to single subscription data
        json_files = [f for f in os.listdir('.') if f.startswith('detailed_analysis_results_') and f.endswith('.json')]
        if json_files:
            latest_file = max(json_files, key=os.path.getctime)
            print(f"Loading single-subscription data from: {latest_file}")
            
            with open(latest_file, 'r') as f:
                data = json.load(f)
            
            return data, False  # False indicates single-subscription data
        
        return None, False
        
    except Exception as e:
        print(f"Error loading analysis data: {e}")
        return None, False

MULTI_SUBSCRIPTION_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Subscription Azure FinOps CIR Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { 
            background-color: #f8f9fa; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .metric-card { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            border-radius: 15px; 
            padding: 25px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        .subscription-card {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 25px;
        }
        .multi-sub-header {
            background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
        }
        .chart-container { 
            height: 300px; 
            position: relative;
            padding: 10px;
        }
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .subscription-badge {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 5px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            margin: 2px;
            display: inline-block;
        }
    </style>
</head>
<body>
    
    <!-- MULTI-SUBSCRIPTION HEADER -->
    <div class="container-fluid" style="padding: 15px; max-width: 1400px; margin: 0 auto;">
        <div class="row">
            <div class="col-12">
                <div class="multi-sub-header">
                    <h1 class="mb-3" style="font-weight: 700; font-size: 3rem;">
                        <i class="fas fa-cloud-upload-alt me-3"></i>
                        Multi-Subscription Azure FinOps CIR Dashboard
                    </h1>
                    <p class="lead mb-3" style="font-size: 1.2rem;">
                        <i class="fas fa-layer-group me-2"></i>
                        Cross-Subscription Cost Intelligence & Resource Management Platform
                    </p>
                    
                    <!-- MULTI-SUBSCRIPTION STATUS -->
                    {% if is_multi_subscription %}
                    <div class="alert alert-light d-inline-block" style="background: rgba(255,255,255,0.9); color: #333;">
                        <i class="fas fa-check-circle text-success me-2"></i>
                        <strong>MULTI-SUBSCRIPTION MODE:</strong> 
                        {{ subscription_count }} Azure Subscriptions | 
                        {{ total_accounts }} Total Storage Accounts | 
                        {{ total_regions }} Regions | 
                        Last Updated: {{ formatted_date }}
                    </div>
                    {% else %}
                    <div class="alert alert-warning d-inline-block">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>SINGLE SUBSCRIPTION MODE:</strong> 
                        1 Azure Subscription | 
                        {{ account_count }} Storage Accounts | 
                        Run multi_subscription_analysis.py for cross-subscription insights
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>

        {% if is_multi_subscription %}
        <!-- MULTI-SUBSCRIPTION METRICS -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="text-center">
                        <i class="fas fa-layer-group fa-3x mb-3"></i>
                        <h3>{{ subscription_count }}</h3>
                        <p>Azure Subscriptions</p>
                        <small>Cross-subscription analysis</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="text-center">
                        <i class="fas fa-database fa-3x mb-3"></i>
                        <h3>{{ total_accounts }}</h3>
                        <p>Total Storage Accounts</p>
                        <small>Across all subscriptions</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="text-center">
                        <i class="fas fa-dollar-sign fa-3x mb-3"></i>
                        <h3>${{ "%.2f"|format(total_cost) }}</h3>
                        <p>Total 90-Day Cost</p>
                        <small>All subscriptions combined</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="text-center">
                        <i class="fas fa-globe fa-3x mb-3"></i>
                        <h3>{{ total_regions }}</h3>
                        <p>Azure Regions</p>
                        <small>Geographic distribution</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- SUBSCRIPTION BREAKDOWN -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #17a2b8 0%, #6610f2 100%); color: white;">
                        <h5 class="mb-0">
                            <i class="fas fa-chart-bar me-2"></i>Subscription Analysis Breakdown
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {% for sub_id, sub_data in subscriptions.items() %}
                            <div class="col-md-6 col-lg-4 mb-3">
                                <div class="subscription-card">
                                    <h6><i class="fas fa-cloud me-2"></i>{{ sub_id[:12] }}...</h6>
                                    <div class="row text-center">
                                        <div class="col-6">
                                            <h4>{{ sub_data.account_count }}</h4>
                                            <small>Storage Accounts</small>
                                        </div>
                                        <div class="col-6">
                                            <h4>${{ "%.0f"|format(sub_data.cost_90_days) }}</h4>
                                            <small>90-Day Cost</small>
                                        </div>
                                    </div>
                                    <div class="mt-2">
                                        <strong>Regions:</strong><br>
                                        {% for region in sub_data.regions %}
                                        <span class="subscription-badge">{{ region }}</span>
                                        {% endfor %}
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- MULTI-SUBSCRIPTION RECOMMENDATIONS -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); color: white;">
                        <h5 class="mb-0">
                            <i class="fas fa-lightbulb me-2"></i>
                            Multi-Subscription CIR Optimization Recommendations
                        </h5>
                    </div>
                    <div class="card-body">
                        {% for rec in recommendations %}
                        <div class="p-3 border-start border-4 {% if rec.priority == 'High' %}border-danger{% elif rec.priority == 'Medium' %}border-warning{% else %}border-info{% endif %} bg-light mb-3">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="{% if rec.priority == 'High' %}text-danger{% elif rec.priority == 'Medium' %}text-warning{% else %}text-info{% endif %} mb-1">
                                        <i class="fas fa-layer-group me-2"></i>{{ rec.title }} (Multi-Sub Analysis)
                                    </h6>
                                    <p class="mb-1">{{ rec.description }}</p>
                                    <small class="text-muted">Type: {{ rec.type }}</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge {% if rec.priority == 'High' %}bg-danger{% elif rec.priority == 'Medium' %}bg-warning{% else %}bg-info{% endif %}">
                                        {{ rec.priority }} Priority
                                    </span>
                                    <br><small class="text-muted">{{ rec.potential_savings }}</small>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        {% else %}
        <!-- SINGLE SUBSCRIPTION FALLBACK -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="alert alert-info">
                    <h5><i class="fas fa-info-circle me-2"></i>Single Subscription Mode</h5>
                    <p class="mb-2">Currently displaying data from a single Azure subscription.</p>
                    <p class="mb-0">
                        <strong>To enable multi-subscription analysis:</strong><br>
                        1. Run: <code>python show_multi_subscription_data.py</code><br>
                        2. Refresh this dashboard to see cross-subscription insights
                    </p>
                </div>
            </div>
        </div>
        {% endif %}

        <!-- CIR CHARTS SECTION (works for both modes) -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white;">
                        <h5 class="mb-0">
                            <i class="fas fa-chart-pie me-2"></i>CIR Cost Distribution
                        </h5>
                    </div>
                    <div class="card-body chart-container">
                        <canvas id="costDistributionChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #6610f2 0%, #e83e8c 100%); color: white;">
                        <h5 class="mb-0">
                            <i class="fas fa-chart-bar me-2"></i>CIR Account Distribution
                        </h5>
                    </div>
                    <div class="card-body chart-container">
                        <canvas id="accountDistributionChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer class="mt-5 py-3" style="background: rgba(0,0,0,0.05); border-top: 1px solid rgba(0,0,0,0.1);">
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 text-center">
                    <small class="text-muted" style="font-size: 0.85rem; opacity: 0.7;">
                        <i class="fas fa-code me-1"></i>
                        Multi-Subscription Azure FinOps CIR Dashboard | 
                        Developed by <strong>Prashant Kumar</strong> | 
                        <i class="fas fa-user-tie me-1"></i>
                        Cloud & DevOps Engineer @AHEAD |
                        <i class="fas fa-calendar me-1"></i>
                        2025
                    </small>
                </div>
            </div>
        </div>
    </footer>

    <!-- CHARTS JAVASCRIPT -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            {% if is_multi_subscription %}
            // Multi-subscription charts
            
            // Cost Distribution by Subscription
            const costCtx = document.getElementById('costDistributionChart').getContext('2d');
            new Chart(costCtx, {
                type: 'pie',
                data: {
                    labels: [{% for sub_id, sub_data in subscriptions.items() %}'{{ sub_id[:8] }}...'{% if not loop.last %},{% endif %}{% endfor %}],
                    datasets: [{
                        data: [{% for sub_id, sub_data in subscriptions.items() %}{{ sub_data.cost_90_days }}{% if not loop.last %},{% endif %}{% endfor %}],
                        backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#43e97b'],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.label + ': $' + context.parsed.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });

            // Account Distribution by Subscription
            const accountCtx = document.getElementById('accountDistributionChart').getContext('2d');
            new Chart(accountCtx, {
                type: 'bar',
                data: {
                    labels: [{% for sub_id, sub_data in subscriptions.items() %}'{{ sub_id[:8] }}...'{% if not loop.last %},{% endif %}{% endfor %}],
                    datasets: [{
                        label: 'Storage Accounts',
                        data: [{% for sub_id, sub_data in subscriptions.items() %}{{ sub_data.account_count }}{% if not loop.last %},{% endif %}{% endfor %}],
                        backgroundColor: 'rgba(54, 162, 235, 0.8)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
            {% else %}
            // Single subscription mode - placeholder charts
            const costCtx = document.getElementById('costDistributionChart').getContext('2d');
            new Chart(costCtx, {
                type: 'pie',
                data: {
                    labels: ['Storage Accounts', 'Blob Storage', 'File Storage'],
                    datasets: [{
                        data: [45, 35, 20],
                        backgroundColor: ['#667eea', '#764ba2', '#f093fb']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom' }}
                }
            });

            const accountCtx = document.getElementById('accountDistributionChart').getContext('2d');
            new Chart(accountCtx, {
                type: 'bar',
                data: {
                    labels: ['East US', 'West US'],
                    datasets: [{
                        label: 'Storage Accounts',
                        data: [{{ account_count or 2 }}, 1],
                        backgroundColor: 'rgba(54, 162, 235, 0.8)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true }}
                }
            });
            {% endif %}
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    # Load analysis data (multi-subscription or single)
    data, is_multi_subscription = load_multi_subscription_data()
    
    if data and is_multi_subscription:
        # Multi-subscription data processing
        subscriptions = data.get('subscriptions', {})
        total_accounts = data.get('total_storage_accounts', 0)
        total_cost = data.get('total_cost', 0)
        recommendations = data.get('aggregated_recommendations', [])
        analysis_date = data.get('analysis_date', '')
        
        # Calculate metrics
        subscription_count = len(subscriptions)
        all_regions = set()
        for sub_data in subscriptions.values():
            all_regions.update(sub_data.get('regions', []))
        total_regions = len(all_regions)
        
        # Format date
        try:
            parsed_date = datetime.fromisoformat(analysis_date.replace('Z', '+00:00'))
            formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M')
        except:
            formatted_date = analysis_date[:19] if analysis_date else 'Unknown'
        
        return render_template_string(MULTI_SUBSCRIPTION_DASHBOARD_TEMPLATE,
            is_multi_subscription=True,
            subscriptions=subscriptions,
            subscription_count=subscription_count,
            total_accounts=total_accounts,
            total_cost=total_cost,
            total_regions=total_regions,
            recommendations=recommendations,
            formatted_date=formatted_date
        )
    
    elif data and not is_multi_subscription:
        # Single subscription fallback
        account_count = len(data.get('storage_accounts', []))
        
        return render_template_string(MULTI_SUBSCRIPTION_DASHBOARD_TEMPLATE,
            is_multi_subscription=False,
            account_count=account_count,
            recommendations=data.get('recommendations', [])
        )
    
    else:
        # No data available
        return render_template_string(MULTI_SUBSCRIPTION_DASHBOARD_TEMPLATE,
            is_multi_subscription=False,
            account_count=0,
            recommendations=[]
        )

if __name__ == '__main__':
    print("🚀 Multi-Subscription Azure FinOps CIR Dashboard")
    print("👨‍💻 Developed by: Prashant Kumar, Cloud & DevOps Engineer @AHEAD")
    print("📊 URL: http://localhost:5001")
    print("🔍 Multi-subscription support enabled")
    
    app.run(host='127.0.0.1', port=5001, debug=False)