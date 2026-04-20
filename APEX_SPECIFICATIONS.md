# Apex Analytix - Technical Specifications

**Last Updated:** April 20, 2026
**Status:** APPROVED - Ready to Build

---

## 1. Priority Levels

**Field:** Priority (Select)
**Values:**
- Low
- Medium (default when assigned)
- High
- Critical

**Criticality Rules:**
- **Critical:** System down, production outage
- **High:** Payment issues, major functionality broken
- **Medium:** General inquiries, moderate impact
- **Low:** Minor questions, cosmetic issues

**Also Influenced By:**
- Client contract level
- SLA agreements
- Agent judgment

---

## 2. Status Values

**Field:** Status (Select)
**Total Values:** 21 statuses

### Core Workflow Statuses:
1. New
2. Open
3. In Progress
4. Resolved
5. Closed

### Change Management:
6. Change Request/Enhancement Request
7. Client Approval on Change Request

### Pending States:
8. Client Response Received
9. Pending LOE
10. Pending Next Release
11. Pending Future Release
12. Pending Customer Testing
13. Pending Apex Update/Testing
14. Continued Production Monitoring

### Waiting States:
15. Waiting on customer
16. Waiting on third party

### Special:
17. Project

**NOTE:** Priority and Status are SEPARATE fields!

---

## 3. Support Groups

### Initial Setup (3 Groups):

#### Group 1: Enterprise Support
- **Size:** 10 people
- **Role:** First responders, initial triage
- **Responsibilities:**
  - Receive all new tickets
  - Send initial customer response
  - Route to appropriate support group
  - Set initial priority

#### Group 2: Portal Support
- **Size:** 25 people
- **Responsibilities:**
  - Portal-related tickets
  - End-user support
  - Portal functionality issues

#### Group 3: Portal Implementation-Performance
- **Size:** 18 people
- **Responsibilities:**
  - Implementation projects
  - Performance optimization
  - Technical implementation support

**Total Agents:** 53 people across 3 groups

**Future:** Will expand to 20+ groups

---

## 4. Client-Agent Mapping

### Example Mapping:

```
Client: Lennox International
├── Support Person: Pranay Kumar
├── Implementation Person: Vishal Saxena
└── Default Group: Portal Support
```

### Mapping Fields:

**DocType:** `Blivora Client Mapping`

| Field | Type | Description |
|-------|------|-------------|
| Client | Link (Customer) | Customer/Client name |
| Support Person | Link (User) | Primary support contact |
| Implementation Person | Link (User) | Implementation contact |
| Default Group | Link (HD Team) | Default support group |
| SLA Level | Select | SLA tier (if applicable) |
| Contract Level | Select | Contract type |
| Active | Check | Is mapping active? |

### Auto-Assignment Logic:

```python
When ticket is assigned by Enterprise Support:
1. Get client name from ticket
2. Look up client in Blivora Client Mapping
3. Check ticket type:
   - If implementation-related → Assign to Implementation Person
   - Else → Assign to Support Person
4. Set default group
5. Set priority to Medium (unless specified)
6. Notify assigned person
```

---

## 5. Email Identification

### Client Detection Methods:

#### Method 1: Email Domain Matching
```
Email: jaya@lennox.com
Domain: lennox.com
→ Match to: Lennox International
```

#### Method 2: Pre-registered Email Addresses
```
Customer Master → Registered Email Addresses
├── jaya@lennox.com
├── support@lennox.com
└── it.help@lennox.com
```

### Implementation:
1. **Customer DocType** extended with:
   - Email Domain (Data field)
   - Registered Email Addresses (Table field)

2. **Ticket Creation Process:**
   ```
   Email arrives → Extract sender email
   → Check registered emails first
   → If not found, check domain
   → Match to customer
   → Apply client mapping
   → Auto-assign
   ```

---

## 6. Ticket Workflow

### Complete Flow:

