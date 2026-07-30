---
title: Overview
---

<div class="cso-hero">
  <span class="cso-eyebrow">English portal</span>
  <h1>Observe the AI tool ecosystem with evidence.</h1>
  <p>The Claude Skills Observatory organizes technical knowledge into verifiable catalogs, reproducible benchmarks and decision-ready dashboards.</p>
  <div class="cso-actions">
    <a class="cso-button cso-button--primary" href="dashboard/">Open dashboard</a>
    <a class="cso-button" href="skills/catalog/">Explore Skills</a>
  </div>
</div>

## Architecture

```mermaid
flowchart LR
    A[Upstream sources] --> B[Structured JSON]
    B --> C[Validation scripts]
    C --> D[Generated documentation]
    C --> E[Portal datasets]
    D --> F[GitHub Pages]
    E --> F
```

## Initial coverage

- official starter Skills catalog;
- benchmark methodology and pipeline;
- English and Portuguese documentation;
- responsive dashboard;
- automated validation and deployment.
