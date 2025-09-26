# Azure FinOps CIR Dashboard + Excel Reports
## ðŸŽ¯ **Unified Single-Command Solution**

> **Professional Azure Storage Cost Intelligence Reports (CIR) Platform**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Azure](https://img.shields.io/badge/azure-storage-0078d4.svg)](https://azure.microsoft.com/en-us/services/storage/)
[![Architecture](https://img.shields.io/badge/architecture-unified-success.svg)](#)

**Developed by Prashant Kumar, Cloud & DevOps Engineer @AHEAD**

## âœ¨ **Unified Features**

- ðŸŽ¯ **Single Command Solution** - One command for analysis + Excel + dashboard
- ï¿½ **Intelligent Detection** - Auto-detects single vs multi-subscription scenarios
- ï¿½ðŸ§  **CIR (Cost Intelligence Reports)** - Professional cost tracking and analysis
- ðŸ”„ **Real-time Azure Data** - Live storage account monitoring and insights  
- ðŸ’¡ **Cost Optimization** - AI-powered savings recommendations
- ðŸ“Š **Unified Dashboard** - Works seamlessly with single/multi-subscription data
- ðŸ“‹ **Automatic Excel CIR Reports** - 8 comprehensive analysis sheets generated automatically
- ðŸŒ **Enterprise Ready** - Handles both individual and multi-subscription environments

## ðŸš€ **Single Command Quick Start**

### **The Only Command You Need:**

```bash
python start.py
```

**This ONE command automatically:**
1. ðŸ¤– **Detects subscription scope** (single/multi/auto-detect)
2. ðŸ“Š **Runs complete Azure analysis** with real data collection
3. ðŸ“‹ **Generates Excel CIR reports** (8 comprehensive sheets)
4. ðŸŒ **Launches unified dashboard** at http://localhost:5000
5. ðŸ”„ **Handles data flow** seamlessly between all components

### **Subscription Selection Options:**
- **Option 1:** Single Subscription Analysis (detailed)
- **Option 2:** Multi-Subscription Analysis (enterprise view) 
- **Option 3:** Auto-detect (recommended)

## ðŸ“‹ **Prerequisites**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Azure Authentication
Choose your preferred method:

```bash
# Option 1: Azure CLI (Recommended)
az login

# Option 2: Service Principal (set environment variables)
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

## ðŸ—ï¸ **Unified Architecture**

```
Azure-Storage-Analysis/
â”œâ”€â”€ ðŸš€ start.py                         # ðŸŽ¯ UNIFIED LAUNCHER (Main Entry Point)
â”œâ”€â”€ ðŸ” unified_azure_analysis.py        # ðŸ¤– COMPLETE ANALYSIS ENGINE  
â”œâ”€â”€ ðŸ“Š real_data_dashboard.py           # ðŸŒ UNIVERSAL CIR DASHBOARD
â”œâ”€â”€ ðŸ“‹ requirements.txt                 # Python dependencies
â”œâ”€â”€ ðŸ“– README.md                        # Project documentation
â”œâ”€â”€ ðŸš« .gitignore                       # Git exclusion rules
â””â”€â”€ ðŸ“¦ azure_storage_analysis/          # ðŸ”§ CORE FRAMEWORK MODULES
    â”œâ”€â”€ __init__.py                     # Package initialization
    â”œâ”€â”€ auth.py                         # Azure authentication & subscription handling
    â”œâ”€â”€ core.py                         # Storage analysis engine
    â”œâ”€â”€ cost_management.py              # Cost analysis & tracking
    â”œâ”€â”€ reservations.py                 # Reserved instances analysis
    â”œâ”€â”€ savings_plans.py                # Savings plans optimization
    â”œâ”€â”€ enhanced_reporting.py           # Advanced reporting features
    â”œâ”€â”€ unified_reporting.py            # Excel CIR report generation
    â”œâ”€â”€ recommendations.py              # Cost optimization recommendations
    â”œâ”€â”€ reporting.py                    # Base reporting functionality
    â””â”€â”€ utils.py                        # Utility functions
```

### ðŸŽ¯ **Key Architecture Benefits:**
- **Single Entry Point:** `start.py` handles everything
- **Intelligent Engine:** `unified_azure_analysis.py` detects and handles all scenarios
- **Universal Dashboard:** `real_data_dashboard.py` works with single/multi-subscription data
- **No Redundancy:** Eliminated separate scripts and dashboards

## ðŸš€ **Usage Examples**

### Basic Usage (Recommended):
```bash
python start.py
```

### Direct Analysis (Advanced):
```bash
python unified_azure_analysis.py
```

### Direct Dashboard (After Analysis):
```bash
python real_data_dashboard.py
```

## ï¿½ **Dashboard Access**

- **URL:** http://localhost:5000
- **Features:** 
  - Real-time CIR tracking
  - Cost intelligence analytics
  - Optimization recommendations
  - Single/Multi-subscription data visualization
  - Interactive charts and metrics

## ðŸ“‹ **What Gets Generated**

### Excel CIR Reports (8 Comprehensive Sheets):
1. **Executive Summary** - High-level cost intelligence overview
2. **Summary** - Detailed subscription and storage account breakdown  
3. **Blob Storage Analysis** - Container-level analysis with size metrics
4. **Azure Files Analysis** - File share usage and optimization
5. **Storage Analysis** - Combined storage overview and insights
6. **Recommendations** - Cost optimization and management suggestions
7. **Cost Optimization** - Advanced financial recommendations
8. **Detailed Data** - Raw data for further analysis

### JSON Analysis Files:
- `detailed_analysis_results_YYYYMMDD_HHMMSS.json` (Single subscription)
- `multi_subscription_analysis_YYYYMMDD_HHMMSS.json` (Multi-subscription)

### Live Dashboard:
- Real-time web interface at http://localhost:5000
- Interactive charts powered by Chart.js
- Bootstrap-styled professional interface

## ðŸŽ¯ **Benefits of Unified Architecture**

### ðŸš€ **Simplified Workflow:**
- **One Command:** `python start.py` handles everything
- **No Manual Steps:** Automatic analysis â†’ Excel generation â†’ dashboard startup
- **Intelligent Detection:** Auto-detects single vs multi-subscription environments
- **Clean Interface:** No need to remember multiple script names

### ðŸ”§ **Technical Advantages:**
- **Reduced Maintenance:** Single codebase instead of separate scripts
- **Better Error Handling:** Unified error management and user feedback
- **Consistent Data Flow:** Seamless integration between analysis and dashboard
- **Future-Proof:** Easy to extend and modify

## ðŸ” **Troubleshooting**

### Common Issues:
```bash
# Authentication problems
az login
az account set --subscription "your-subscription-id"

# Permission issues (ensure you have Storage Account Reader role)
az role assignment list --assignee "your-email@domain.com"

# Module import errors
pip install -r requirements.txt
```

## ðŸ“ž **Support & Contributing**

- **Issues:** [GitHub Issues](https://github.com/PrashantAHD/Azure-Storage-Analysis/issues)
- **Feature Requests:** Open an issue with enhancement label
- **Contributions:** Pull requests welcome!

---

## ðŸ‘¨â€ðŸ’» **About Author**

**[Prashant Kumar](https://www.linkedin.com/in/iprashantkr)**

Cloud DevOps Engineer @AHEAD With 4+ Years of Experience Specializing in Managing Scalable Platforms. Expert in AWS, Azure & GCP Cloud, with focus on Cloud-Security, DevOps, FinOps, and Site Reliability.

**Certifications:** 
- [AWS Certified DevOps Engineer - Professional](https://www.credly.com/badges/72e67681-2adc-4eff-8f31-e565b7596838/public_url)
- [AWS Certified Solutions Architect - Professional](https://www.credly.com/badges/410997f9-2d5d-43bb-9660-4bd38fc928b7/public_url)

[![Email](https://img.shields.io/badge/Email-prashant271227%40gmail.com-red?style=for-the-badge&logo=gmail&logoColor=white)](mailto:prashant271227@gmail.com)

---

## ðŸ“„ **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**ðŸŽ¯
** Azure FinOps CIR Dashboard - Your Complete Single-Command Solution for Azure Storage Cost Intelligence** 
