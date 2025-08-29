# 📘 Ściąga: Struktury danych w Pythonie
## Struktura	Cechy	Kiedy używać	Kiedy unikać	Przykład kodu
###  list	Dynamiczna tablica, zachowuje kolejność, indeksowana	Gdy potrzebujesz sekwencji, iteracji, dostępu po indeksie	Gdy często usuwasz/wstawiasz na początku listy (O(n))	nums = [1,2,3]; nums.append(4); nums[0]
### dict	Klucze → wartości, od Pythona 3.7 zachowuje kolejność wstawiania	Gdy potrzebujesz mapy/lookup (O(1) średnio)	Gdy potrzebujesz wielu duplikatów tego samego klucza	d = {"a":1,"b":2}; d["a"]
### set	Unikalne elementy, brak duplikatów, operacje matematyczne	Gdy musisz sprawdzać przynależność (O(1)) lub eliminować duplikaty	Gdy kolejność ma znaczenie	s = {1,2,3}; 2 in s; s.add(4)
### tuple	Niezmienna lista (immutable), hashowalna	Gdy dane mają być stałe (np. klucze w dict, zwracanie wielu wartości)	Gdy trzeba modyfikować zawartość	t = (1,2,3); x,y,z = t
### deque (z collections)	Dwustronna kolejka, szybkie dodawanie/usuwanie z obu stron	Gdy implementujesz kolejkę FIFO, bufor przesuwający	Gdy potrzebujesz losowego dostępu po indeksie (wolniej niż list)	from collections import deque; dq = deque([1,2]); dq.appendleft(0)
### stack (list/deque)	Zasada LIFO (Last-In-First-Out)	Gdy implementujesz np. undo, DFS, parsowanie nawiasów	Gdy kolejność FIFO jest kluczowa (lepsze deque)	stack=[]; stack.append(1); stack.pop()