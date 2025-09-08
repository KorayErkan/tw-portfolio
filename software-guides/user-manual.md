# Product User Manual (SaaS)

**Author:** Koray Erkan (portfolio sample)
**Version:** 0.1 — <update date here>

---

## About This Manual

- **Product name**: _ACME Cloud_ (fictional SaaS product for demonstration)
- **Audience**: End-users and workspace administrators
- **Assumptions**: Active account with workspace access and modern web browser

---

## Getting Started

1. **Sign in**
   Navigate to https://acmecloud.example and authenticate with your credentials.
   ![Screenshot: Sign-in page](images/sign-in-placeholder.png)

2. **Create your first project**
   From the dashboard, select **New Project**. Provide a descriptive name and optional details.

3. **Invite teammates**
   Use the **Invite** function to add collaborators via email addresses.

4. **Complete onboarding checklist**
   Follow the guided setup wizard to configure essential workspace preferences.

> 💡 **Tip:** Bookmark the dashboard for faster access.

```graphviz
// user-onboarding-flow.dot
digraph G {
  graph [rankdir=TB, splines=true, bgcolor="transparent", nodesep=0.7, ranksep=0.8];
  node  [shape=rounded, style="filled,rounded", fillcolor="#161b22", color="#30363d", fontcolor="#c9d1d9", penwidth=1.2];
  edge  [color="#8b949e", arrowsize=0.9, penwidth=1.3];

  start [label="Sign In", shape=ellipse, fillcolor="#0d1117", penwidth=1.6];
  project [label="Create First Project"];
  invite [label="Invite Teammates"];
  checklist [label="Complete Onboarding\nChecklist"];
  ready [label="Ready to Use", shape=ellipse, fillcolor="#238636", fontcolor="#ffffff"];

  // Decision points
  has_team [label="Working with\na team?", shape=diamond, fillcolor="#d29922"];
  
  start -> project;
  project -> has_team;
  has_team -> invite [label="Yes"];
  has_team -> checklist [label="No"];
  invite -> checklist;
  checklist -> ready;

  // Parallel activities
  shortcuts [label="Learn Shortcuts\n(Ctrl+K / Cmd+K)", style=dotted];
  ready -> shortcuts [style=dotted, arrowhead=none];
}
```

---

## Core Workflows

### Create & Assign Tasks

1. Access your project workspace.
2. Select **+ Task** and define title, description, and deadline.
3. Assign ownership to a team member.
4. Confirm creation.

![Screenshot: New task dialog](images/new-task-placeholder.png)

### Track Progress & Dashboards

- Access **Dashboards** via primary navigation.
- Apply filters by **status**, **assignee**, and **priority**.
- Generate CSV or PDF reports for stakeholder distribution.

---

## Tips & Shortcuts

- Press `Ctrl + K` (Windows) / `Cmd + K` (Mac) for universal search.
- Leverage **saved views** for standardized reporting.
- Perform bulk operations by multi-selecting task rows.

---

## FAQs

**Q: Can I reset my password without contacting support?**
A: Yes. Use **Forgot Password** on the sign-in page.

**Q: How do I change my workspace name?**
A: Go to **Settings → Workspace → General**.

**Q: Is there a mobile app?**
A: Not yet, but the web app is fully responsive.

---

## Glossary

- **Workspace** — A shared environment containing projects and users.
- **Project** — A collection of tasks, milestones, and dashboards.
- **Admin** — A role with elevated permissions (invite/manage users, configure settings).
