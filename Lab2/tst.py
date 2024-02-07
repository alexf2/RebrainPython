import re

input2 = 'May 24 14:03:01 ideapad systemid[1]: failed to get session [pid 8279]: Нет доступных данных'

reg = re.compile(
    r'^(?P<date_time>\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}).+(?P<service>\d+[\d+]).+')
grp = reg.search(input2).group
print(grp('date_time'))
print(grp('service'))
print(input2.replace('ideapad', 'PC-12092'))
print(input2.index('failed'))
print(input2.upper().count('S'))
grp = grp('date_time').split(':')
print(
    int(grp[0].split(' ')[-1]) +
    int(grp[1]) +
    int(grp[2])
)


reg = re.compile(
    r'^(?P<date_time>\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2})\s*(?P<name>\w+)\s+(?P<service>\w+\[\d+\]):\s*(?P<msg>[^:]+):\s+(?P<cause>.+)\s*$')

input2 = 'May 24 14:03:01 ideapad colord[844]: failed to get session [pid 8279]: Нет доступных данных'

grp = reg.search(input2).group
date_time = grp('date_time')
name = grp('name')
service = grp('service')
msg = grp('msg') or 'xxx'
cause = grp('cause')

print(f'The PC "{name}" {date_time} receive message from service "{
      service}" what syas "{msg}" because "{cause}"')
