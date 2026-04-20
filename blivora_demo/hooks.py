app_name = "blivora_demo"
app_title = "Apex Analytix Ticketing"
app_publisher = "Rahul Kumar"
app_description = "Custom Ticketing System for Apex Analytix based on Frappe Helpdesk"
app_email = "rk190688@gmail.com"
app_license = "MIT"

# Includes in <head>
# app_include_css = "/assets/blivora_demo/css/blivora_demo.css"
# app_include_js = "/assets/blivora_demo/js/blivora_demo.js"

# Installation
after_install = "blivora_demo.blivora_demo.install.after_install"

# Desk Notifications
# notification_config = "blivora_demo.notifications.get_notification_config"

# Document Events
doc_events = {
	"HD Ticket": {
		"after_insert": "blivora_demo.blivora_demo.api.auto_assignment.on_ticket_create",
		"on_update": "blivora_demo.blivora_demo.api.auto_assignment.on_ticket_update",
	}
}

# Scheduled Tasks
# scheduler_events = {
# 	"daily": [
# 		"blivora_demo.tasks.daily"
# 	]
# }
