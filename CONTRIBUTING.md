# Contribution Guide

---

## Branch Naming Convention

We use a prefix-based naming convention to quickly identify the nature of each change.

### Format
`type/short-description`

* **Type**: The category of the change (see list below).
* **Description**: 2 to 4 keywords in lowercase separated by hyphens.

### Allowed Types
| Type | Usage |
| :--- | :--- |
| `feat/` | A new feature. |
| `fix/` | A bug fix. |
| `docs/` | Documentation changes only. |
| `refactor/` | Code change that neither fixes a bug nor adds a feature. |
| `test/` | Adding missing tests or correcting existing tests. |
| `hotfix/` | Critical fix for the production environment. |

*Example: `docs/update-readme`*

---

## 📝 Commit Messages

We follow the **Conventional Commits** specification. Messages should be concise and descriptive:

`type(scope): short description`

- `feat(ui): add logout button`
- `fix(api): resolve 500 error on auth endpoint`

See [https://www.conventionalcommits.org/](https://www.conventionalcommits.org/) for full specification.

---

## 🛠 Golden Rules
- **No uppercase** in branch names.
- Use **hyphens** `-` exclusively (no spaces or underscores).
- **One commit = one logical task.** Keep it atomic.
