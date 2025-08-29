# 2. Unikalne elementy
# Napisz funkcję unique_elements(nums: list[int]) -> list[int], która zwróci listę elementów, które występują w nums dokładnie raz.
# Przykład:
# unique_elements([1,2,2,3,4,4,5])  
# [1, 3, 5]
from collections import Counter
from typing import List


def unique_elements(nums: List[int]) -> List[int]:
    counter = Counter(nums)
    return [
        num
        for num in nums
        if counter[num] == 1
    ]
