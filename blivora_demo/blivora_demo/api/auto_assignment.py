# Copyright (c) 2026, Rahul Kumar and contributors
# For license information, please see license.txt

"""
Auto-Assignment Engine for Apex Analytix Ticketing System

This module handles automatic ticket assignment based on:
1. Client-to-agent mapping
2. Ticket type (support vs implementation)
3. Group routing
4. Enterprise Support workflow
"""

import frappe
from frappe import _
from frappe.desk.form.assign_to import add as assign_to


@frappe.whitelist()
def auto_assign_ticket(ticket_name):
	"""
	Auto-assign ticket based on client mapping

	Args:
		ticket_name (str): HD Ticket name

	Returns:
		dict: Assignment result
	"""
	try:
		ticket = frappe.get_doc("HD Ticket", ticket_name)

		# Check if ticket has a customer/client
		if not ticket.customer:
			return {
				"success": False,
				"message": "No customer found on ticket. Cannot auto-assign."
			}

		# Get client mapping
		mapping = get_client_mapping_for_ticket(ticket)

		if not mapping:
			return {
				"success": False,
				"message": f"No client mapping found for customer: {ticket.customer}"
			}

		# Determine which person to assign based on ticket type
		assignee = determine_assignee(ticket, mapping)

		if not assignee:
			return {
				"success": False,
				"message": "Could not determine assignee from mapping"
			}

		# Perform assignment
		result = assign_ticket(ticket, assignee, mapping)

		return result

	except Exception as e:
		frappe.log_error(f"Auto-assignment failed for {ticket_name}: {str(e)}")
		return {
			"success": False,
			"message": f"Error during auto-assignment: {str(e)}"
		}


def get_client_mapping_for_ticket(ticket):
	"""
	Get client mapping for a ticket

	Args:
		ticket: HD Ticket document

	Returns:
		dict: Client mapping or None
	"""
	# Check if customer exists in mapping
	mapping = frappe.db.get_value(
		"Blivora Client Mapping",
		{"client": ticket.customer, "active": 1},
		[
			"support_person",
			"implementation_person",
			"default_group",
			"backup_group",
			"sla_level",
			"contract_level"
		],
		as_dict=True
	)

	return mapping


def determine_assignee(ticket, mapping):
	"""
	Determine which person should be assigned based on ticket type

	Args:
		ticket: HD Ticket document
		mapping: Client mapping dict

	Returns:
		str: User email to assign to
	"""
	# Check if it's an implementation-related ticket
	is_implementation = check_if_implementation_ticket(ticket)

	if is_implementation and mapping.get("implementation_person"):
		return mapping.get("implementation_person")
	elif mapping.get("support_person"):
		return mapping.get("support_person")

	return None


def check_if_implementation_ticket(ticket):
	"""
	Check if ticket is implementation-related

	Args:
		ticket: HD Ticket document

	Returns:
		bool: True if implementation ticket
	"""
	# Check custom fields
	if hasattr(ticket, "apex_issue_type"):
		if ticket.apex_issue_type in ["Feature Request", "Access Request"]:
			return True

	if hasattr(ticket, "apex_default_group"):
		if "Implementation" in str(ticket.apex_default_group):
			return True

	# Check subject/description keywords
	keywords = ["implementation", "deploy", "install", "setup", "configure"]
	subject = (ticket.subject or "").lower()
	description = (ticket.description or "").lower()

	for keyword in keywords:
		if keyword in subject or keyword in description:
			return True

	return False


