class RBTreeNode:
    __slots__ = ['key','red','left','right','parent','left_amount','left_sum','right_amount','right_sum']
    def __init__(self, key = None):
        self.key = key
        self.left_sum = 0
        self.right_sum = 0
        self.left_amount = 0
        self.right_amount = 0
        self.red = False
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    __slots__ = ['root','nil']
    def __init__(self):
        """
        Initializing tree with empty nil and root nodes with no children and no parent
        """
        self.nil = RBTreeNode()
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil

        self.root = RBTreeNode()
        self.root.parent = self.nil
        self.root.left = self.nil
        self.root.right = self.nil

    def is_leaf(self, x):
        if x.left == self.nil and x.right == self.nil:
            return True
        else:
            return False

    def left_rotate(self,x: RBTreeNode):
        """
        Rotates subtree as described in _Introduction_To_Algorithms_ by
        Cormen, Leiserson, Rivest (Chapter 14).  Basically this
        makes the parent of x be to the left of x, x the parent of
        its parent before the rotation and fixes other pointers
        accordingly.
        :param x: RBTreeNode to be rotated
        :return: None
        :modifies: self, x, sums and amounts
        """
        y = x.right
        x.right = y.left
        if y.left != self.nil:
           y.left.parent = x
        y.parent = x.parent
        if x.parent == self.root:
            self.root.left = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

        """Changing amount and sum in left and right subtrees for rotated nodes when changed"""
        x.right_amount = x.right.left_amount + x.right.right_amount + 1 if x.right != self.nil else 0
        x.right_sum = x.right.left_sum + x.right.right_sum + x.right.key if x.right != self.nil else 0

        y.left_amount += x.left_amount + 1
        y.left_sum += x.left_sum + x.key

        assert (not self.nil.red), "nil not black in left_rotate"

    def right_rotate(self, y: RBTreeNode):
        """
        Rotates as described in _Introduction_To_Algorithms_ by
        Cormen, Leiserson, Rivest (Chapter 14).  Basically this
        makes the parent of x be to the left of x, x the parent of
        its parent before the rotation and fixes other pointers
        accordingly.
        :param y: RBTreeNode to be rotated
        :return: None
        :modifies: self, y, sums and amounts
        """
        x = y.left
        y.left = x.right
        if self.nil != x.right:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.root:
            self.root.left = x
        if y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

        """Changing amount and sum in left and right subtrees for rotated nodes when changed"""
        y.left_amount = y.left.left_amount + y.left.right_amount + 1 if y.left != self.nil else 0
        y.left_sum = y.left.left_sum + y.left.right_sum + y.left.key if y.left != self.nil else 0

        x.right_amount += y.right_amount + 1
        x.right_sum += y.right_sum + y.key

        assert (not self.nil.red), "nil not black in right_rotate"

    def _tree_insert_fixup(self, z: RBTreeNode):
        """
        Fixes tree after insert of z into the tree as if it was a regular
        binary tree using the algorithm described in _Introduction_To_Algorithms_
        by Cormen et al, 3rd Edition. This function is only intended to be called
        by the Insert function and not by the user
        :param z: RBTreeNode to start fixup
        :return: None
        :modifies: self, z, sums and amounts in parent to z nodes
        """
        while z.parent.red:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.left_rotate(z.parent.parent)
        self.root.left.red = False
        assert (not self.nil.red), "nil not black in _tree_insert_fixup"

    def insert(self, new_entry):
        """
        This function returns a pointer to the newly inserted node
        which is guaranteed to be valid until this node is deleted.
        What this means is if another data structure stores this
        pointer then the tree does not need to be searched when this
        is to be deleted.
        :param new_entry: key to insert
        :return: new RBTreeNode that contains new_entry as key
        :modifies: self, sums and amounts
        """
        z = RBTreeNode(new_entry)
        y = self.root
        x = self.root.left
        while x != self.nil:
            y = x
            if z.key < x.key:
                x.left_amount += 1
                x.left_sum += z.key
                x = x.left
            else:
                x.right_amount += 1
                x.right_sum += z.key
                x = x.right
        z.parent = y
        if y == self.root:
            self.root.left = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.red = True
        self._tree_insert_fixup(z)
        return z

    def _transplant(self,u,v):
        """
        Directly changes u to v by linking parents of u to v and vice versa.
        Make no additional work with excluding loops, so must be called only by delete_node method.
        :param u: old node to be substituted by v
        :param v: node that will substitute u
        :return: None
        :modifies: self
        """
        if u.parent == self.root:
            self.root.left = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _decrease_lookup(self, z):
        """
        Walks on the z-root way and decreases every nodes' left/right corresponding
        (depends on child is left or right) amount and sum with 1 and z.key correspondingly.
        Must be called only by delete_node method, as it is part of its' procedure.
        :param z:
        :return: None
        :modifies: self
        """
        buff_node = z
        while buff_node.parent != self.root:
            if buff_node == buff_node.parent.left:
                buff_node.parent.left_amount -= 1
                buff_node.parent.left_sum -= z.key
            else:
                buff_node.parent.right_amount -= 1
                buff_node.parent.right_sum -= z.key
            buff_node = buff_node.parent

    def _delete_fix_up(self, x: RBTreeNode):
        """
        Performs rotations and changes colors to restore red-black
        properties after a node is deleted. All sum/amount work is done in rotate functions
        :param x: child of the spliced out node in delete_node.
        :return: None
        :modifies: self, x
        """
        root_left = self.root.left

        while not x.red and root_left != x:
            if x == x.parent.left:
                w = x.parent.right
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.parent
                else:
                    if not w.right.red:
                        w.left.red = False
                        w.red = True
                        self.right_rotate(w)
                        w = x.parent.right
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    self.left_rotate(x.parent)
                    x = root_left
            else:
                w = x.parent.left
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.parent
                else:
                    if not w.left.red:
                        w.right.red = False
                        w.red = True
                        self.left_rotate(w)
                        w = x.parent.left
                    w.red = x.parent.red
                    x.parent.red = False
                    w.left.red = False
                    self.right_rotate(x.parent)
                    x = root_left
        x.red = False
        assert (not self.nil.red), "nil not black in _delete_fix_up"

    def delete_node(self, z: RBTreeNode):
        """
        Deletes z from tree and fixes the tree. Algorithm described in _Introduction_to_Algorithms_
        by Cormen et al., 3rd Edition (2009). WARNING! Be ready that older edition has completely
        different description of pseudocode, wrong at several points, and thus redefined in new edition.
        Also, in older edition would be poorer explanation with less graph-explanation.
        :param z: node from this tree to delete
        :return: key that was stored in deleted node
        :modifies: self, z
        """
        y = z
        y_red = y.red
        if z.left == self.nil:
            """
            1st case: no left children. Note that it is insignificant if there is no right child too.
            We will just decrease every value on z-root path and replace z with z.right.
            """
            x = z.right
            self._decrease_lookup(z)
            self._transplant(z,z.right)
        elif z.right == self.nil:
            """
            2nd case: no right children. Note that right child exists because of 1st case.
            We will just decrease every value on z-root path and replace z with z.left.
            """
            x = z.left
            self._decrease_lookup(z)
            self._transplant(z,z.left)
        else:
            y = z.right
            while y.left != self.nil:
                y = y.left
            y_red = y.red
            x = y.right
            if y.parent == z:
                """
                3rd case: right child is the closest node: no left descendants. Thus, z.right.left is nil.
                For the sake of algorithm z.right.right.parent = z.right, even if z.right.right is nil.
                We will decrease every value on z-root path and replace z with z.right.
                Also we replace left amount of y with left amount of z. At the end, we will replace z with z.right
                directly and links to the z.left. Look illustration in Cormen to understand.
                """
                x.parent = y
                y.left_amount = z.left_amount
                y.left_sum = z.left_sum
                self._decrease_lookup(z)
            else:
                """
                4th case: right child is not the closest node: there are leftmost descendant (min of z.right).
                We will decrease values of all nodes on z.right-z.right.min path with z.right.min
                as it will be replaced from this subtree.
                Right amount/sum for z.right.min on new position will be just as for z, but w/o z.right.min itself.
                Left amount/sum for z.right.min on new position will match with z left amount/sum.
                We will decrease every value on z-root path. We will replace z.right.min with z.right.min.right.
                Also we will relink z.right.min.right to z.right and same parent relationship.
                At the end, we will replace z with z.right.min directly and links to the z.left.
                Look illustration in Cormen to understand.
                """
                buff_node = z.right
                while buff_node != y:
                    buff_node.left_amount -= 1
                    buff_node.left_sum -= y.key
                    buff_node = buff_node.left
                y.right_amount = z.right_amount - 1
                y.right_sum = z.right_sum - y.key
                y.left_amount = z.left_amount
                y.left_sum = z.left_sum
                self._decrease_lookup(z)
                self._transplant(y,y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z,y)
            y.left = z.left
            y.left.parent = y
            y.red = z.red
        if not y_red:
            self._delete_fix_up(x)
        return_value = z.key
        del z
        return return_value

    def check_amount_and_sum(self,node):
        """
        Test recursive function used to check if tree has correct amount and sums, starting from self.root.left.
        True if node is nil, if 0 for the side with nil-child and if correct sum/amount for non-nil child.
        :param node: node to check.
        :return: boolean for this very node, that will be used by upper recursive call.
        :modifies: None.
        """
        if node == self.nil:
            return True
        if not self.check_amount_and_sum(node.left):
            return False
        if not self.check_amount_and_sum(node.right):
            return False
        if node.left == self.nil:
            if node.left_amount != 0 or abs(node.left_sum) > 1e-6:
                return False
        else:
            if node.left_amount != node.left.left_amount + node.left.right_amount + 1:
                return False
            if abs(node.left_sum - node.left.left_sum - node.left.right_sum - node.left.key) > 1e-6:
                return False
        if node.right == self.nil:
            if node.right_amount != 0 or abs(node.right_sum) > 1e-6:
                return False
        else:
            if node.right_amount != node.right.left_amount + node.right.right_amount + 1:
                return False
            if abs(node.right_sum - node.right.left_sum - node.right.right_sum - node.right.key) > 1e-6:
                return False
        return True