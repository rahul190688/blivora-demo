# Custom Fields for HD Ticket - Apex Analytix Requirements
# This file defines custom fields to be added to HD Ticket

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_apex_custom_fields():
	"""
	Create custom fields for Apex Analytix ticketing system
	"""

	custom_fields = {
		"HD Ticket": [
			# Priority Field
			{
				"fieldname": "apex_priority",
				"label": "Priority",
				"fieldtype": "Select",
				"options": "Low\nMedium\nHigh\nCritical",
				"default": "Medium",
				"insert_after": "status",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"reqd": 0
			},
			# Internal Team Status (21 values)
			{
				"fieldname": "internal_team_status",
				"label": "Internal Team Status",
				"fieldtype": "Select",
				"options": "\n".join([
					"New",
					"Open",
					"In Progress",
					"Resolved",
					"Closed",
					"Change Request/Enhancement Request",
					"Client Approval on Change Request",
					"Client Response Received",
					"Pending LOE",
					"Pending Next Release",
					"Pending Future Release",
					"Project",
					"Pending Customer Testing",
					"Pending Apex Update/Testing",
					"Continued Production Monitoring",
					"Waiting on customer",
					"Waiting on third party"
				]),
				"default": "New",
				"insert_after": "apex_priority",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"reqd": 0
			},
			# Section Break for Apex Details
			{
				"fieldname": "apex_assignment_section",
				"label": "Apex Assignment Details",
				"fieldtype": "Section Break",
				"insert_after": "internal_team_status",
				"collapsible": 1
			},
			# Support Person
			{
				"fieldname": "apex_support_person",
				"label": "Support Person",
				"fieldtype": "Link",
				"options": "User",
				"insert_after": "apex_assignment_section",
				"in_list_view": 0,
				"read_only": 0
			},
			# Implementation Person
			{
				"fieldname": "apex_implementation_person",
				"label": "Implementation Person",
				"fieldtype": "Link",
				"options": "User",
				"insert_after": "apex_support_person",
				"in_list_view": 0
			},
			# Column Break
			{
				"fieldname": "apex_column_break_1",
				"fieldtype": "Column Break",
				"insert_after": "apex_implementation_person"
			},
			# Default Group
			{
				"fieldname": "apex_default_group",
				"label": "Assigned Group",
				"fieldtype": "Link",
				"options": "HD Team",
				"insert_after": "apex_column_break_1",
				"in_list_view": 1,
				"in_standard_filter": 1
			},
			# Client Reference (for mapping lookup)
			{
				"fieldname": "apex_client_mapping",
				"label": "Client Mapping",
				"fieldtype": "Link",
				"options": "Blivora Client Mapping",
				"insert_after": "apex_default_group",
				"read_only": 1,
				"hidden": 1
			},
			# Section Break for Additional Fields
			{
				"fieldname": "apex_additional_section",
				"label": "Additional Information",
				"fieldtype": "Section Break",
				"insert_after": "apex_client_mapping",
				"collapsible": 1
			},
			# Product/Service
			{
				"fieldname": "apex_product_service",
				"label": "Product/Service",
				"fieldtype": "Select",
				"options": "\n".join([
					"Risk Management Platform",
					"Payment Processing",
					"Supplier Onboarding",
					"Audit & Recovery",
					"Compliance Platform",
					"Portal",
					"Other"
				]),
				"insert_after": "apex_additional_section",
				"in_standard_filter": 1
			},
			# Division
			{
				"fieldname": "apex_division",
				"label": "Division",
				"fieldtype": "Select",
				"options": "\n".join([
					"Finance & Accounting",
					"Supplier Risk",
					"Compliance & Audit",
					"IT & Systems",
					"Operations",
					"Recovery Services"
				]),
				"insert_after": "apex_product_service",
				"in_standard_filter": 1
			},
			# Column Break
			{
				"fieldname": "apex_column_break_2",
				"fieldtype": "Column Break",
				"insert_after": "apex_division"
			},
			# Issue Type
			{
				"fieldname": "apex_issue_type",
				"label": "Issue Type",
				"fieldtype": "Select",
				"options": "Issue\nInquiry\nFeature Request\nAccess Request\nTraining Request",
				"insert_after": "apex_column_break_2",
				"in_standard_filter": 1
			},
			# Apex Application/Service
			{
				"fieldname": "apex_application",
				"label": "Apex Application",
				"fieldtype": "Select",
				"options": "\n".join([
					"Risk Portal",
					"Supplier Management",
					"Payment Platform",
					"Audit System",
					"Compliance Dashboard",
					"Other"
				]),
				"insert_after": "apex_issue_type",
				"in_standard_filter": 1
			},
			# Module
			{
				"fieldname": "apex_module",
				"label": "Module",
				"fieldtype": "Data",
				"insert_after": "apex_application"
			},
			# Section Break for Project Details
			{
				"fieldname": "apex_project_section",
				"label": "Project Details",
				"fieldtype": "Section Break",
				"insert_after": "apex_module",
				"collapsible": 1
			},
			# Project Code
			{
				"fieldname": "apex_project_code",
				"label": "Project Code",
				"fieldtype": "Data",
				"insert_after": "apex_project_section"
			},
			# Client Perceived Priority
			{
				"fieldname": "apex_client_priority",
				"label": "Client Perceived Priority",
				"fieldtype": "Select",
				"options": "Critical - Business stopped\nHigh - Major impact\nMedium - Moderate impact\nLow - Minor inconvenience",
				"insert_after": "apex_project_code"
			}
		]
	}

	create_custom_fields(custom_fields, update=True)
	frappe.db.commit()

	print("✅ Custom fields created successfully!")


def remove_apex_custom_fields():
	"""Remove all Apex custom fields from HD Ticket"""
	custom_fields = frappe.get_all(
		"Custom Field",
		filters={"dt": "HD Ticket", "fieldname": ["like", "apex_%"]},
		pluck="name"
	)

	for field in custom_fields:
		frappe.delete_doc("Custom Field", field)

	frappe.db.commit()
	print("✅ Custom fields removed successfully!")
