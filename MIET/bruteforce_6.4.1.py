'''
На одну пару (i j) закрываются ячейки:
i     | j
i     | 6 - j
9 - i | j
9 - i | 6 - j

Так как вырезанных ячеек - 15, а всего - 60, то все пары не пересекающиеся
=> i != 9 - i => Не влияет
=> j != 6 - j => j != 3

=> i <= 4
=> j < 3

pairs = set()
for i in range(0, 5):
    for j in range(0, 3):
        if (i, j) not in pairs:
            pairs.add((i,j))
        if (i,6-j) not in pairs:
            pairs.add((i,6-j))
        if (9-i,j) not in pairs:
            pairs.add((9-i,j))
        if (9-i,6-j) not in pairs:
            pairs.add((9-i,6-j))
print(len(pairs), pairs)

field = [
    list('РПТЕШАВЕСЛ'),
    list('ОЯТАЛ-ЬЗТ-'),
    list('-УКТ-ЯАЬ-С'),
    list('НП-ЬЕУ-ШЛС'),
    list('ТИЬЗЫЯЕМ-О'),
    list('-ЕФ--РО-СМ')
]
print(field)
'''
