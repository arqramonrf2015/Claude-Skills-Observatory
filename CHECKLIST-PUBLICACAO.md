# Checklist Final de Publicação

## Antes do envio

1. Execute `AUDITAR-PROJETO.cmd`.
2. Execute `PREVIEW-LOCAL.cmd`.
3. Abra as páginas principais.
4. Confira o catálogo de Skills.
5. Confira o dashboard de benchmarks.
6. Confirme que dados sintéticos estão identificados.
7. Verifique se não existem tokens ou credenciais no projeto.

## Envio ao GitHub

1. Execute `PUBLICAR-AGORA.cmd` na raiz da Entrega 11/12.
2. Autorize a GitHub CLI no navegador.
3. Aguarde o commit e o push.
4. Abra a aba **Actions** do repositório.
5. Confirme que `Quality audit` e o workflow de Pages estão verdes.

## Depois da publicação

1. Abra o endereço do GitHub Pages.
2. Teste desktop e smartphone.
3. Teste busca, tema e navegação.
4. Crie a tag `v0.1.0`.
5. Publique as notas de versão de `RELEASE-v0.1.0.md`.

## Reversão

Em caso de falha grave:

```bash
git log --oneline
git revert <SHA_DO_COMMIT>
git push origin main
```

Não utilize `git push --force` na branch `main`.
