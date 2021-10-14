# Title

## Table of contents
- [General Description](#general-description)
- [Interfaces](#interfaces)
- [Technical Description](#technical-description)
- [Issues](#issues)

## General Description
The key management panel simply needs to show the user information on the keys they have saved (service + added time,) a list of import logs for those keys, an indication if that key is "dead"as well, as a button to "revoke" permissions, which deletes the key from the database.

## Interfaces

```typescript
interface ServiceKey {
  id: number
  service: string
  discord_channel_ids?: string
  encrypted_key: string
  added: Date
  dead: boolean
  contributor_id: number
}
```

```python
@dataclass
class Service_Key:
    id: int
    service: str
    discord_channel_ids: Optional[str]
    encrypted_key: str
    added: datetime
    dead: bool
    contributor_id: int
```
## Technical Description
## Issues
