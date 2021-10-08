# Moderation System

## Table of contents
- [General Description](#general-description)
- [Interfaces](#interfaces)
- [Technical Description](#technical-description)
- [Process](#process)
- [Issues](#issues)

## General Description
The moderation system allows certain users ("moderators") chosen by the administrator user to perform various tasks.

## Interfaces
```typescript
interface Action {
  id: string
  account_id: string
  type: string
  categories: string[]
  /**
   * A list of resource `id`s affected by the action.
   */
  entity_ids: string[]
  status: "completed" | "failed" | "reverted"
  created_at: Date
}
```

## Technical Description


## Process

### Moderator
1. When the role of an account changes to `moderator`, the account gets notified of this.
1. The account then can access `/mod` endpoint, which leads to the moderator dashboard. On this page the mod can see various stats, among them is the list of various `tasks`.
1. Each performed `task` results in an `action`.

## Issues
