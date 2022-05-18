# Atrapalhar fraudes pelo WhatsApp
Este projeto consiste na automatização de ações pelo WhatsApp. Ele foi desenvolvido com o intuito de lidar com o recebimento massivo de spam pelo whatsapp por meio de contas clonadas. Grupos hackers clonam contas e as utilizam com bots para propagação de fraudes e vírus sem que o verdadeiro dono da conta saiba o que ocorreu. Dessa forma, esse algoritmo automatiza ações no whatsapp para ajudar as vítimas sobre como proteger melhor seus perfis e possui também uma função para envio de mensagens em massa para o contato principal do grupo de fraude.

## Processos
O algoritmo possui dois processos principais:

- Enviar mensagens para vítimas propagadoras de spam
Esse processo consiste em percorrer todas as conversas ativas do whatsapp procurando por números desconhecidos e para cada um destes, verificar se a última mensagem é um spam. Caso positivo, são enviadas mensagens de advertência sobre o ocorrido e um link de um vídeo no YouTube explicando como ativar a verificação de duas etapas e ajudá-los a protegerem suas contas.
A verificação do spam é feita utilizando a mensagem de spam recebida através dos contatos clonados, basicamente consiste em verificar se as palavras-chaves da última mensagem da conversa corresponde a mais de 85% das palavras-chaves da mensagem padrão utilizada no spam.

- Enviar mensagens em massa para contato principal de fraude
Esse processo consiste em pesquisar no whatsapp por uma conversa ou pelo contato de fraude salvo e então iniciar o envio de mensagens em massa. O objetivo desse processo é enviar milhares de mensagens para atrapalhar o bot ou pessoa que está por trás desse contato. As mensagens enviadas são obtidas do script do filme "SHREK" (achei a ideia de utiliza o do Shrek bem divertida, sinta-se livre pra escolher o seu!), são 2265 mensagens (1 para cada linha) que podem ser repetidas de acordo com a configuração do algoritmo.

## Tecnologias utilizadas

Nesse projeto foi utilizado Python com Selenium e NLTK.

## Executando

- Clone o projeto para seu computador;
- Acesse a pasta do projeto;
- Instale as bibliotecas utilizadas:
    ```
    $ pip install selenium nltk
    ```
- Escolha o processo a ser executado:
    1. Enviar mensagens para vítimas:
        - Modifique a variável *msg_fraud* no arquivo *manager_whats.py* linha 28 para conter a mensagem de spam que você tenha recebido. Essa mensagem é importante pois é através dela que o algoritmo verifica se a última mensagem de uma conversa do whatsapp é a mensagem de fraude.
        ```
        $ python3 manager_whats.py --type 1 --message "Olá\nVocê me enviou mensagens de spam!"
        ```
        O parâmetro `message` não é obrigatório, caso ele não seja enviado, será utilizada a mensagem padrão apresentada abaixo:
        
        >Olá\nNo dia X a tarde você me enviou mensagens de spam oferecendo emprego com um link para o contato de fraude. Seu whatsApp provavelmente foi clonado por algum golpista que utilizou para enviar essas mensagens, acredito que não apenas para mim. \nQueria te recomendar que proteja sua conta de whatsApp ativando a verificação em dois fatores, dessa forma eles não podem mais acessar o seu número. Vou enviar um tutorial de como fazer isso:\n https://www.youtube.com/watch?v=SpCONE_gYKE\n Tenha uma bom dia e se cuide!
        
        A cada `\n` o texto é separado e enviado como mensagens diferentes.

    2. Enviar menssagens para contato principal de fraude:

        ```
        $ python3 manager_whats.py --type 2 --contact "Golpista" --messages_number 5
        ```
        O parâmetro `contact` é obrigatório para esse processo e pode ser o nome do contato golpista (caso você tenha salvo) ou o número (+55 99 9999-9999). O parâmetro `messages_number` é referente a quantidade de vezes que você deseja repetir o processo (geralmente o golpista não suporta que você atrapalhe ele por muito tempo, ele bloqueia você XD).

