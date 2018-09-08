# Tipos de fork bomb #
- `$ :(){ :|: &};:`
- `fork()`

## Prevenção ##
#### Limitar o número de processos abertos por usuário ####
ulimit: comando responsável por alterar o limites concebidos aos usuário. Ele altera o arquivo `/etc/security/limits.conf` [verificar] adicionando uma nova diretriz delimitadora.

obs: não tem efeito no root ou em qualquer usuário/programa que possu flags `CAP_SYS_ADMIN` ou `CAP_SYS_RESOURCE`

## Ultimo caso ##
`$ ps -ef | grep $PNAME`
`$ exec killall -9 $PNAME`


exec: comando que invoca subprocessos em segundo plano (não traz para o bash)

---

`$ ps -ef | grep 'PID\|pstree'`
`ps -eo ppid --no-header > ps.out; python mypy.py`
`ps -e --no-header | wc -l` número de processos rodando

bash: fork: Resource temporarily unavailable
bash: fork: retry: No child processes
