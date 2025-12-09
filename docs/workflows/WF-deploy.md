---
kind: workflow
id: WF-deploy
owner: Unknown
status: active
trigger: push (main), workflow_dispatch
inputs: []
outputs:
  - name: github-pages
    type: deployment
    description: Deployed static site
entrypoints:
  - .github/workflows/deploy.yml
files:
  - .github/workflows/deploy.yml
last_reviewed: 2025-12-09
---

# Deploy to GitHub Pages

This workflow deploys the static dashboard to GitHub Pages whenever changes are pushed to the main branch.

## Purpose

To publish the latest version of the dashboard code and data to the live URL.

## Process

1.  **Trigger**: Push to `main` or manual dispatch.
2.  **Build**: Uploads the root directory as a pages artifact.
3.  **Deploy**: Deploys the artifact to the `github-pages` environment.

## Configuration

- **Permissions**: Requires `pages: write` and `id-token: write`.
- **Concurrency**: Ensures only one deployment runs at a time.
