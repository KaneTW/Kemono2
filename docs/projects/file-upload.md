# File Upload

## Table of contents
- [Interfaces](#interfaces)
- [Core information](#core-information)
- [Process](#process)
- [Issues](#issues)

## Interfaces
```typescript
interface ManualUpload {}
```

## Core information

## Process
1. The account goes to `/posts/upload`.
2. Uploads the file.
3. The file gets processed.
4. The file gets sent for review to a moderator.
5. The moderator then decides to discard the upload or approve for public view.
6. ...

## Issues
- What happens when one mod approves a file while the other one discards it?
- Unlike DMs the file verification can take very variable amount of time, so there should be separate states for a given upload, like `"pending"`,`"approved"`,`"rejected"`.
