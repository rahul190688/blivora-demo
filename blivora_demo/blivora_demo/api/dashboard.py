# Copyright (c) 2026, Rahul Kumar and contributors
# For license information, please see license.txt

"""
Dashboard APIs for Apex Analytix Ticketing System
"""

import frappe
from frappe import _


@frappe.whitelist()
def get_ticket_summary():
	"""
	Get summary of tickets by status and priority

	Returns:
		dict: Ticket summary data
	"""
	# Tickets by status
	status_counts = frappe.db.sql("""
		SELECT
			COALESCE(internal_team_status, 'No Status') as status,
			COUNT(*) as count
		FROM `tabHD Ticket`
		GROUP BY internal_team_status
		ORDER BY count DESC
	""", as_dict=True)

	# Tickets by priority
	priority_counts = frappe.db.sql("""
		SELECT
			COALESCE(apex_priority, 'No Priority') as priority,
			COUNT(*) as count
		FROM `tabHD Ticket`
		GROUP BY apex_priority
		ORDER BY
			CASE apex_priority
				WHEN 'Critical' THEN 1
				WHEN 'High' THEN 2
				WHEN 'Medium' THEN 3
				WHEN 'Low' THEN 4
				ELSE 5
			END
	""", as_dict=True)

	# Tickets by group
	group_counts = frappe.db.sql("""
		SELECT
			COALESCE(apex_default_group, 'Unassigned') as group_name,
			COUNT(*) as count
		FROM `tabHD Ticket`
		GROUP BY apex_default_group
		ORDER BY count DESC
	""", as_dict=True)

	# Total tickets
	total_tickets = frappe.db.count("HD Ticket")

	# Open tickets (not closed/resolved)
	open_tickets = frappe.db.count("HD Ticket", {
		"internal_team_status": ["not in", ["Closed", "Resolved"]]
	})

	return {
		"total_tickets": total_tickets,
		"open_tickets": open_tickets,
		"status_breakdown": status_counts,
		"priority_breakdown": priority_counts,
		"group_breakdown": group_counts
	}


@frappe.whitelist()
def get_agent_workload(group=None):
	"""
	Get workload for each agent

	Args:
		group (str): Optional - filter by group

	Returns:
		list: Agent workload data
	"""
	filters = {}
	if group:
		filters["apex_default_group"] = group

	# Get assigned tickets per agent
	workload = frappe.db.sql("""
		SELECT
			apex_support_person as agent,
			COUNT(*) as open_tickets,
			SUM(CASE WHEN apex_priority = 'Critical' THEN 1 ELSE 0 END) as critical_tickets,
			SUM(CASE WHEN apex_priority = 'High' THEN 1 ELSE 0 END) as high_tickets
		FROM `tabHD Ticket`
		WHERE
			internal_team_status NOT IN ('Closed', 'Resolved')
			AND apex_support_person IS NOT NULL
			{group_filter}
		GROUP BY apex_support_person
		ORDER BY open_tickets DESC
	""".format(
		group_filter=f"AND apex_default_group = '{group}'" if group else ""
	), as_dict=True)

	return workload


@frappe.whitelist()
def get_recent_tickets(limit=10):
	"""
	Get recent tickets

	Args:
		limit (int): Number of tickets to return

	Returns:
		list: Recent tickets
	"""
	tickets = frappe.get_all(
		"HD Ticket",
		fields=[
			"name",
			"subject",
			"customer",
			"apex_priority",
			"internal_team_status",
			"apex_default_group",
			"creation",
			"modified"
		],
		order_by="creation desc",
		limit=limit
	)

	return tickets


@frappe.whitelist()
def get_group_performance(group_name):
	"""
	Get performance metrics for a specific group

	Args:
		group_name (str): Group name

	Returns:
		dict: Group performance data
	"""
	# Total tickets for group
	total = frappe.db.count("HD Ticket", {"apex_default_group": group_name})

	# Open tickets
	open_count = frappe.db.count("HD Ticket", {
		"apex_default_group": group_name,
		"internal_team_status": ["not in", ["Closed", "Resolved"]]
	})

	# Closed tickets
	closed_count = frappe.db.count("HD Ticket", {
		"apex_default_group": group_name,
		"internal_team_status": "Closed"
	})

	# Average resolution time (if you have resolution_date field)
	# This is a placeholder - implement based on your actual fields
	avg_resolution_time = "N/A"

	return {
		"group_name": group_name,
		"total_tickets": total,
		"open_tickets": open_count,
		"closed_tickets": closed_count,
		"avg_resolution_time": avg_resolution_time
	}
