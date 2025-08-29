"""
Zadanie 2: System kolejkowania zadań wg priorytetu

Napisz funkcję:
def schedule_tasks(tasks: list[tuple[int, str]]) -> list[str]:
    ...

tasks to lista krotek (priority, name), gdzie priority to liczba całkowita (im mniejsza, tym wyższy priorytet).

Funkcja ma zwrócić listę nazw zadań w kolejności ich wykonywania wg priorytetu.

Jeśli kilka zadań ma taki sam priorytet → wykonujemy je w kolejności ich pojawienia się na liście.

Przykłady:

schedule_tasks([(2, "write tests"), (1, "fix bug"), (3, "deploy")])
# ➡ ["fix bug", "write tests", "deploy"]

schedule_tasks([(5, "low"), (1, "high"), (1, "urgent"), (3, "mid")])

💡 Tip: Możesz użyć heapq (min-heap), ale możesz też rozwiązać inaczej — celem jest poczuć różnicę między listą posortowaną a kolejką priorytetową.

⏱ Czas: daj sobie 15 min na pierwsze podejście.
Nie podpowiadam nic więcej — spróbuj sam, a potem wrócimy i pogadamy o złożoności oraz plusach/minusach użycia heapq.

"""
import heapq


def schedule_tasks(tasks: list[tuple[int, str]]) -> list[str]:
    heap = [(priority, index, name) for index, (priority, name) in enumerate(tasks)]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[2] for _ in range(0, len(heap))]
