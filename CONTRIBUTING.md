# Adding Documents to This Repository

## Prerequisites
Run these before any git/gh commands:
```
export PATH="/DATA/Videos:$PATH"
export GH_CONFIG_DIR="/DATA/Videos/.gh-config"
export GIT_CONFIG_GLOBAL="/DATA/Videos/.gitconfig"
```

## Adding a File

### 1. Place the file in the repo
Copy your document into `/DATA/Videos/project-documents/`:
```
cp /path/to/your-file.md /DATA/Videos/project-documents/
```

For files on another machine, transfer first:
```
scp user@host:/path/to/file.md /DATA/Videos/project-documents/
```

For files in Nextcloud:
```
docker cp nextcloud:/var/www/html/data/<user>/files/<filename> /DATA/Videos/project-documents/
```

### 2. Stage, commit, and push
```
git -C /DATA/Videos/project-documents add -A
git -C /DATA/Videos/project-documents commit -m "Add <brief description>"
git -C /DATA/Videos/project-documents push origin main
```

## Adding a Session Log
Place session logs in the `session-logs/` subdirectory using the naming convention:
```
session-logs/YYYY-MM-DD_short-description.md
```

## Repository Structure
```
project-documents/
├── README.md
├── PROJECT_SUMMARY.md
├── CONTRIBUTING.md
├── session-logs/
│   └── YYYY-MM-DD_short-description.md
└── <other documents>
```
