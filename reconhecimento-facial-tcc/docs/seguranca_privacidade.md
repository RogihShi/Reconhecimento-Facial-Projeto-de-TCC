# Segurança, privacidade e dados biométricos

Este projeto envolve reconhecimento facial, portanto as imagens dos participantes devem ser tratadas como dados biométricos sensíveis.

## 1. O que não deve ser publicado

Não publique no GitHub:

- fotos reais dos participantes;
- vídeos de teste;
- imagens de cadastro;
- imagens de ataques por foto ou vídeo contendo rostos reais;
- arquivos com nomes completos dos participantes;
- logs que permitam identificar pessoas.

## 2. Como manter a estrutura sem publicar dados

As pastas de dados foram mantidas com arquivos `.gitkeep`. Assim, a estrutura aparece no GitHub, mas sem expor as imagens reais.

## 3. Cuidados com consentimento

Antes de coletar imagens, registre autorização dos participantes para uso acadêmico. Também informe:

- objetivo da coleta;
- onde os dados serão armazenados;
- quem terá acesso;
- por quanto tempo os dados serão mantidos;
- possibilidade de exclusão futura.

## 4. Recomendações práticas

- Armazene imagens reais apenas localmente.
- Use nomes genéricos ou pseudônimos.
- Evite subir arquivos `.zip` contendo imagens.
- Confira o `git status` antes de cada commit.
- Use `.gitignore` para bloquear imagens e vídeos.

## 5. Conferência antes de publicar

Antes de enviar para o GitHub, execute:

```bash
git status
```

E verifique se nenhuma imagem ou vídeo real aparece na lista de arquivos a serem enviados.
