# Tratamento de Erros

Cenários de erro comuns e como lidar com cada um.

## PDF protegido por senha

**Sintoma:** `pdfplumber` ou `pypdf` lançam exceção de senha.

**Ação:** Informar o usuário e pedir a senha. Exemplo:
> "Este PDF está protegido por senha. Poderia me informar a senha para que eu consiga extrair o texto?"

## PDF escaneado (sem texto selecionável)

**Sintoma:** `pdfplumber` retorna texto vazio ou com menos de 200 caracteres.

**Ação:** O script `extract_pdf.py` já faz fallback para OCR automaticamente. Se o OCR também falhar ou retornar texto de baixa qualidade, avisar o usuário:
> "O PDF parece ser uma imagem escaneada e o OCR não conseguiu extrair o texto com qualidade suficiente. Poderia enviar uma versão do PDF com texto selecionável?"

## Link inacessível (paywall ou restrição)

**Sintoma:** `web_fetch` retorna erro 403/401 ou conteúdo incompleto (só abstract).

**Ação:** Informar o usuário:
> "Não foi possível acessar o conteúdo completo deste artigo (provavelmente está atrás de um paywall). Você poderia baixar o PDF e enviá-lo diretamente?"

Se apenas o abstract estiver disponível, oferecer:
> "Consegui acessar apenas o abstract. Deseja que eu gere um resumo baseado nele, ou prefere enviar o PDF completo?"

## Artigo em idioma não reconhecido

**Sintoma:** Texto extraído está em idioma diferente de inglês ou português.

**Ação:** Informar e prosseguir:
> "O artigo parece estar em [idioma]. Vou gerar o resumo em português brasileiro mesmo assim, traduzindo o conteúdo."

## Texto extraído corrompido ou muito curto

**Sintoma:** Texto com caracteres estranhos, layout quebrado, ou menos de 500 caracteres após extração.

**Ação:** Avisar o usuário:
> "O texto extraído do PDF está fragmentado/corrompido. Poderia verificar se o arquivo está íntegro ou enviar outra versão?"

## Artigo sem estrutura padrão

**Sintoma:** O texto não possui seções claras como Introdução, Metodologia, Resultados.

**Ação:** Adaptar o template do resumo ao conteúdo real do artigo. Nem todos os artigos seguem a estrutura IMRaD. Artigos de revisão, position papers e surveys podem ter organizações diferentes. Manter as seções do template que fizerem sentido e adaptar ou omitir as demais.

## Arquivo não é PDF

**Sintoma:** O arquivo enviado tem extensão diferente (`.doc`, `.epub`, etc.) ou é um PDF inválido.

**Ação:** Informar o usuário:
> "O arquivo enviado não parece ser um PDF válido. Poderia verificar o formato e enviar novamente como PDF?"
