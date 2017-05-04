Para rodar o preditor, simplesmente o execute com `python3 preditor.py`.

Ao executar o preditor, caso os modelos (`models/2-gram` e `models/3-gram`) não existam, eles serão gerados. O número de documentos usados para treino está definido no código-fonte (procurar por `n_datasets=15`), e por padrão são 15. Os documentos utilizados para treino são obras do Machado de Assis e se encontram no diretório `dataset/critica`.

Uma vez gerados os modelos, o preditor estará pronto para uso. Basta digitar a primeira palavra para começar a receber as predições e suas probabilidades.