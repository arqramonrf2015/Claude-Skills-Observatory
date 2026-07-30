# Publicação rápida

Este ZIP já está organizado para ser enviado diretamente para a raiz do repositório:

`arqramonrf2015/Claude-Skills-Observatory`

## Método recomendado no Windows

1. Extraia este ZIP.
2. Abra o terminal na pasta extraída.
3. Execute:

```powershell
git init
git branch -M main
git remote add origin https://github.com/arqramonrf2015/Claude-Skills-Observatory.git
git add .
git commit -m "release: publish Claude Skills Observatory v0.1.0"
git push -u origin main
```

Se o repositório remoto já possuir um README:

```powershell
git pull origin main --allow-unrelated-histories
git add .
git commit -m "release: publish Claude Skills Observatory v0.1.0"
git push -u origin main
```

Depois, no GitHub:

1. Abra **Settings → Pages**.
2. Em **Source**, selecione **GitHub Actions**.
3. Abra **Actions** e acompanhe `Deploy documentation`.
