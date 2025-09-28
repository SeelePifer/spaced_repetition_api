# GitHub Actions y Codecov

## Problema con Rate Limiting

El workflow principal (`test.yml`) puede fallar con el error:

```
429 - {"message":"Rate limit reached. Please upload with the Codecov repository upload token to resolve issue. Expected time to availability: 2882s."}
```

## Soluciones

### 1. Usar el Workflow Alternativo (Recomendado)

Si tienes problemas con Codecov, puedes usar el workflow alternativo:

```yaml
# Renombrar el archivo principal
mv .github/workflows/test.yml .github/workflows/test-with-codecov.yml

# Activar el workflow sin Codecov
mv .github/workflows/test-no-codecov.yml .github/workflows/test.yml
```

### 2. Configurar Token de Codecov (Para Repositorios Privados)

Si tienes un repositorio privado, puedes configurar un token de Codecov:

1. Ve a [codecov.io](https://codecov.io)
2. Conecta tu repositorio
3. Obtén el token del repositorio
4. Agrega el token como secret en GitHub:
   - Ve a Settings > Secrets and variables > Actions
   - Agrega un nuevo secret llamado `CODECOV_TOKEN`
5. Actualiza el workflow:

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    file: ./coverage.xml
    flags: unittests
    name: codecov-umbrella
    fail_ci_if_error: false
    verbose: true
```

### 3. Deshabilitar Codecov Temporalmente

Si quieres deshabilitar Codecov temporalmente, puedes comentar la sección:

```yaml
# - name: Upload coverage to Codecov
#   uses: codecov/codecov-action@v3
#   with:
#     file: ./coverage.xml
#     flags: unittests
#     name: codecov-umbrella
#     fail_ci_if_error: false
#     verbose: true
```

## Archivos de Cobertura

Los reportes de cobertura se generan en:

- `htmlcov/` - Reporte HTML interactivo
- `coverage.xml` - Reporte XML para Codecov

Puedes descargar estos archivos como artifacts del workflow de GitHub Actions.

## Comandos Locales

Para ejecutar los mismos comandos localmente:

```bash
# Tests principales
python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

# Tests de performance
python -m pytest tests/performance/ -v -m "slow" --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=24

# Ver reporte HTML
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```
