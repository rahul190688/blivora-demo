# Copyright (c) 2026, Rahul Kumar and contributors
# For license information, please see license.txt

"""
Installation and Setup for Apex Analytix Ticketing System
"""

import frappe
from frappe import _


def after_install():
	"""
	Run after app installation
	"""
	print("\n" + "="*60)
	print("Installing Apex Analytix Ticketing System...")
	print("="*60 + "\n")

	# Step 1: Create custom fields
	print("→ Creating custom fields for HD Ticket...")
	create_custom_fields()

	# Step 2: Create default groups
	print("→ Creating default support groups...")
	create_default_groups()

	# Step 3: Set up permissions
	print("→ Configuring permissions...")
	setup_permissions()

	print("\n" + "="*60)
	print("✅ Apex Analytix Ticketing System installed successfully!")
	print("="*60 + "\n")

	print("Next Steps:")
	print("1. Create users and assign to groups")
	print("2. Set up client mappings")
	print("3. Configure email integration")
	print("4. Test auto-assignment workflow")
	print("\n")


def create_custom_fields():
	"""Create custom fields for HD Ticket"""
	try:
		from blivora_demo.blivora_demo.doctype.blivora_client_mapping.blivora_custom_fields import create_apex_custom_fields
		create_apex_custom_fields()
		print("   ✅ Custom fields created")
	except Exception as e:
		print(f"   ⚠️  Error creating custom fields: {str(e)}")
		frappe.log_error(f"Custom field creation error: {str(e)}")


def create_default_groups():
	"""Create default support groups"""
	groups = [
		{
			"name": "Enterprise Support",
			"description": "First responders - initial triage and customer response"
		},
		{
			"name": "Portal Support",
			"description": "Portal-related tickets and end-user support"
		},
		{
			"name": "Portal Implementation-Performance",
			"description": "Implementation projects and performance optimization"
		}
	]

	for group_data in groups:
		try:
			if not frappe.db.exists("HD Team", group_data["name"]):
				team = frappe.get_doc({
					"doctype": "HD Team",
					"team_name": group_data["name"],
					"description": group_data["description"]
				})
				team.insert(ignore_permissions=True)
				print(f"   ✅ Created group: {group_data['name']}")
			else:
				print(f"   ℹ️  Group already exists: {group_data['name']}")
		except Exception as e:
			print(f"   ⚠️  Error creating group {group_data['name']}: {str(e)}")


def setup_permissions():
	"""Set up permissions for Blivora doctypes"""
	try:
		# Add Support Team role if it doesn't exist
		if not frappe.db.exists("Role", "Support Team"):
			role = frappe.get_doc({
				"doctype": "Role",
				"role_name": "Support Team",
				"desk_access": 1
			})
			role.insert(ignore_permissions=True)
			print("   ✅ Created Support Team role")

		print("   ✅ Permissions configured")
	except Exception as e:
		print(f"   ⚠️  Error setting up permissions: {str(e)}")


def create_sample_data():
	"""
	Create sample data for testing
	Call this manually: bench execute blivora_demo.blivora_demo.install.create_sample_data
	"""
	print("\n" + "="*60)
	print("Creating Sample Data for Testing...")
	print("="*60 + "\n")

	# Sample customers
	customers = [
		{
			"customer_name": "Lennox International",
			"email_id": "support@lennox.com",
			"domain": "lennox.com"
		},
		{
			"customer_name": "Acme Corporation",
			"email_id": "helpdesk@acme.com",
			"domain": "acme.com"
		},
		{
			"customer_name": "Demo Client",
			"email_id": "demo@example.com",
			"domain": "example.com"
		}
	]

	print("→ Creating sample customers...")
	for cust_data in customers:
		try:
			if not frappe.db.exists("HD Customer", cust_data["customer_name"]):
				customer = frappe.get_doc({
					"doctype": "HD Customer",
					"customer_name": cust_data["customer_name"],
					"email_id": cust_data["email_id"]
				})
				customer.insert(ignore_permissions=True)
				print(f"   ✅ Created customer: {cust_data['customer_name']}")
			else:
				print(f"   ℹ️  Customer exists: {cust_data['customer_name']}")
		except Exception as e:
			print(f"   ⚠️  Error: {str(e)}")

	# Sample client mappings
	print("\n→ Creating sample client mappings...")
	print("   ℹ️  Note: Update with actual user emails after creating users")

	mappings = [
		{
			"client": "Lennox International",
			"email_domain": "lennox.com",
			"support_person": "Administrator",  # Replace with actual user
			"default_group": "Portal Support",
			"sla_level": "Enterprise",
			"contract_level": "Strategic Partner"
		}
	]

	for mapping_data in mappings:
		try:
			if not frappe.db.exists("Blivora Client Mapping", mapping_data["client"]):
				mapping = frappe.get_doc({
					"doctype": "Blivora Client Mapping",
					**mapping_data
				})
				mapping.insert(ignore_permissions=True)
				print(f"   ✅ Created mapping for: {mapping_data['client']}")
			else:
				print(f"   ℹ️  Mapping exists: {mapping_data['client']}")
		except Exception as e:
			print(f"   ⚠️  Error: {str(e)}")

	frappe.db.commit()

	print("\n" + "="*60)
	print("✅ Sample data created!")
	print("="*60 + "\n")