def assign_ticket(ticket, assignee, mapping):
	"""
	Assign ticket to user and update fields

	Args:
		ticket: HD Ticket document
		assignee: User email
		mapping: Client mapping dict

	Returns:
		dict: Assignment result
	"""
	try:
		# Assign to user
		assign_to({
			"assign_to": [assignee],
			"doctype": "HD Ticket",
			"name": ticket.name,
			"description": f"Auto-assigned based on client mapping"
		})

		# Update ticket fields
		ticket.reload()

		# Set custom fields
		is_implementation = check_if_implementation_ticket(ticket)

		if is_implementation:
			ticket.apex_implementation_person = assignee
		else:
			ticket.apex_support_person = assignee

		# Set default group
		if mapping.get("default_group"):
			ticket.apex_default_group = mapping.get("default_group")

		# Set default priority if not set
		if not hasattr(ticket, "apex_priority") or not ticket.apex_priority:
			ticket.apex_priority = "Medium"

		# Set internal status if not set
		if not hasattr(ticket, "internal_team_status") or not ticket.internal_team_status:
			ticket.internal_team_status = "Open"

		# Save changes
		ticket.save(ignore_permissions=True)

		frappe.db.commit()

		return {
			"success": True,
			"message": f"Ticket assigned to {assignee}",
			"assignee": assignee,
			"group": mapping.get("default_group"),
			"priority": ticket.apex_priority if hasattr(ticket, "apex_priority") else None
		}

	except Exception as e:
		frappe.log_error(f"Error assigning ticket {ticket.name}: {str(e)}")
		return {
			"success": False,
			"message": f"Assignment failed: {str(e)}"
		}


@frappe.whitelist()
def identify_client_from_email(email_address):
	"""
	Identify client from email address

	Args:
		email_address (str): Email address

	Returns:
		str: Client name or None
	"""
	if not email_address:
		return None

	# Method 1: Check exact match in HD Customer
	customer = frappe.db.get_value(
		"HD Customer",
		{"email_id": email_address},
		"name"
	)

	if customer:
		return customer

	# Method 2: Check email domain in client mapping
	domain = email_address.split("@")[-1] if "@" in email_address else None

	if domain:
		client = frappe.db.get_value(
			"Blivora Client Mapping",
			{"email_domain": domain, "active": 1},
			"client"
		)

		if client:
			return client

	return None


@frappe.whitelist()
def bulk_auto_assign_tickets(filters=None):
	"""
	Bulk auto-assign multiple tickets

	Args:
		filters (dict): Filters for tickets to assign

	Returns:
		dict: Results summary
	"""
	if filters is None:
		filters = {
			"status": "Open",
			"_assign": ["is", "not set"]
		}

	tickets = frappe.get_all("HD Ticket", filters=filters, pluck="name")

	results = {
		"total": len(tickets),
		"success": 0,
		"failed": 0,
		"errors": []
	}

	for ticket_name in tickets:
		result = auto_assign_ticket(ticket_name)

		if result.get("success"):
			results["success"] += 1
		else:
			results["failed"] += 1
			results["errors"].append({
				"ticket": ticket_name,
				"error": result.get("message")
			})

	return results


def on_ticket_create(doc, method):
	"""
	Hook: When ticket is created via email
	Auto-detect client and populate fields

	Args:
		doc: HD Ticket document
		method: Event method
	"""
	# Check if customer is not set
	if not doc.customer and doc.raised_by:
		# Try to identify client from email
		client = identify_client_from_email(doc.raised_by)

		if client:
			doc.customer = client

			# Get mapping and populate fields
			mapping = frappe.db.get_value(
				"Blivora Client Mapping",
				{"client": client, "active": 1},
				["default_group", "sla_level"],
				as_dict=True
			)

			if mapping:
				if mapping.get("default_group"):
					doc.apex_default_group = mapping.get("default_group")


def on_ticket_update(doc, method):
	"""
	Hook: When ticket is updated
	Check if Enterprise Support has responded and auto-assign

	Args:
		doc: HD Ticket document
		method: Event method
	"""
	# Check if status changed to Open (Enterprise Support responded)
	if doc.has_value_changed("status") and doc.status == "Open":
		# Check if not already assigned
		if not frappe.db.get_value("HD Ticket", doc.name, "_assign"):
			# Trigger auto-assignment
			frappe.enqueue(
				auto_assign_ticket,
				ticket_name=doc.name,
				queue="short"
			)
