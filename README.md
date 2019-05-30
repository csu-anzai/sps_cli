### SPS/FUP CLI Scrips ###

Este projeto consiste em um conjunto de Scripts/Ferramentas para o uso no cotidiano da Assitência Estudantil da UnB. Estes permitem realizar registros de atendimentos, reaver informações armazenadas, grava-lás em arquivos de saída e enviá-las facilmente via email pelo terminal.

Estas ferramentas foram concebidas para trabalharem de forma integrada com o Bash, tendo sido testadas e desenvolvidas a partir de uma versão básica do Debian. O objetivo é fornecer uma ferramenta prática e funcional para lidar com as demandas e necessidades cotidianas do trabalho sem exigir muito tempo de desenvolvimento, manutenção e correção de erros.

Para gestão dos profissionais, aproveitamos os recursos do próprio sistema operacional e do openssh que permite um ambiente multitarefa integrado. A ideia é que as ferramentas sejam instaladas em uma máquina virtual e que os acessos sejam efetuados por cada profissional a partir de sua própria estação de trabalho.

Os dados, no momento, estão sendo estruturados em arquivos de texto no formato JSON.

### Dependências ###

## Python ##

- docopt
- colored

sudo pip3 install docopt colored

## Base do sistema ##

- rclone

