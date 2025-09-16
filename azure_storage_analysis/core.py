from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

def get_storage_account_connection_string(storage_client, resource_group_name, account_name):
    # Placeholder: Implement actual logic to retrieve connection string
    # For now, return None to avoid breaking the flow
    return None

def process_containers_concurrently(containers_to_process, max_workers=10):
    # Placeholder: Implement actual concurrent processing logic
    return []

def process_file_shares_concurrently(file_shares_to_process, max_workers=10):
    # Placeholder: Implement actual concurrent processing logic for file shares
    return []

def _generate_enhanced_excel_report(container_results, file_share_results, export_detailed_blobs=False, max_blobs_per_container=None, export_detailed_files=False, max_files_per_share=None):
    # Placeholder: Implement actual Excel report generation
    pass
import fnmatch
from azure.storage.blob import BlobServiceClient

def select_containers_to_process(storage_client, account, auto_mode=False, container_names=None, container_pattern=None, max_containers_per_account=None):
    try:
        resource_group = account.id.split('/')[4]
        conn_string = get_storage_account_connection_string(storage_client, resource_group, account.name)
        if not conn_string:
            logging.error(f"Could not get connection string for account {account.name}")
            return []
        blob_service_client = BlobServiceClient.from_connection_string(conn_string)
        containers = list(blob_service_client.list_containers())
        if not containers:
            logging.info(f"No containers found in account {account.name}")
            return []
        logging.info(f"Found {len(containers)} containers in account {account.name}")
        if auto_mode or container_names or container_pattern:
            selected_containers = []
            if container_names:
                for container_name in container_names:
                    matching_containers = [c for c in containers if c.name.lower() == container_name.lower()]
                    if matching_containers:
                        selected_containers.extend([(c.name, blob_service_client) for c in matching_containers])
                    else:
                        logging.warning(f"Container '{container_name}' not found in account {account.name}")
                if not selected_containers:
                    logging.warning(f"No valid containers found from specified names in account {account.name}. Processing all containers.")
                    selected_containers = [(container.name, blob_service_client) for container in containers]
            elif container_pattern:
                for container in containers:
                    if fnmatch.fnmatch(container.name.lower(), container_pattern.lower()):
                        selected_containers.append((container.name, blob_service_client))
                if not selected_containers:
                    logging.warning(f"No containers matched pattern '{container_pattern}' in account {account.name}. Processing all containers.")
                    selected_containers = [(container.name, blob_service_client) for container in containers]
            else:
                selected_containers = [(container.name, blob_service_client) for container in containers]
            if max_containers_per_account and len(selected_containers) > max_containers_per_account:
                logging.info(f"Limiting to first {max_containers_per_account} containers in account {account.name}")
                selected_containers = selected_containers[:max_containers_per_account]
            container_names_list = [c[0] for c in selected_containers]
            logging.info(f"Auto mode: Processing {len(selected_containers)} containers in account {account.name}: {', '.join(container_names_list[:3])}" + (f" and {len(container_names_list) - 3} more" if len(container_names_list) > 3 else ""))
            return selected_containers
        return [(container.name, blob_service_client) for container in containers]
    except Exception as e:
        logging.error(f"Error selecting containers for account {account.name}: {e}")
        return []

def select_file_shares_to_process(storage_client, account, auto_mode=False, share_names=None, share_pattern=None, max_shares_per_account=None):
    # Placeholder: Implement similar to select_containers_to_process, using ShareServiceClient
    return []
import logging
from azure_storage_analysis.auth import (
    initialize_azure_clients,
    get_all_storage_accounts,
    select_storage_accounts_to_process
)

