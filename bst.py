from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def inorder(root):
    if root:
        inorder(root.left)
        print(root.value, end=' ')
        inorder(root.right)


def preorder(root):
    if root:
        print(root.value, end=' ')
        preorder(root.left)
        preorder(root.right)


def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.value, end=' ')


def level_order(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.value, end=' ')
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def height(root):
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def search_bst(root, val):
    if root is None or root.value == val:
        return root
    if val < root.value:
        return search_bst(root.left, val)
    return search_bst(root.right, val)


def insert_bst(root, val):
    if root is None:
        return Node(val)
    if val < root.value:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    return root


def find_min(root):
    while root.left:
        root = root.left
    return root


def delete_node(root, val):
    if root is None:
        return root

    if val < root.value:
        root.left = delete_node(root.left, val)
    elif val > root.value:
        root.right = delete_node(root.right, val)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        temp = find_min(root.right)
        root.value = temp.value
        root.right = delete_node(root.right, temp.value)

    return root

class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None


class ContactDirectory:
    def __init__(self):
        self.root = None

    def insert(self, root, name, phone):
        if root is None:
            return Contact(name, phone)
        if name < root.name:
            root.left = self.insert(root.left, name, phone)
        elif name > root.name:
            root.right = self.insert(root.right, name, phone)
        else:
            root.phone = phone
        return root

    def search(self, root, name):
        if root is None or root.name == name:
            return root
        if name < root.name:
            return self.search(root.left, name)
        return self.search(root.right, name)

    def find_min(self, root):
        while root.left:
            root = root.left
        return root

    def delete(self, root, name):
        if root is None:
            return root

        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.find_min(root.right)
            root.name = temp.name
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)

        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(f"Name: {root.name}, Phone: {root.phone}")
            self.inorder(root.right)


if __name__ == "__main__":

    #BST
    print("=== BST with Numbers ===")
    root = None
    values = [10, 5, 15, 3, 7, 12, 18]

    for v in values:
        root = insert_bst(root, v)

    print("Inorder:", end=' ')
    inorder(root)

    print("\nHeight:", height(root))

    #Contact Directory
    print("\n\n=== Contact Directory ===")

    directory = ContactDirectory()

    directory.root = directory.insert(directory.root, 'Alice', '123-456-7890')
    directory.root = directory.insert(directory.root, 'Bob', '234-567-8901')
    directory.root = directory.insert(directory.root, 'Eve', '345-678-9012')

    print("All contacts:")
    directory.inorder(directory.root)

    print("\nSearching for Bob:")
    contact = directory.search(directory.root, 'Bob')
    if contact:
        print(f"Found contact: {contact.name} - {contact.phone}")
    else:
        print("Contact not found")

    print("\nDeleting Alice:")
    directory.root = directory.delete(directory.root, 'Alice')
    directory.inorder(directory.root)