---
title: Visão geral
---

<div class="cso-hero">
  <span class="cso-eyebrow">Portal em português</span>
  <h1>Observe o ecossistema de ferramentas de IA com evidências.</h1>
  <p>O Claude Skills Observatory organiza conhecimento técnico em catálogos verificáveis, benchmarks reproduzíveis e dashboards voltados à tomada de decisão.</p>
  <div class="cso-actions">
    <a class="cso-button cso-button--primary" href="dashboard/">Abrir dashboard</a>
    <a class="cso-button" href="skills/catalog/">Explorar Skills</a>
  </div>
</div>

## Arquitetura

```mermaid
flowchart LR
    A[Fontes originais] --> B[JSON estruturado]
    B --> C[Scripts de validação]
    C --> D[Documentação gerada]
    C --> E[Dados do portal]
    D --> F[GitHub Pages]
    E --> F
```

## Cobertura inicial

- catálogo inicial de Skills oficiais;
- metodologia e pipeline de benchmarks;
- documentação em inglês e português;
- dashboard responsivo;
- validação e publicação automatizadas.
