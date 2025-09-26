# Azure FinOps CIR Dashboard + Excel Reports

> **Professional Azure Storage Cost Intelligence Reports (CIR) Platform**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Azure](https://img.shields.io/badge/azure-storage-0078d4.svg)](https://azure.microsoft.com/en-us/services/storage/)

**Developed by Prashant Kumar, Cloud & DevOps Engineer @AHEAD**

## 🎯 Key Features

- **🧠 CIR (Cost Intelligence Reports)** - Professional cost tracking and analysis
- **🔄 Real-time Azure Data** - Live storage account monitoring and insights  
- **💡 Cost Optimization** - AI-powered savings recommendations
- **📊 Professional Dashboard** - Interactive charts, metrics, and visualizations
- **📋 Excel CIR Reports** - Comprehensive analysis and executive summaries
- **🌐 Multi/Single Subscription** - Unified support for enterprise and individual accounts

## 🚀 Quick Start (Unified Command)

### One Command for Everything:

**Windows:**
```cmd
start-unified-cir.bat
```

**Python:**
```bash
python start.py
```

This single command will:
1. **Run Analysis** (choose single or multi-subscription)
2. **Generate Excel CIR Reports** automatically 
3. **Launch Professional Dashboard** at http://localhost:5000

### Manual Setup (if needed):

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Azure Authentication

Choose your preferred method:- Highlight opportunities for lifecycle management and automation

```bash- Recommend deletion or consolidation of redundant resources

# Option 1: Azure CLI (Recommended)- Provide insights on data redundancy and geo-replication settings

az login

## 📁 Project Structure

# Option 2: Service Principal (set environment variables)```

export AZURE_CLIENT_ID="your-client-id"Azure-Storage-Analysis/

export AZURE_CLIENT_SECRET="your-client-secret" ├── cli.py                          # Main CLI entry point

export AZURE_TENANT_ID="your-tenant-id"├── requirements.txt                # Python dependencies

```├── README.md                       # Project documentation

├── .gitignore                      # Git exclusion rules

### 3. Run Analysis & Start Dashboard├── azure_storage_analysis/         # Core analysis package

```bash│   ├── __init__.py                 # Package initialization

# Generate fresh Azure analysis data│   ├── auth.py                     # Azure authentication

python show_detailed_data.py│   ├── core.py                     # Main analysis engine

│   ├── recommendations.py          # Cost optimization

# Start the CIR Dashboard│   ├── reporting.py                # Excel report generation

python start.py│   └── utils.py                    # Utility functions

# OR directly: python real_data_dashboard.py└── tests/                          # Test framework

``````



### 4. Access Dashboard## 🚀 Quick Start

- **URL:** http://localhost:5000

- **Features:** CIR tracking, cost intelligence, optimization recommendations### Prerequisites

- Python 3.8 or higher

## 🗂️ Clean Project Structure- Required Python packages (see below)

- Azure CLI (for authentication and subscription management)

```

FinOps/### 🔧 Installation

├── 🎯 real_data_dashboard.py      # Main CIR Dashboard (Port 5000)

├── 🔍 show_detailed_data.py       # Azure Analysis Engine#### 1. Azure CLI Setup

├── 🚀 start.py                    # Simple Startup Script1. Download and install the Azure CLI from the official site:

├── 📦 azure_storage_analysis/     # Core Analysis Modules   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

│   ├── auth.py                   # Azure Authentication2. After installation, open a new terminal and run:

│   ├── core.py                   # Storage Analysis   ```powershell

│   ├── cost_management.py        # Cost Analysis APIs   az login

│   ├── recommendations.py        # Optimization Engine   ```

│   └── unified_reporting.py      # Excel Generation   This will open a browser window for you to authenticate with your Azure account.

├── 📋 requirements.txt            # Python Dependencies3. (Optional) Set your default subscription:

├── 📊 detailed_analysis_*.json    # Generated Analysis Results   ```powershell

└── 📖 README.md                   # This Documentation   az account set --subscription "<your-subscription-name-or-id>"

```   ```

4. Verify your login and subscription:

## 💼 Professional CIR Dashboard Features   ```powershell

   az account show

### Cost Intelligence Reports (CIR)   ```

- **Real-time cost tracking** across all Azure storage accounts

- **Monthly spend analysis** with trend visualization#### 2. Project Setup

- **Budget monitoring** with alerts and projections1. Clone this repository:

- **Regional cost distribution** analysis   ```powershell

   git clone git@github.com:PrashantAHD/Azure-Storage-Analysis.git

### Optimization Engine   cd Azure-Storage-Analysis

- **Automated recommendations** for cost savings   ```

- **Storage tier optimization** suggestions2. (Optional) Create and activate a virtual environment:

- **Lifecycle management** policy recommendations   ```powershell

- **Resource consolidation** opportunities   python -m venv venv

   .\venv\Scripts\activate

### Professional Analytics   ```

- **Interactive charts** with Chart.js integration3. Install required packages:

- **Mobile-responsive design** for on-the-go monitoring   ```powershell

- **Excel report generation** for executive presentations   pip install -r requirements.txt

- **Live data refresh** every 30 seconds   ```



## 🔧 Advanced Usage### 💻 Usage



### Generate Detailed AnalysisRun the analysis tool:

```bash```powershell

# Run comprehensive Azure storage analysispython cli.py --auto

python show_detailed_data.py```

```

This will:For additional options and help:

- Scan all storage accounts in your subscription```powershell

- Analyze containers, blobs, and utilizationpython cli.py --help

- Generate cost optimization recommendations```

- Save results to JSON for dashboard consumption

## 📋 Detailed Command Reference

### Dashboard Features

- **Live Data Integration:** Connects to your Azure subscription### Core Commands

- **CIR Tracking:** Professional cost intelligence reporting| Command | Description | Usage Example |

- **Optimization Score:** Real-time efficiency metrics|---------|-------------|---------------|

- **Budget Alerts:** Proactive cost monitoring| `--auto` | Automatic mode with intelligent prompts | `python cli.py --auto` |

| `--help` | Display comprehensive help information | `python cli.py --help` |

## 📈 Sample CIR Dashboard Output

### Subscription Management

```| Command | Description | Usage Example |

🔍 AZURE FINOPS CIR ANALYSIS|---------|-------------|---------------|

====================================| `--all-subscriptions` | Analyze all accessible subscriptions | `python cli.py --all-subscriptions --auto` |

✅ Subscription: Azure Lab Subscription| `--single-subscription` | Force analysis of current subscription only | `python cli.py --single-subscription --auto` |

📦 Storage Accounts: 3 accounts discovered| `--subscription-ids` | Analyze specific subscription IDs | `python cli.py --subscription-ids sub1 sub2 --auto` |

📊 Regions: East US, West US  

💰 Monthly Cost: $45.67 (within budget)### Output

🎯 CIR Score: 85/100 (Excellent)- Enhanced Excel report: `azure_storage_analysis_enhanced_<date>.xlsx`

💡 Savings Potential: $106.60/month- Multi-sheet Excel report with:

====================================  - **Executive Summary**: High-level metrics and KPIs

```  - **Blob Storage Analysis**: Container-level details and insights

  - **Azure Files Analysis**: File share utilization and metrics

## 🎯 Professional Development  - **Cost Optimization**: Detailed recommendations and savings calculations

  - **Raw Data**: Complete dataset for custom analysis

This project demonstrates enterprise-level Azure FinOps capabilities including:

- **Cloud Cost Management** best practices## Analysis Features

- **Real-time data integration** with Azure APIs

- **Professional dashboard development** with modern web technologies### 🎯 Intelligent Subscription Detection

- **Automated reporting and analysis** for executive decision-making- **Automatic Detection**: When running `python cli.py --auto`, the tool automatically detects available subscriptions

- **Smart Prompting**: Only prompts for subscription selection when multiple subscriptions are available

---- **Single Subscription Fallback**: Automatically uses current subscription when only one is accessible



**Developed by:** Prashant Kumar | Cloud & DevOps Engineer @AHEAD | 2025### 📈 Benefits

1. **Enterprise Ready**: Supports organizations with multiple Azure subscriptions

*Professional Azure FinOps solution with CIR (Cost Intelligence Reports) tracking*2. **User Friendly**: Professional interface with clear instructions
3. **Flexible**: Multiple selection modes for different use cases

## 💰 Cost Optimization Strategies

The tool provides intelligent cost optimization recommendations based on industry best practices and Azure pricing models.

### 🔍 Analysis Categories

#### 1. **Storage Lifecycle Management**
- **Cold Data Detection**: Identifies data not accessed for 30-90+ days
- **Archive Candidates**: Files suitable for Archive tier (>180 days old)
- **Lifecycle Policies**: Automated tier transition recommendations

#### 2. **Storage Tier Optimization**
- **Hot vs Cool Analysis**: Usage pattern analysis for tier recommendations
- **Access Pattern Metrics**: Frequency and timing of data access
- **Cost Impact Projections**: Estimated savings from tier changes

#### 3. **Redundancy Right-sizing**
- **LRS vs GRS Analysis**: Redundancy requirement assessment
- **Regional Considerations**: Multi-region vs single-region strategies
- **Compliance Requirements**: Data residency and backup needs

#### 4. **Capacity Optimization**
- **Empty Container Detection**: Unused containers consuming resources
- **Small File Consolidation**: Optimization for storage transaction costs
- **Duplicate Data Analysis**: Potential deduplication opportunities

### Performance & Scalability
- Configurable multi-threading for large-scale analysis
- Memory-efficient processing for large datasets
- Progress tracking with real-time updates

## Troubleshooting Guide

### Common Issues and Solutions

#### Authentication Problems
**Issue**: `Authentication failed` or `Unable to obtain credentials`
```bash
# Solution 1: Re-authenticate with Azure CLI
az logout
az login

# Solution 2: Check current account
az account show

# Solution 3: Set default subscription
az account set --subscription "your-subscription-id"
```

#### Permission Errors
**Issue**: `Access denied` or `Insufficient permissions`
- **Required Permissions**: `Storage Account Contributor` or `Reader` role
- **Subscription Access**: Ensure account has access to target subscriptions
- **Resource Group Permissions**: Verify read access to storage resource groups

#### Memory Issues
**Issue**: Out of memory errors with large datasets
```bash
# Solution 1: Process single subscription
python cli.py --single-subscription --auto

# Solution 2: Filter by specific accounts
python cli.py --auto --account-names "account1" "account2"

# Solution 3: Reduce concurrent operations
python cli.py --auto --max-workers 3
```

#### Excel Export Problems
**Issue**: Unable to generate Excel reports
```bash
# Install/update required packages
pip install --upgrade openpyxl pandas

# Check disk space
# Ensure sufficient disk space for report generation

# Alternative: Export to CSV only
python cli.py --auto --export-format csv
```

### Debug Mode
Enable detailed logging for troubleshooting:
```bash
# Set debug environment variable
set AZURE_STORAGE_DEBUG=1
python cli.py --auto

# Or use verbose output
python cli.py --auto --verbose
```

## Customization
- Modify or extend modules in `azure_storage_analysis/` to adjust analysis logic, reporting, or add new features.
- Update the CLI (`cli.py`) to support additional options or workflows.

## Support
For questions or suggestions, please open an issue on the GitHub repository.

## Azure Storage Cost Optimization Resources

### Key Strategies & Best Practices
- **Storage Tiering & Lifecycle Management:**
  - Move infrequently accessed data to Cool, Cold, or Archive tiers.
  - Use lifecycle policies to automate tier transitions and deletions.
  - Be aware of early deletion fees for each tier.
- **Reserved Capacity & Discounts:**
  - Commit to 1- or 3-year reserved capacity for predictable workloads to save up to 38% (storage) or 72% (compute).
  - Use Azure Cost Management to simulate and plan reservations.
- **Monitor, Audit, and Clean Up:**
  - Use Azure Advisor and Cost Management for recommendations and alerts.
  - Delete unused resources (disks, snapshots, storage accounts).
  - Right-size provisioned resources regularly.
- **Optimize Data Transfer and Redundancy:**
  - Minimize data egress by co-locating compute and storage.
  - Choose redundancy (LRS, ZRS, GRS, RA-GRS) based on cost and durability needs.
- **Backup and Encryption:**
  - Use incremental backups, set appropriate retention, and move long-term backups to Archive.
  - Use server-side encryption with managed keys for most scenarios.
- **Cost Management Tools:**
  - Use the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) to estimate costs.
  - Consider third-party tools like Ternary, Turbo360, IBM Cloudability for advanced cost visibility.
