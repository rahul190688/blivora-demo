# Apex Analytix - Support Ticket Workflow

**Last Updated:** April 20, 2026
**Source:** Rahul Kumar - Internal workflow documentation

---

## 🏢 Organization Structure

### Groups
- **Total Groups:** 20+ internal support groups
- **Each Group:** Has its own set of people/agents
- **Structure:** Departmentalized support teams

### Key Roles
1. **Enterprise Support Team** - First responders, initial customer contact
2. **Support Person** - Assigned per client for ongoing support
3. **Implementation Person** - Assigned per client for implementation issues
4. **Group Members** - Team members within each support group

---

## 📧 Ticket Creation Flow

### Initial Creation
```
1. Client sends email → customer support email address
2. System creates ticket automatically
3. Email parsed for ticket details
```

### Client Mapping (Pre-configured)
```
Each client has:
├── Designated Support Person (primary contact)
├── Designated Implementation Person (for implementation issues)
└── Default Group assignment
```

**Important:** This mapping exists BEFORE ticket creation (configuration/setup)

---

## 🔄 Ticket Assignment Workflow

### Step-by-Step Flow

#### Step 1: Ticket Created (via Email)
```
Status: New
Assigned: None (initially)
Priority: Not set
```

#### Step 2: Enterprise Support Team Response
```
Action: Send initial response to customer
Status: Open
Assigned: Still with Enterprise Support
Priority: Medium (default)
```

**Enterprise Support Team:**
- First responders
- Acknowledge ticket to customer
- Assess initial priority
- Route to appropriate support person

#### Step 3: Assignment to Support Person
```
Action: Route based on client mapping
Status: Medium (default, can be changed)
Assigned: Client's designated Support Person
Group: Client's designated Support Group
```

**Assignment Logic:**
- Look up client in mapping table
- Find designated Support Person
- Auto-assign to that person
- Set default status: Medium

#### Step 4: Status Management
```
Status can be changed by:
├── Enterprise Support Team (during initial triage)
├── Assigned Support Person (while working)
└── Any team member working on ticket
```

**Status Changes Based On:**
- Ticket criticality
- Business impact
- SLA requirements
- Customer priority

---

## 👥 Group Structure

### Group Hierarchy
```
Company (Apex Analytix)
├── Group 1 (e.g., "Finance Support")
│   ├── Team Member 1
│   ├── Team Member 2
│   └── Team Member N
├── Group 2 (e.g., "Technical Support")
│   ├── Team Member 1
│   └── Team Member N
├── Group 3
└── ... (20+ groups total)
```

### Group Responsibilities
- Each group handles specific types of tickets
- Groups have multiple team members
- Tickets assigned to individuals within groups

---

## 🎯 Client-to-Agent Mapping

### Pre-configured Mapping Table
```
Client Name          Support Person       Implementation Person    Default Group
─────────────────────────────────────────────────────────────────────────────
Acme Corporation     John Smith          Jane Doe                 Technical Support
XYZ Industries       Bob Johnson         Alice Brown              Finance Support
ABC Company          Mike Davis          Sarah Wilson             Risk Management
...
```

**Mapping Fields:**
1. Client/Customer Name
2. Designated Support Person (primary agent)
3. Designated Implementation Person (for impl. issues)
4. Default Support Group
5. (Optional) Default Priority
6. (Optional) SLA Level

---

## 📊 Status Values

### Default Status: Medium
**Set when:** Ticket assigned to Support Person after Enterprise Support response

### Status Options (to be defined):
- [ ] New
- [ ] Open
- [ ] Medium (default)
- [ ] High
- [ ] Critical
- [ ] In Progress
- [ ] Waiting on Customer
- [ ] Waiting on 3rd Party
- [ ] Resolved
- [ ] Closed

**NOTE:** Need clarification on exact status values used

---

## 🔴 Criticality Determination

### Who Sets Criticality:
1. **Enterprise Support Team** (during initial triage)
2. **Assigned Support Person** (during work)
3. **Any team member** working on ticket

### Criticality Factors (to be defined):
- [ ] Business impact
- [ ] Number of users affected
- [ ] Revenue impact
- [ ] Compliance/regulatory issues
- [ ] System downtime
- [ ] SLA requirements
- [ ] Customer contract level

---

## 🚀 Implementation Requirements for POC

### Must Build:

#### 1. Client-Agent Mapping System
**DocType:** `Blivora Client Mapping`

Fields:
- Client (Link to Customer)
- Support Person (Link to User)
- Implementation Person (Link to User)
- Default Group (Link to Team)
- Default Priority (Select)
- SLA Level (Select)

#### 2. Enterprise Support Team
**Role/Team:** `Enterprise Support`

Capabilities:
- See all new tickets
- Send initial customer response
- Assign to support person (auto or manual)
- Set initial priority

#### 3. Auto-Assignment Logic
**Trigger:** After Enterprise Support responds

Process:
```python
1. Check client name on ticket
2. Look up client in mapping table
3. Find designated Support Person
4. Auto-assign ticket to that person
5. Set status to "Medium"
6. Notify assigned person
```

#### 4. Group Management
**Use Existing:** HD Team (Frappe Helpdesk)

Configure:
- 20+ teams/groups
- Team members for each
- Team-based permissions

#### 5. Status Workflow
**Custom Field:** Internal Team Status

Values:
- New → Open → In Progress → Resolved → Closed
- With intermediate states (Waiting, etc.)

---

## ❓ Questions for Clarification

### **1. Exact Status Values**
What are ALL the status options you use?
- New, Open, In Progress, Resolved, Closed?
- What about "Waiting on Customer", "Escalated", etc.?

### **2. Priority vs Status**
- Priority: Low, Medium, High, Critical?
- Status: Different from priority, right?
- Or is "Medium" a priority level?

### **3. Enterprise Support Team**
- Is this a specific team/group?
- Or a role that multiple people have?
- Who are the members?

### **4. Group Names**
Can you list the 20+ groups? Or at least the main ones:
- Technical Support
- Finance Support
- Risk Management
- Implementation Team
- ...?

### **5. Criticality Rules**
What makes a ticket "Critical" vs "High" vs "Medium"?
- Specific criteria?
- Or agent judgment?

### **6. Client Mapping**
- How many clients in total?
- Is one support person per client? Or can be multiple?
- What if client has multiple contracts/products?

### **7. Email Parsing**
- Does email subject determine anything?
- Any special email formats/tags?
- How do you identify the client from email?

---

## 📝 Next Steps

1. **Clarify status values** (what are they exactly?)
2. **List main groups** (at least top 10-15)
3. **Define criticality rules** (what determines priority?)
4. **Build client mapping system**
5. **Configure auto-assignment**
6. **Set up Enterprise Support workflow**

---

## 💡 POC Demo Scenario

**Sample Ticket Flow:**
```
1. Email arrives from: vendor.inquiry@acmecorp.com
2. System creates ticket
3. Enterprise Support sees new ticket
4. Enterprise Support sends: "Thank you, we're looking into this"
5. System checks mapping: Acme Corp → John Smith (Support)
6. Auto-assign to John Smith
7. Status set to: Medium
8. John works on ticket, changes status as needed
9. Resolved → Closed
```

**This demonstrates:**
- ✅ Email-based creation
- ✅ Enterprise Support first response
- ✅ Auto-assignment via mapping
- ✅ Default status (Medium)
- ✅ Status workflow
- ✅ Group-based organization

---

**CRITICAL for POC:** Client-to-Agent mapping is the KEY differentiator!
