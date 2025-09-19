import fnmatch
import sys
import json
import subprocess
import logging
from azure.identity import AzureCliCredential, DefaultAzureCredential, InteractiveBrowserCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient

def get_all_subscriptions(credential):
    """Get all accessible subscriptions"""
    logger = logging.getLogger(__name__)
    try:
        subscription_client = SubscriptionClient(credential)
        subscriptions = list(subscription_client.subscriptions.list())
        logger.info(f"Found {len(subscriptions)} accessible subscriptions")
        return subscriptions
    except Exception as e:
        logger.error(f"Error listing subscriptions: {e}")
        return []

def get_storage_accounts_from_subscription(credential, subscription_id):
    """Get all storage accounts from a specific subscription"""
    logger = logging.getLogger(__name__)
    try:
        storage_client = StorageManagementClient(credential, subscription_id)
        storage_accounts = list(storage_client.storage_accounts.list())
        logger.info(f"Found {len(storage_accounts)} storage accounts in subscription {subscription_id}")
        
        # Add subscription info to each account
        for account in storage_accounts:
            account.subscription_id = subscription_id
            
        return storage_accounts
    except Exception as e:
        logger.error(f"Error listing storage accounts in subscription {subscription_id}: {e}")
        return []

def get_all_storage_accounts_multi_subscription(credential, subscription_ids=None):
    """Get storage accounts from multiple subscriptions"""
    logger = logging.getLogger(__name__)
    all_storage_accounts = []
    
    if subscription_ids is None:
        # Get all accessible subscriptions
        subscriptions = get_all_subscriptions(credential)
        subscription_ids = [sub.subscription_id for sub in subscriptions]
        logger.info(f"Analyzing all {len(subscription_ids)} subscriptions")
    else:
        logger.info(f"Analyzing {len(subscription_ids)} specified subscriptions")
    
    for subscription_id in subscription_ids:
        logger.info(f"Processing subscription: {subscription_id}")
        storage_accounts = get_storage_accounts_from_subscription(credential, subscription_id)
        all_storage_accounts.extend(storage_accounts)
    
    logger.info(f"Total storage accounts found across all subscriptions: {len(all_storage_accounts)}")
    return all_storage_accounts

def get_all_storage_accounts(storage_client):
    """Get storage accounts from current subscription (legacy function)"""
    logger = logging.getLogger(__name__)
    try:
        storage_accounts = list(storage_client.storage_accounts.list())
        logger.info(f"Found {len(storage_accounts)} storage accounts")
        return storage_accounts
    except Exception as e:
        logger.error(f"Error listing storage accounts: {e}")
        return []

def select_storage_accounts_to_process(storage_accounts, auto_mode=False, account_names=None, account_pattern=None, max_accounts=None):
	total_accounts = len(storage_accounts)
	logger.info(f"Total available storage accounts: {total_accounts}")
	if auto_mode or account_names or account_pattern:
		if account_names:
			selected_accounts = []
			for account_name in account_names:
				matching_accounts = [a for a in storage_accounts if a.name.lower() == account_name.lower()]
				if matching_accounts:
					selected_accounts.extend(matching_accounts)
				else:
					logger.warning(f"Storage account '{account_name}' not found in subscription")
			if not selected_accounts:
				logger.warning("No valid storage accounts found from specified names. Processing all accounts.")
				selected_accounts = storage_accounts
		elif account_pattern:
			selected_accounts = []
			for account in storage_accounts:
				if fnmatch.fnmatch(account.name.lower(), account_pattern.lower()):
					selected_accounts.append(account)
			if not selected_accounts:
				logger.warning(f"No storage accounts matched pattern '{account_pattern}'. Processing all accounts.")
				selected_accounts = storage_accounts
		else:
			selected_accounts = storage_accounts
		if max_accounts and len(selected_accounts) > max_accounts:
			logger.info(f"Limiting to first {max_accounts} storage accounts")
			selected_accounts = selected_accounts[:max_accounts]
		account_names_list = [a.name for a in selected_accounts]
		logger.info(f"Auto mode: Processing {len(selected_accounts)} storage accounts: {', '.join(account_names_list[:3])}" + (f" and {len(account_names_list) - 3} more" if len(account_names_list) > 3 else ""))
		return selected_accounts
	# ...existing code for interactive mode omitted for brevity...
	return storage_accounts