- **Case Studies:**
  - Companies like Maersk, ASOS, and H&R Block achieved savings by regular audits, training, and using Azure’s built-in cost management features.

### Useful Links
- [Azure Storage Pricing](https://azure.microsoft.com/en-us/pricing/details/storage/)
- [Azure Blob Storage Pricing](https://azure.microsoft.com/en-us/pricing/details/storage/blobs/)
- [Azure Managed Disks Pricing](https://azure.microsoft.com/en-us/pricing/details/managed-disks/)
- [Azure Advisor Cost Recommendations](https://learn.microsoft.com/en-us/azure/advisor/advisor-reference-cost-recommendations)
- [Azure Storage Access Tiers Overview](https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview)
- [Azure Blob Lifecycle Management](https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-policy-access-tiers)
- [Azure Cost Management and Billing](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/overview-cost-management)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [CloudZero: Azure Storage Cost Optimization](https://www.cloudzero.com/blog/azure-storage-cost-optimization/)
- [Intercept: Azure Storage Pricing Guide](https://intercept.cloud/en-gb/blogs/azure-storage-pricing)
- [TechTarget: Azure Storage Pricing Guide](https://www.techtarget.com/searchstorage/tip/A-guide-to-Microsoft-Azure-storage-pricing)
- [N2WS: Azure Storage Cost Factors](https://n2ws.com/blog/microsoft-azure-cloud-services/azure-storage-costs)
- [Ternary: Azure Cost Management Tools](https://ternary.app/blog/azure-cost-management-tools/)
- [Medium: Azure Cost Optimization Stories](https://medium.com/@NickHystax/get-inspired-cost-optimization-stories-of-ms-azure-customers-ddf7ebf97042)

---

## 👨‍💻 About Author

**[Prashant Kumar](https://www.linkedin.com/in/iprashantkr)**

Cloud DevOps Engineer @AHEAD With 4+ Years of Working Experience Specializing in Managing Scalable Platforms Serving Millions of Customers & Engineers for Multiple US & European Clients Involving AWS, Azure & GCP Cloud. Specializing Cloud-Security, DevOps, FinOps, Incidents & Request Management, And Ensuring Site Reliability.

**Certified With:** [AWS Certified DevOps Engineer - Professional](https://www.credly.com/badges/72e67681-2adc-4eff-8f31-e565b7596838/public_url) & [AWS Certified Solutions Architect - Professional](https://www.credly.com/badges/410997f9-2d5d-43bb-9660-4bd38fc928b7/public_url)

[![Email](https://img.shields.io/badge/Email-prashant271227%40gmail.com-red?style=for-the-badge&logo=gmail&logoColor=white)](mailto:prashant271227@gmail.com)
