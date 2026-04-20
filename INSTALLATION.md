# Installation Guide - Apex Analytix Ticketing System

## Prerequisites
- Frappe Framework 15.73.0+
- Frappe Helpdesk 1.12.0+
- ERPNext 15.69.2+ (optional)

## Installation Steps

### Step 1: Install the App

The app is already installed in your site. If reinstalling:

```bash
# Inside container
cd ~/frappe-bench
bench --site demo.blivora install-app blivora_demo
```

### Step 2: Run Installation Script

This will:
- Create custom fields on HD Ticket
- Create default support groups
- Set up permissions

```bash
# The after_install hook runs automatically during installation
# To run manually:
bench --site demo.blivora console

>>> import frappe
>>> from blivora_demo.blivora_demo.install import after_install
>>> after_install()
```

### Step 3: Create Sample Data (Optional)

```bash
bench --site demo.blivora console

>>> from blivora_demo.blivora_demo.install import create_sample_data
>>> create_sample_data()
```

## Post-Installation Setup

### 1. Create Users

Create users for your support teams:

```
1. Go to: User List
2. Create users for each team:
   - Enterprise Support (10 users)
   - Portal Support (25 users)
   - Portal Implementation-Performance (18 users)
3. Assign appropriate roles
```

### 2. Assign Users to Groups

```
1. Go to: HD Team List
2. Open each group:
   - Enterprise Support
   - Portal Support
   - Portal Implementation-Performance
3. Add team members to each group
```

### 3. Create Client Mappings

```
1. Go to: Blivora Client Mapping
2. Create new mapping:
   - Client: Select customer
   - Support Person: Primary support contact
   - Implementation Person: Implementation contact
   - Default Group: Support group
   - Email Domain: e.g., "lennox.com"
3. Save and activate
```

## Testing the Workflow

### Test 1: Manual Assignment

1. Create a new HD Ticket
2. Set customer (e.g., "Lennox International")
3. Click "Auto Assign" button (or use API)
4. Verify:
   - Ticket assigned to correct person
   - Group set correctly
   - Priority set to Medium
   - Status updated

### Test 2: Email-Based Creation

1. Send email to support address
2. Verify:
   - Ticket created
   - Client auto-detected from email
   - Fields populated from mapping

### Test 3: Enterprise Support Workflow

1. Create ticket (status: New)
2. Enterprise Support responds (status: Open)
3. Verify auto-assignment triggers
4. Check notification sent to assigned person

## API Endpoints

### Auto-Assign Ticket
```javascript
frappe.call({
    method: 'blivora_demo.blivora_demo.api.auto_assignment.auto_assign_ticket',
    args: {
        ticket_name: 'TKT-00001'
    },
    callback: function(r) {
        console.log(r.message);
    }
});
```

### Get Dashboard Data
```javascript
frappe.call({
    method: 'blivora_demo.blivora_demo.api.dashboard.get_ticket_summary',
    callback: function(r) {
        console.log(r.message);
    }
});
```

### Identify Client from Email
```javascript
frappe.call({
    method: 'blivora_demo.blivora_demo.api.auto_assignment.identify_client_from_email',
    args: {
        email_address: 'john@lennox.com'
    },
    callback: function(r) {
        console.log('Client:', r.message);
    }
});
```

## Custom Fields Added to HD Ticket

### Priority & Status
- `apex_priority`: Low, Medium, High, Critical
- `internal_team_status`: 21 status values

### Assignment
- `apex_support_person`: Primary support contact
- `apex_implementation_person`: Implementation contact
- `apex_default_group`: Assigned group

### Categorization
- `apex_product_service`: Product/Service affected
- `apex_division`: Business division
- `apex_issue_type`: Issue, Inquiry, Feature Request, etc.
- `apex_application`: Apex application affected
- `apex_module`: Module/component
- `apex_project_code`: Project reference
- `apex_client_priority`: Client's perceived priority

## Troubleshooting

### Custom Fields Not Showing

```bash
# Reinstall custom fields
bench --site demo.blivora console

>>> from blivora_demo.blivora_demo.doctype.blivora_client_mapping.blivora_custom_fields import create_apex_custom_fields
>>> create_apex_custom_fields()
```

### Auto-Assignment Not Working

1. Check client mapping exists and is active
2. Verify support person is valid user
3. Check event hooks in hooks.py
4. Check error logs:
   ```bash
   bench --site demo.blivora console
   >>> import frappe
   >>> frappe.get_all("Error Log", limit=5)
   ```

### Groups Not Created

```bash
bench --site demo.blivora console

>>> from blivora_demo.blivora_demo.install import create_default_groups
>>> create_default_groups()
```

## Next Steps

1. ✅ Install app and run setup
2. ✅ Create users and assign to groups
3. ✅ Create client mappings
4. ✅ Test auto-assignment workflow
5. ⏭️ Apply Apex branding (colors, logo)
6. ⏭️ Create custom dashboard page
7. ⏭️ Configure email integration
8. ⏭️ Set up SLA policies
9. ⏭️ Create sample tickets for demo
10. ⏭️ Prepare management presentation

## Support

For issues or questions:
- GitHub: https://github.com/rahul190688/blivora-demo
- Developer: Rahul Kumar (rk190688@gmail.com)