import sys
import json
import subprocess
import logging
from azure.identity import AzureCliCredential, DefaultAzureCredential, InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient

logger = logging.getLogger(__name__)

def get_available_azure_subscriptions():
	subscriptions = []
	# Prefer SDK-based auth first
	try:
		credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
		subscription_client = SubscriptionClient(credential)
		for sub in subscription_client.subscriptions.list():
			subscriptions.append({
				'id': sub.subscription_id,
				'name': sub.display_name,
				'state': sub.state,
				'is_default': False
			})
	except Exception as e:
		logger.warning(f"SDK subscription listing failed: {e}")
		# Fallback to az CLI if SDK fails
		try:
			result = subprocess.run(['az', 'account', 'list', '--output', 'json'], capture_output=True, text=True)
			if result.returncode == 0:
				subscription_data = json.loads(result.stdout)
				for sub in subscription_data:
					subscriptions.append({
						'id': sub['id'],
						'name': sub['name'],
						'state': sub.get('state', 'Unknown'),
						'is_default': sub.get('isDefault', False)
					})
			else:
				logger.warning(f"Error running Azure CLI: {result.stderr}")
		except FileNotFoundError:
			logger.warning("Azure CLI not found. Make sure it's installed and in your PATH.")
		except json.JSONDecodeError:
			logger.warning("Error parsing Azure CLI output")
	return subscriptions

def select_azure_subscription():
	subscriptions = get_available_azure_subscriptions()
	if not subscriptions:
		logger.warning("No Azure subscriptions found. Please configure Azure CLI first.")
		return None
	try:
		result = subprocess.run(['az', 'account', 'show', '--output', 'json'], capture_output=True, text=True)
		if result.returncode == 0:
			current_sub = json.loads(result.stdout)
			current_sub_id = current_sub.get('id')
		else:
			current_sub_id = None
	except Exception:
		current_sub_id = None
	print("\n" + "="*80)
	print(" SELECT AZURE SUBSCRIPTION ".center(80, "="))
	print("="*80)
	print(f"Available Azure subscriptions ({len(subscriptions)}):")
	for i, sub in enumerate(subscriptions, 1):
		current_marker = " (current)" if sub['id'] == current_sub_id else ""
		print(f"{i}. {sub['name']}{current_marker} - ID: {sub['id']}, State: {sub['state']}")
	if current_sub_id:
		print(f"\nC. Continue with current subscription")
	print("X. Cancel and exit")
	while True:
		choice = input("\nEnter your choice (number, 'c', or 'x'): ").strip().lower()
		if choice == 'x':
			return None
		elif choice == 'c' and current_sub_id:
			return current_sub_id
		else:
			try:
				idx = int(choice)
				if 1 <= idx <= len(subscriptions):
					return subscriptions[idx-1]['id']
				else:
					print(f"Please enter a number between 1 and {len(subscriptions)}")
			except ValueError:
				print("Please enter a valid choice")

def check_and_login_to_azure(auto_mode=False):
	# Try SDK-based login first (browser or CLI)
	try:
		# Try browser-based login
		credential = InteractiveBrowserCredential()
		token = credential.get_token("https://management.azure.com/.default")
		if token:
			logger.info("Successfully logged in via browser")
			return True
	except Exception as e:
		logger.warning(f"Browser-based login failed: {e}")
	# Fallback to Azure CLI login
	try:
		credential = AzureCliCredential()
		token = credential.get_token("https://management.azure.com/.default")
		if token:
			logger.info("Successfully logged in via Azure CLI")
			return True
	except Exception as e:
		logger.warning(f"Azure CLI login failed: {e}")
	if auto_mode:
		logger.error("Auto mode requires Azure authentication. Please login interactively or via Azure CLI.")
		return False
	print("\n" + "="*80)
	print(" AZURE LOGIN REQUIRED ".center(80, "="))
	print("="*80)
	print("\nYou need to log in to Azure to continue.")
	print("\nPlease choose a login method:")
	print("1. Interactive browser login")
	print("2. Use Azure CLI login")
	print("X. Cancel and exit")
	while True:
		choice = input("\nEnter your choice (1, 2, or 'x'): ").strip().lower()
		if choice == 'x':
			return False
		elif choice == '1':
			try:
				print("\nLaunching browser for interactive login...")
				credential = InteractiveBrowserCredential()
				token = credential.get_token("https://management.azure.com/.default")
				if token:
					logger.info("Successfully logged in via browser")
					return True
			except Exception as e:
				logger.error(f"Error during interactive login: {e}")
		elif choice == '2':
			try:
				print("\nLaunching Azure CLI login...")
				credential = AzureCliCredential()
				token = credential.get_token("https://management.azure.com/.default")
				if token:
					logger.info("Successfully logged in via Azure CLI")
					return True
				else:
					logger.error("Azure CLI login failed")
			except Exception as e:
				logger.error(f"Error during Azure CLI login: {e}")
		else:
			print("Please enter 1, 2, or 'x'")
	return False

