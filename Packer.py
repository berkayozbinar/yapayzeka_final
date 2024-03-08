from Node import Node, Rect

class Packer():
    def __init__(self, minW: int, minH: int) -> None:
        self.root = Node((0, 0), (minW, minH))
        self.bounds = (minW, minH)
        self.rects = []

    def nInBounds(self) -> int:
        return sum([r.inbounds for r in self.rects])

    def fit(self, rects: list[Rect]) -> list[Rect]:
        self.rects = rects

        while True:
            self.rects = self._fit(rects)
            return self.rects

    def findNode(self, node: Node, w: int, h: int) -> Node:
        if node.used:
            return self.findNode(node.right, w, h) or self.findNode(node.down, w, h)
        elif w <= node.w and h <= node.h:
            return node
        else:
            return None

    def splitNode(self, node: Node, w: int, h: int) -> Node:
        node.used = True
        node.down = Node(origin=(node.x, node.y + h), size=(node.w, node.h - h))
        node.right = Node(origin=(node.x + w, node.y), size=(node.w - w, h))
        return node

class RectanglePacker(Packer):
    def _fit(self, rects: list[Rect]) -> list[Rect]:
        for rect in rects:
            node = self.findNode(self.root, rect.w, rect.h)
            rect.fit = self.splitNode(node, rect.w, rect.h) if node else self.growNode(rect.w, rect.h)
            rect.inbounds = False if self.root.x + self.bounds[0] <= rect.fit.x or self.root.y + self.bounds[1] <= rect.fit.y else True

        return rects

    def growNode(self, w: int, h: int):
        canGrowDown = w <= self.root.w
        canGrowRight = w <= self.root.h
        shouldGrowRight = canGrowRight and (self.root.w + w <= self.root.h)
        shouldGrowDown = canGrowDown and (self.root.h + h <= self.root.w)
        
        if shouldGrowRight:
            return self.growRight(w, h)
        elif shouldGrowDown:
            return self.growDown(w, h)
        elif canGrowRight:
            return self.growRight(w, h)
        elif canGrowDown:
            return self.growDown(w, h)
        else:
            return None

    def growDown(self, w: int, h: int):
        newRoot = Node((0, 0), (self.root.w, self.root.h + h))
        newRoot.used = True
        newRoot.down = Node((0, self.root.h), (self.root.w, h))
        newRoot.right = self.root

        self.root = newRoot
        return self.next(w, h)

    def growRight(self, w: int, h: int):
        newRoot = Node((0, 0), (self.root.w + w, self.root.h))
        newRoot.used = True
        newRoot.down = self.root
        newRoot.right = Node((self.root.w, 0), (w, self.root.h))

        self.root = newRoot
        return self.next(w, h)

    def next(self, w, h):
        node = self.findNode(self.root, w, h)
        return self.splitNode(node, w, h) if node else None