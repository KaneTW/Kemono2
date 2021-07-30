# Direct Messages

## Table of contents
- [Interfaces](#interfaces)
- [The process](#the-process)
- [Issues](#issues)

## Interfaces
```typescript
interface DirectMessage {
  id: string
  user: string
  service: string
  content: string
  added: Date | string
  published: Date | string
  embed: {}
  file: {}
}

interface DirectMessageUnapproved extends DirectMessage {
  import_id: string
}
```
Using typescript because of its simple interface syntax.

## The Process
The user: 
1. Goes to `/importer`.
2. Checks the "allow DMs" box and submits the results
3. This allows the archiver to collect DMs along the way.
4. Gets responded with `success.html` template with a redirect to import status page.
5. The status page then checks for `dms` search query to inform about unapproved DMs and gives a link to `/importer/dms/<import_id>`.
6. This page shows a list of DMs which need approval.
7. The IDs of approved DMs are sent to the `POST` `/importer/dms/<import_id>`, the rest are discarded.
8. Approved DMs then appear at `GET` `/<service>/user/<artist_id>/dms`.

## Issues
- No safety checks.

  All of this stuff seems to be public, and relying on URL to notify about unapproved DMs is kinda sketchy. DM imports should require an account.

- DM duplication. 

  The DM `id` is most likely local to the user importing the stuff and thus a similar DM will have a different ID if imported by another user.

- Approval confilcts

  Suppose the way to resolve ID duplication is in place, how are the approvals of "same" DM resolved between different importers?

- Doxxx

  Outside of obvious post content being an easy way to doxxx both the importer and the artist, there are less obvious markers which can be used by the artist, such as ID and timestamps. The problem is worse if DMs are going to get included in the dump.

- Unapproved DMs piling up.

  There is probably going to be at least 1 unapproved DM per importer, which means an evergrowing number of unapproved DM entries piling up in database. An explicit "reject" action for DMs, which removes the DM from database and adds its ID to some account-bound list of exclusions will alleviate this issue, on top of not showing them again in the approval list for the importing user.

- Unapproved DMs getting reimported

  This makes them reappear in the DM approval list and the server throws an error upon approval of previously discarded DMs, thus piling up them in DM approval page too.
