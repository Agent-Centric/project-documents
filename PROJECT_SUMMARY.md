# Project Documents - ZimaOS Home Server

## Overview
This repository serves as a central collection of project documents, configuration notes, and session logs for work performed on a ZimaOS (ZimaCube) home server.

## System Details
- **OS**: ZimaOS v1.4.3
- **Hardware**: ZimaCube (IceWhale Technology)
- **Architecture**: x86_64 / amd64

## Repository Purpose
- Track setup, configuration, and maintenance work done on the server
- Store troubleshooting notes and guides
- Document tooling installations and customizations
- Maintain session logs for reproducibility

## Installed Tools
- **GitHub CLI (gh)** v2.92.0 — installed at `/DATA/Videos/gh`
  - Config: `/DATA/Videos/.gh-config`
  - Git config: `/DATA/Videos/.gitconfig`
- **Git** — system-provided
- **Docker** — available (user is in docker group)

## Environment Notes
Due to ZimaOS filesystem permissions (`/DATA` owned by root), user-writable paths are limited. Tools and configs are stored under `/DATA/Videos/` as a workaround.

Required environment setup for gh/git operations:
```
export PATH="/DATA/Videos:$PATH"
export GH_CONFIG_DIR="/DATA/Videos/.gh-config"
export GIT_CONFIG_GLOBAL="/DATA/Videos/.gitconfig"
```