# Main orchestration function moved from original script
def get_azure_storage_analysis_enhanced(max_workers=10, export_detailed_blobs=False, max_blobs_per_container=None,
                                       analyze_file_shares=True, export_detailed_files=False, max_files_per_share=None,
                                       auto_mode=False, subscription_id=None, account_names=None, account_pattern=None,
                                       container_names=None, container_pattern=None, share_names=None, share_pattern=None,
                                       max_accounts=None, max_containers_per_account=None, max_shares_per_account=None,
                                       analyze_containers=True):
    """
    Analyze Azure Storage accounts including both Blob Storage and Azure Files.
    Returns: bool: True if analysis completed successfully
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Analysis configuration:")
        logger.info(f"  - Analyze containers: {analyze_containers}")
        logger.info(f"  - Analyze file shares: {analyze_file_shares}")
        if not analyze_containers and not analyze_file_shares:
            logger.error("Both container and file share analysis are disabled. Nothing to analyze!")
            return False
        logger.info("Initializing Azure clients...")
        credential, subscription_id, resource_client, storage_client = initialize_azure_clients(
            subscription_id=subscription_id, auto_mode=auto_mode
        )
        logger.info("Discovering storage accounts...")
        storage_accounts = get_all_storage_accounts(storage_client)
        if not storage_accounts:
            logger.error("No storage accounts found in the subscription.")
            return False
        selected_accounts = select_storage_accounts_to_process(
            storage_accounts, 
            auto_mode=auto_mode,
            account_names=account_names,
            account_pattern=account_pattern,
            max_accounts=max_accounts
        )
        if not selected_accounts:
            logger.error("No storage accounts selected for processing.")
            return False
        containers_to_process = []
        file_shares_to_process = []
        for account in selected_accounts:
            logger.info(f"Processing storage account: {account.name}")
            if analyze_containers:
                logger.info(f"Container analysis ENABLED - Selecting containers for storage account: {account.name}")
                try:
                    account_containers = select_containers_to_process(
                        storage_client, 
                        account, 
                        auto_mode=auto_mode,
                        container_names=container_names,
                        container_pattern=container_pattern,
                        max_containers_per_account=max_containers_per_account
                    )
                    for container_name, blob_service_client in account_containers:
                        containers_to_process.append((
                            blob_service_client,
                            container_name,
                            account.name,
                            subscription_id
                        ))
                    logger.info(f"Found {len(account_containers)} containers in account {account.name}")
                except Exception as e:
                    logger.warning(f"Error processing containers for account {account.name}: {e}")
            else:
                logger.info(f"Container analysis DISABLED - Skipping container processing for storage account: {account.name}")
            if analyze_file_shares:
                logger.info(f"File share analysis ENABLED - Selecting file shares for storage account: {account.name}")
                try:
                    account_shares = select_file_shares_to_process(
                        storage_client,
                        account,
                        auto_mode=auto_mode,
                        share_names=share_names,
                        share_pattern=share_pattern,
                        max_shares_per_account=max_shares_per_account
                    )
                    for share_name, share_service_client in account_shares:
                        file_shares_to_process.append((
                            share_service_client,
                            share_name,
                            account.name,
                            subscription_id
                        ))
                    logger.info(f"Found {len(account_shares)} file shares in account {account.name}")
                except Exception as e:
                    logger.warning(f"Error processing file shares for account {account.name}: {e}")
            else:
                logger.info(f"File share analysis DISABLED - Skipping file share processing for storage account: {account.name}")
        if not containers_to_process and not file_shares_to_process:
            logger.error("No containers or file shares selected for processing.")
            if not analyze_containers:
                logger.info("Container analysis was disabled")
            if not analyze_file_shares:
                logger.info("File share analysis was disabled")
            return False
        logger.info(f"Total containers to analyze: {len(containers_to_process)}")
        logger.info(f"Total file shares to analyze: {len(file_shares_to_process)}")
        container_results = []
        if containers_to_process and analyze_containers:
            logger.info("Starting container analysis...")
            container_results = process_containers_concurrently(
                containers_to_process, 
                max_workers=max_workers
            )
            logger.info(f"Successfully analyzed {len(container_results)} containers")
        elif not analyze_containers:
            logger.info("Container analysis disabled - skipping blob storage analysis")
        else:
            logger.info("No containers found to analyze")
        file_share_results = []
        if file_shares_to_process and analyze_file_shares:
            logger.info("Starting file share analysis...")
            file_share_results = process_file_shares_concurrently(
                file_shares_to_process,
                max_workers=max_workers
            )
            logger.info(f"Successfully analyzed {len(file_share_results)} file shares")
        elif not analyze_file_shares:
            logger.info("File share analysis disabled - skipping Azure Files analysis")
        else:
            logger.info("No file shares found to analyze")
        logger.info("Generating Excel report...")
        _generate_enhanced_excel_report(
            container_results,
            file_share_results,
            export_detailed_blobs=export_detailed_blobs,
            max_blobs_per_container=max_blobs_per_container,
            export_detailed_files=export_detailed_files,
            max_files_per_share=max_files_per_share
        )
        logger.info("Azure Storage analysis completed successfully!")
        return True
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        return False
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
# Core analysis logic for Azure Storage Analysis

# ...functions and classes from azure_storage_analysis.py will be moved here...



import sys
import argparse
from azure_storage_analysis import auth, utils, reporting, recommendations

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Azure Storage accounts (Blob Storage and Azure Files)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --auto
  python cli.py --auto --no-file-shares
  python cli.py --auto --no-containers
  python cli.py --auto --account-pattern \"prod-*\"
  python cli.py --auto --export-detailed-blobs --max-blobs-per-container 1000
  python cli.py --auto --share-names myshare1 myshare2
        """
    )
    # General options
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode without prompts")
    parser.add_argument("--max-workers", type=int, default=10, help="Maximum number of concurrent workers")
    # Blob Storage options
    parser.add_argument("--no-containers", action="store_true", help="Skip Blob Storage analysis")
    parser.add_argument("--export-detailed-blobs", action="store_true", help="Export detailed blob lists")
    parser.add_argument("--max-blobs-per-container", type=int, help="Maximum blobs to export per container")
    parser.add_argument("--container-names", nargs="+", help="Specific container names to process")
    parser.add_argument("--container-pattern", help="Pattern to match container names")
    parser.add_argument("--max-containers-per-account", type=int, help="Maximum containers per account")
    # Azure Files options
    parser.add_argument("--no-file-shares", action="store_true", help="Skip Azure Files analysis")
    parser.add_argument("--export-detailed-files", action="store_true", help="Export detailed file lists")
    parser.add_argument("--max-files-per-share", type=int, help="Maximum files to export per share")
    parser.add_argument("--share-names", nargs="+", help="Specific file share names to process")
    parser.add_argument("--share-pattern", help="Pattern to match file share names")
    parser.add_argument("--max-shares-per-account", type=int, help="Maximum file shares per account")
    # Account selection options
    parser.add_argument("--subscription-id", help="Specific subscription ID to use")
    parser.add_argument("--account-names", nargs="+", help="Specific storage account names to process")
    parser.add_argument("--account-pattern", help="Pattern to match storage account names")
    parser.add_argument("--max-accounts", type=int, help="Maximum number of accounts to process")

    args = parser.parse_args()

    print("\n" + "="*80)
    print(" AZURE STORAGE ANALYSIS TOOL v3.0 ".center(80, "="))
    print(" Enhanced with Azure Files Support ".center(80, "="))
    print("="*80)
    print("This tool analyzes Azure Storage accounts including:")
    if not args.no_containers:
        print("  - Blob Storage containers and blobs")
    if not args.no_file_shares:
        print("  - Azure Files shares and files")
    print("  - Cost optimization recommendations")
    print("  - Detailed usage reports")
    print("="*80)

    analyze_containers = not args.no_containers
    analyze_file_shares = not args.no_file_shares

    if not analyze_containers and not analyze_file_shares:
        print("\nError: Both --no-containers and --no-file-shares specified.")
        print("Nothing to analyze!")
        sys.exit(1)

    if args.auto:
        if analyze_containers and analyze_file_shares:
            print("\nAuto mode: Will analyze both Blob Storage and Azure Files")
        elif analyze_containers:
            print("\nAuto mode: Will analyze only Blob Storage (Azure Files disabled)")
        elif analyze_file_shares:
            print("\nAuto mode: Will analyze only Azure Files (Blob Storage disabled)")

    # Run the analysis
    success = get_azure_storage_analysis_enhanced(
        max_workers=args.max_workers,
        export_detailed_blobs=args.export_detailed_blobs,
        max_blobs_per_container=args.max_blobs_per_container,
        analyze_file_shares=analyze_file_shares,
        export_detailed_files=args.export_detailed_files,
        max_files_per_share=args.max_files_per_share,
        auto_mode=args.auto,
        subscription_id=args.subscription_id,
        account_names=args.account_names,
        account_pattern=args.account_pattern,
        analyze_containers=analyze_containers,
        container_names=args.container_names if analyze_containers else None,
        container_pattern=args.container_pattern if analyze_containers else None,
        max_containers_per_account=args.max_containers_per_account if analyze_containers else None,
        share_names=args.share_names if analyze_file_shares else None,
        share_pattern=args.share_pattern if analyze_file_shares else None,
        max_shares_per_account=args.max_shares_per_account if analyze_file_shares else None,
        max_accounts=args.max_accounts
    )

    if success:
        print("\n" + "="*80)
        print(" ANALYSIS COMPLETED SUCCESSFULLY ".center(80, "="))
        print("="*80)
        sys.exit(0)
    else:
        print("\n" + "="*80)
        print(" ANALYSIS FAILED ".center(80, "="))
        print("="*80)
        sys.exit(1)