def initialize_azure_clients(subscription_id=None, auto_mode=False):
	if not check_and_login_to_azure(auto_mode):
		logger.error("Azure login required to continue. Exiting.")
		sys.exit(1)
	if not subscription_id:
		if auto_mode:
			try:
				# Use SDK to get the first enabled subscription
				credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
				subscription_client = SubscriptionClient(credential)
				sub = next((s for s in subscription_client.subscriptions.list() if s.state.lower() == 'enabled'), None)
				if sub:
					subscription_id = sub.subscription_id
					logger.info(f"Auto mode: Using current subscription {subscription_id}")
				else:
					logger.error("Could not determine current subscription in auto mode (no enabled subscriptions found)")
					sys.exit(1)
			except Exception as e:
				logger.error(f"Error getting current subscription in auto mode: {e}")
				sys.exit(1)
		else:
			subscription_id = select_azure_subscription()
			if not subscription_id:
				logger.error("Subscription selection canceled. Exiting.")
				sys.exit(1)
	# No need to set active subscription in Azure CLI when using SDK
	logger.info(f"Using subscription {subscription_id} for SDK clients.")
	try:
		try:
			credential = AzureCliCredential()
			subscription_client = SubscriptionClient(credential)
			test_sub = next(subscription_client.subscriptions.list())
			logger.info("Using AzureCliCredential")
		except Exception:
			credential = DefaultAzureCredential()
			logger.info("Using DefaultAzureCredential")
		resource_client = ResourceManagementClient(credential, subscription_id)
		storage_client = StorageManagementClient(credential, subscription_id)
		return credential, subscription_id, resource_client, storage_client
	except Exception as e:
		logger.error(f"Error initializing Azure clients: {e}")
		sys.exit(1)

def initialize_multi_subscription_analysis(subscription_ids=None, auto_mode=False):
	"""Initialize Azure clients for multi-subscription analysis"""
	logger = logging.getLogger(__name__)
	
	if not check_and_login_to_azure(auto_mode):
		logger.error("Azure login required to continue. Exiting.")
		sys.exit(1)
	
	try:
		try:
			credential = AzureCliCredential()
			subscription_client = SubscriptionClient(credential)
			test_sub = next(subscription_client.subscriptions.list())
			logger.info("Using AzureCliCredential for multi-subscription analysis")
		except Exception:
			credential = DefaultAzureCredential()
			logger.info("Using DefaultAzureCredential for multi-subscription analysis")
		
		if subscription_ids is None:
			# Get all accessible subscriptions
			subscriptions = get_all_subscriptions(credential)
			subscription_ids = [sub.subscription_id for sub in subscriptions if sub.state.lower() == 'enabled']
			
			if auto_mode:
				logger.info(f"Auto mode: Found {len(subscription_ids)} enabled subscriptions")
			else:
				# In interactive mode, let user select subscriptions
				print(f"\nFound {len(subscriptions)} accessible subscriptions:")
				for i, sub in enumerate(subscriptions, 1):
					print(f"  {i}. {sub.display_name} ({sub.subscription_id}) - {sub.state}")
				
				choice = input("\nAnalyze all subscriptions? (y/n): ").lower()
				if choice != 'y':
					# Let user select specific subscriptions
					selected_indices = input("Enter subscription numbers (comma-separated): ").split(',')
					try:
						subscription_ids = [subscriptions[int(i.strip())-1].subscription_id for i in selected_indices]
					except (ValueError, IndexError):
						logger.warning("Invalid selection. Using all subscriptions.")
		
		logger.info(f"Will analyze {len(subscription_ids)} subscriptions")
		return credential, subscription_ids
		
	except Exception as e:
		logger.error(f"Error initializing multi-subscription analysis: {e}")
		sys.exit(1)
