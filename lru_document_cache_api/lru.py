import datetime
from typing import List, Dict


class Node:
    def __init__(self, doc_id: str, content: str | None = None, updated_at: str | None = None):
        self.doc_id = doc_id
        self.content = content
        self.updated_at = updated_at
        self.next = None
        self.prev = None

    @property
    def to_dict(self) -> dict:
        return {'doc_id': self.doc_id, 'content': self.content, 'updated_at': self.updated_at}


class LruDocument:
    
    def __init__(self):
        self._map: dict[str, Dict[str, Node]] = {}
        self._head: dict[str, Node | None] = {}
        self._tail: dict[str, Node | None] = {}
        self._size: dict[str, int] = {}
        self._capacity: dict[str, int] = {}

    def get_doc(self, user: str, doc_id: str) -> Dict[str, str] | None:
        self._ensure_user(user)
        node = self._map[user].get(doc_id)
        if not node:
            return None
        
        self._push_head(user, node)

        return node.to_dict

    def get_docs(self, user: str) -> List[Dict[str, str]]:
        self._ensure_user(user)
        node = self._head.get(user)
        docs = []
        if node:
            docs.append(node.to_dict)
        while node:
            next_node = node.next
            if next_node:
                docs.append(next_node.to_dict)
            node = next_node

        return docs

    def cache(self, user: str, doc_id: str, content: str) -> None:
        self._ensure_user(user)
        node = self._map[user].get(doc_id)
        if not node:
            self._size[user] += 1

        node = self._update_doc(user, doc_id, content)

        self._push_head(user, node)

        if self._size[user] > self._capacity[user]:
            self._pop_tail(user)

    def set_capacity(self, user: str, capacity: int):
        self._ensure_user(user)
        self._capacity[user] = capacity

        size = self._size.get(user, 0)
        if size == 0:
            self._size[user] = 0

        while self._size[user] > capacity:
            node = self._pop_tail(user)
            if not node:
                break
    
    def get_size(self, user: str):
        return self._size[user]
    
    def _push_head(self, user: str, node: Node) -> None:
        head = self._head.get(user)
        if head:
            head.prev = node
            next_node = node.next
            prev_node = node.prev
            if next_node and not head.next:
                head.next = next_node
                next_node.prev = head
            elif next_node and prev_node:
                next_node.prev = prev_node
                prev_node.next = next_node
            elif not next_node and prev_node:
                prev_node.next = None
            
            node.next = head
            node.prev = None
            
            if not head.next:
                self._tail[user] = head
        else:
            self._tail[user] = node
        self._head[user] = node

    def _update_doc(self, user, doc_id, content) -> Node:
        node = self._map[user].get(doc_id)
        if not node:
            node = Node(doc_id)
        node.content = content
        node.updated_at = str(datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z")

        self._map[user][doc_id] = node
        return node
    
    def _pop_tail(self, user: str) -> Node | None:
        tail = self._tail.get(user)
        if not tail:
            return None
        
        new_tail = tail.prev
        if new_tail:
            new_tail.next = None
        else:
            self._head[user] = None
        self._tail[user] = new_tail
        self._size[user] -= 1
        del self._map[user][tail.doc_id]
        return tail
    
    def _ensure_user(self, user: str) -> None:
        if user not in self._map:
            self._map[user] = {}
            self._head[user] = None
            self._tail[user] = None
            self._size[user] = 0
            self._capacity[user] = 3  # domyślnie
