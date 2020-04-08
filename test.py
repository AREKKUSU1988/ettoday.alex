a=[1,2,3,4,5,6,7,7,5,8,2,2,2,2,2]
for x in range(0,-1,-1):
    print(x)


_cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
values = [None, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
value_map = zip(_cards, values)
print(list(value_map))

# value_map = {k: v for k, v in zip(_cards, values)}
# total = sum([value_map[card] for card in hand if card != 'A'])
print(a.count(2))


