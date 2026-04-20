# Copyright (c) 2026, Rahul Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BlivoraClientMapping(Document):
	"""
	Client-to-Agent Mapping for Auto-Assignment

	This DocType maps clients to their designated support personnel,
	enabling automatic ticket routing based on client information.
	"""

	def validate(self):
		"""Validate the client mapping configuration"""
		self.validate_users()
		self.validate_group()
		self.extract_email_domain()

	def validate_users(self):
		"""Ensure support and implementation persons are valid users"""
		if self.support_person:
			if not frappe.db.exists("User", self.support_person):
				frappe.throw(f"Support Person {self.support_person} does not exist")

		if self.implementation_person:
			if not frappe.db.exists("User", self.implementation_person):
				frappe.throw(f"Implementation Person {self.implementation_person} does not exist")

	def validate_group(self):
		"""Ensure default group exists"""
		if self.default_group:
			if not frappe.db.exists("HD Team", self.default_group):
				frappe.throw(f"Default Group {self.default_group} does not exist")

	def extract_email_domain(self):
		"""Auto-extract email domain from client if available"""
		if not self.email_domain and self.client:
			# Try to get email domain from customer
			customer = frappe.get_doc("HD Customer", self.client)
			if hasattr(customer, "email_id") and customer.email_id:
				domain = customer.email_id.split("@")[-1]
				self.email_domain = domain


@frappe.whitelist()
def get_client_mapping(client):
	"""
	Get client mapping for a given client

	Args:
		client (str): Client name

	Returns:
		dict: Client mapping details or None
	"""
	if not client:
		return None

	mapping = frappe.db.get_value(
		"Blivora Client Mapping",
		{"client": client, "active": 1},
		["support_person", "implementation_person", "default_group", "sla_level", "contract_level"],
		as_dict=True
	)

	return mapping


@frappe.whitelist()
def get_client_from_email(email):
	"""
	Identify client from email address

	Args:
		email (str): Email address

	Returns:
		str: Client name or None
	"""
	if not email:
		return None

	# Method 1: Check exact registered email in HD Customer
	customer = frappe.db.get_value("HD Customer", {"email_id": email}, "name")
	if customer:
		return customer

	# Method 2: Check email domain in client mapping
	domain = email.split("@")[-1] if "@" in email else None
	if domain:
		mapping = frappe.db.get_value(
			"Blivora Client Mapping",
			{"email_domain": domain, "active": 1},
			"client"
		)
		if mapping:
			return mapping

	return None
