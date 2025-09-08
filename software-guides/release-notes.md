# Release Notes / Changelog Template

**Author:** Koray Erkan (portfolio sample)
**Version:** 0.1 — <update date here>

---

## How to Use

- Keep entries **task-oriented** and **impact-oriented**.
- Provide *upgrade notes*, *breaking changes*, and *deprecations* up front.
- Use consistent tags or icons for clarity (✨ New, ⚡ Improved, 🐛 Fixed, 🛡️ Security).

---

## 2025-09-08 (v1.8.0)

### Highlights

- ✨ **New:** Project templates gallery
- ⚡ **Improved:** Report exports now 30% faster
- 🛡️ **Security:** SSO enforcement required for all admins

### Breaking Changes

- None in this release

### Details

- Added `/v2/reports` batch endpoint
- Improved CSV import error messages
- Fixed timezone handling in dashboards

### Upgrade Notes

- `GET /v1/reports` deprecated (removal in 90 days) → use `/v2/reports`

---

## 2025-08-15 (v1.7.2)

### Highlights

- 🐛 Bugfix rollup release

### Details

- Fixed duplicate notifications in activity feed
- Corrected billing invoice rounding issues
- Patched minor XSS vulnerability in dashboard filters

### Upgrade Notes

- No action required
