# Skills Catalog Architecture

## Purpose

The catalog stores auditable metadata about Agent Skills without copying entire upstream implementations.

## Origin taxonomy

| Value | Meaning |
|---|---|
| `official` | Published by Anthropic in an official repository |
| `partner` | Published by an identified software or platform partner |
| `community` | Published by an independent community maintainer |
| `custom` | Created for the Observatory or a documented organization |
| `research` | Experimental or academic implementation |

## Status taxonomy

| Value | Meaning |
|---|---|
| `verified` | Source path and metadata checked |
| `review` | Record exists but needs editorial verification |
| `draft` | Incomplete record |
| `deprecated` | Upstream has deprecated the skill |
| `archived` | Retained for historical reference |

## Licensing

The Observatory records licensing information but does not relicense third-party content. Document Skills may be source-available under proprietary upstream terms, while other skills can have different terms. Always consult the upstream repository.

## Required evidence

A verified record must contain:

- source repository;
- source path;
- source URL;
- source blob SHA;
- verification date;
- licensing notice.