```
┌─────────────────────────────────────────────────────────┐
│ 1. Email Arrives                                        │
│    From: jaya@lennox.com                               │
│    To: support@apexanalytix.com                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Ticket Auto-Created                                  │
│    Client: Lennox International (auto-detected)        │
│    Status: New                                          │
│    Priority: Not set                                    │
│    Assigned: None                                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Enterprise Support Queue                             │
│    Visible to: Enterprise Support Team (10 people)     │
│    Action: Review and respond                           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Enterprise Support Responds                          │
│    Status: Open                                         │
│    Response: "Thank you, we're looking into this..."   │
│    Action: Click "Assign to Support Person"            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Auto-Assignment (via Client Mapping)                │
│    Look up: Lennox International                        │
│    Found: Support Person = Pranay Kumar                 │
│    Assigned: Pranay Kumar                               │
│    Group: Portal Support                                │
│    Priority: Medium (default)                           │
│    Status: Open                                         │
│    Notification: Sent to Pranay Kumar                   │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Pranay Works on Ticket                              │
│    Can change: Priority (based on criticality)         │
│    Can change: Status (In Progress, Waiting, etc.)     │
│    Can add: Comments, updates                           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Resolution                                           │
│    Status: Resolved → Closed                            │
│    Customer: Notified                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 7. POC Implementation Plan

### Phase 1: Core Structure (Day 1-2)

#### Create Custom Fields on HD Ticket:
1. **Priority** (Select)
   - Low, Medium, High, Critical

2. **Internal Team Status** (Select)
   - All 21 status values

3. **Client** (Link to Customer)
   - Auto-populated from email

4. **Support Person** (Link to User)
   - Auto-populated from mapping

5. **Implementation Person** (Link to User)
   - From client mapping

6. **Default Group** (Link to HD Team)
   - From client mapping

#### Create New DocType: Blivora Client Mapping
- Fields as specified above
- Form view for easy configuration
- List view for quick reference

#### Create Groups:
1. Enterprise Support (10 members)
2. Portal Support (25 members)
3. Portal Implementation-Performance (18 members)

### Phase 2: Auto-Assignment (Day 3)

#### Server Script: Auto-Assignment Logic
```python
# Trigger: When ticket is assigned by Enterprise Support
# Action: Look up client mapping and auto-assign

def auto_assign_ticket(doc, method):
    if doc.status == "Open" and not doc.assigned_to:
        # Get client mapping
        mapping = frappe.get_doc("Blivora Client Mapping",
                                  {"client": doc.client})

        # Determine which person to assign
        if is_implementation_ticket(doc):
            assign_to = mapping.implementation_person
        else:
            assign_to = mapping.support_person

        # Assign ticket
        assign({"assign_to": [assign_to],
                "doctype": "HD Ticket",
                "name": doc.name})

        # Set defaults
        doc.priority = "Medium"
        doc.default_group = mapping.default_group
        doc.save()
```

### Phase 3: Email Integration (Day 4)

#### Email-to-Client Matching
```python
# When email arrives
def identify_client(email_address):
    # Method 1: Check registered emails
    client = frappe.db.get_value("Customer",
                                   {"registered_emails": ["like", f"%{email_address}%"]},
                                   "name")

    if client:
        return client

    # Method 2: Check email domain
    domain = email_address.split("@")[1]
    client = frappe.db.get_value("Customer",
                                   {"email_domain": domain},
                                   "name")

    return client
```

### Phase 4: Dashboard & Reporting (Day 5)

#### Simple Dashboard showing:
1. Tickets by Status (pie chart)
2. Tickets by Priority (bar chart)
3. Tickets by Group (bar chart)
4. Agent Workload (table)
5. Response Time Metrics
6. SLA Compliance

---

## 8. Success Metrics for POC

### Demonstrate to Management:

1. **Auto-Assignment Works** ✅
   - Show email → ticket → auto-assign flow
   - Highlight time saved (no manual routing)

2. **Client Mapping** ✅
   - Show configuration interface
   - Demonstrate automatic routing

3. **Enterprise Support Workflow** ✅
   - Show first responder queue
   - Show handoff process

4. **Status Management** ✅
   - Show 21 status options
   - Demonstrate workflow flexibility

5. **Cost Savings** ✅
   - Freshdesk Enterprise: $79/agent × 53 = $4,187/month = **$50,244/year**
   - Blivora Demo: **$0**
   - **Savings: $50,000+/year**

---

## 9. Data Requirements for POC

### Sample Data to Create:

#### Customers (5-10):
1. Lennox International
2. Acme Corporation
3. XYZ Industries
4. ABC Company
5. Demo Client 1-5

#### Users/Agents:
- Enterprise Support: 10 users
- Portal Support: 5-10 users (sample)
- Implementation: 5-10 users (sample)

#### Client Mappings:
- 5-10 mappings matching customers
- Mix of support/implementation assignments

#### Test Tickets:
- 10-15 sample tickets
- Various statuses and priorities
- Assigned to different groups

---

## 10. Technical Stack

### Backend:
- Frappe Framework 15.73.0
- Python 3.10
- MariaDB 10.6

### Custom Components:
- `Blivora Client Mapping` DocType
- Custom fields on `HD Ticket`
- Auto-assignment server script
- Email parsing hooks
- Custom dashboard

### Integration:
- Email (SMTP/IMAP)
- Frappe Helpdesk base features
- Custom workflows

---

**READY TO BUILD!** 🚀
