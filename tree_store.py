from typing import Optional


class Node:
    def __init__(self, id_: int, type_: Optional[str]):
        self.__id: int = id_
        self.parent: Optional["Node"] = None
        self.children: list["Node"] = []
        self.type_: Optional[str] = type_

    @property
    def id(self) -> int:
        return self.__id

    def dict(self) -> dict:
        """
        Возвращает данные узла в виде словаря.
        """

        if not self.parent:
            return {"id": self.id, "parent": "root"}
        return {"id": self.id, "parent": self.parent.id, "type": self.type_}

    def addChild(self, child: "Node") -> None:
        """
        Добавляет новый дочерний узел к текущему.
        :param child: Node
        :return: None
        """
        child.parent = self
        self.children.append(child)


class TreeStore:
    def __init__(self, items: list[dict]):
        """

        :param items: [
            {"id": 1, "parent": "root"},
            {"id": 2, "parent": 1, "type": "test"},
            {"id": 4, "parent": 2, "type": "test"},
            {"id": 5, "parent": 2, "type": "test"},
            {"id": 7, "parent": 4, "type": None},
        ]
        """

        self._tree = {}
        root = items.pop(0)
        self._head = Node(root["id"], None)
        self._tree[root["id"]] = self._head

        for item in items:
            parent = self._getNode(item["parent"])
            child = Node(item["id"], item["type"])
            parent.addChild(child)
            self._tree[item["id"]] = child

    def getAll(self) -> list[dict]:
        """
        Возвращает список всех элементов
        """
        return [item.dict() for item in self._tree.values()]

    def getItem(self, id_: int) -> Optional[dict]:
        """
        Возвращает объект элемента по id.

        :param id_: id элемента.
        :return:
                Данные элемента в виде словаря (dict)
        """

        item = self._tree.get(id_)
        if item:
            return item.dict()

    def getChildren(self, id_: int) -> list[dict]:
        """
        Возвращает ближайших потомков элемента.
        Если потомков нет, вернется пустой список - [].

        :param id_: id элемента, детей которого, нужно вернуть.
        :return: Список элементов.
        """

        item = self._getNode(id_)
        return [i.dict() for i in item.children]

    def getAllChildren(self, id_: int) -> list[dict]:
        """
        Возвращает список всех дочерних элементов.
        Если дочерних элементов нет, вернется пустой список - [].

        :param id_: id элемента, детей которого, нужно вернуть.
        :return: Список элементов.
        """

        item = self._getNode(id_)
        return self._getAllChildren(item)

    def getAllParents(self, id_) -> list[dict]:
        """
        Возвращает список цепочки родительских элементов,
        начиная от самого элемента, чей id был передан в аргументе и до корневого элемента.

        :param id_: id элемента, родителей которого, нужно вернуть.
        :return: Список родителей
        """

        item = self._getNode(id_)
        parents = []
        while item.parent:
            item = item.parent
            parents.append(item.dict())

        return parents

    def _getNode(self, id_: int) -> Node:
        return self._tree[id_]

    def _getAllChildren(self, node: Node) -> list[dict]:
        if not node:
            return []
        children = []
        for child in node.children:
            children.append(child.dict())
            children.extend(self._getAllChildren(child))

        return children


if __name__ == "__main__":
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]

    ts = TreeStore(items)

    print(ts.getAllParents(7))
