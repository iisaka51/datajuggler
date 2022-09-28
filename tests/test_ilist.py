import time
import pytest

from datajuggler import iList

class TestClass:
    def test_ilist_case01(self):
        l = iList()
        assert l == []

    def test_ilist_case02(self):
        l = iList([1,2,3])
        assert l == [1,2,3]

    def test_ilist_case03(self):
        l = iList()
        with pytest.raises(IndexError) as e:
            l[0] = 1
        assert str(e.value) == 'list assignment index out of range'

    def test_ilist_case04(self):
        l = iList([1])
        l[0] = 10
        assert l == [10]

    def test_ilist_eq_case01(self):
        l1 = iList([1,2,3,4,5])
        l2 = iList([1,2,3,4,5])
        assert l1 == l2

    def test_ilist_eq_case02(self):
        l1 = iList([1,2,3,4,5])
        l2 = list([1,2,3,4,5])
        assert l1 == l2

    def test_ilist_ne_case01(self):
        l1 = iList([5,4,3,2,1])
        l2 = iList([1,2,3,4,5])
        assert l1 != l2

    def test_ilist_ne_case02(self):
        l1 = iList([5,4,3,2,1])
        l2 = list([1,2,3,4,5])
        assert l1 != l2

    def test_ilist_freeze_case01(self):
        l1 = iList([1, 2, 3])
        with pytest.raises(AttributeError) as e:
            hash(l1)
        assert str(e.value) == 'unhashable not frozen object.'

    def test_ilist_freeze_case02(self):
        l = iList([1])
        l.freeze()
        with pytest.raises(AttributeError) as e:
            l[0] = 10
        assert str(e.value) == 'iList frozen object cannot be modified.'


    def test_ilist_freeze_case03(self):
        l = iList([1])
        l.freeze()
        result = hash(l)
        assert isinstance(result, int)

    def test_ilist_freeze_case04(self):
        l = iList([1])
        l.freeze()
        l.unfreeze()
        l[0] = 10
        assert l == [10]

    def test_ilist_attr_case01(self):
        l = iList([1,2,3])
        l.python = 10
        assert l.python == 10
        assert l == [1,2,3]

    def test_ilist_attr_case02(self):
        l = iList([1,2,3])
        l.python = 10
        l.python = 20
        assert l.python == 20
        assert l == [1,2,3]

    def test_ilist_attr_case03(self):
        l = iList([1,2,3])
        l.hello = 'python'
        assert l.hello == 'python'
        assert l.get_attrs('hello') == 'python'
        assert l == [1,2,3]

    def test_ilist_attr_case04(self):
        l1 = iList([1,2,3])
        l1.hello = 'python'
        l2 = iList([1,2,3])
        assert l2.get_attrs() == {}

    def test_ilist_attr_case05(self):
        l = iList([1,2,3])
        l.hello = 'python'
        assert l.get_attrs('hello') == 'python'
        assert l.get_attrs('python', 'Kyoto') == 'Kyoto'


    def test_ilist_attr_case06(self):
        l = iList([1])
        l.hello = 'python'
        with pytest.raises(KeyError) as e:
            result = l.python
        assert str(e.value) == "'python not found.'"


    def test_ilist_copy_case01(self):
        l1 = iList([1,2,3])
        l2 = l1.copy()
        assert l2 == l1

    def test_ilist_copy_case02(self):
        l1 = iList([1])
        l2 = l1.copy(freeze=True)
        result = hash(l2)
        assert isinstance(result, int)

    def test_ilist_copy_case03(self):
        l1 = iList([1])
        l2 = l1.copy(freeze=False)
        with pytest.raises(AttributeError) as e:
            result = hash(l2)
        assert str(e.value) == 'unhashable not frozen object.'

    def test_ilist_copy_case04(self):
        l1 = iList([1,2,3])
        l1.hello = 'python'
        l2 = l1.copy()
        assert l2 == l1
        assert l2.get_attrs() == {}


    def test_ilist_clone_case01(self):
        l1 = iList([1,2,3])
        l1.hello = 'python'
        l2 = l1.clone()
        assert l2 == l1
        assert l2.get_attrs() == {'hello': 'python'}

    def test_ilist_clone_case02(self):
        l1 = iList([1,2,3])
        l1.hello = 'python'
        l2 = l1.clone(empty=True)
        assert l2 == []
        assert l2.get_attrs() == {'hello': 'python'}

    def test_ilist_clone_case03(self):
        l1 = iList([1,2,3])
        l1.hello = 'python'
        l1.freeze()
        l2 = l1.clone()
        result = hash(l2)
        assert isinstance(result, int)



    def test_ilist_add_case01(self):
        l1 = iList([1,2,3])
        l2 = list([4,5,6])
        assert l1 + l2 == [1,2,3,4,5,6]

    def test_ilist_add_case02(self):
        l1 = iList([1,2,3])
        l2 = iList([4,5,6])
        assert l1 + l2 == [1,2,3,4,5,6]

    def test_ilist_radd_case01(self):
        l1 = iList([1,2,3])
        l2 = iList([4,5,6])
        del l1.__class__.__add__
        assert l1 + l2 == [1,2,3,4,5,6]

    def test_ilist_iadd_case01(self):
        l1 = iList([1,2,3])
        l2 = iList([4,5,6])
        l1 += l2
        assert l1 == [1,2,3,4,5,6]

    def test_ilist_iadd_case02(self):
        l1 = iList([1,2,3])
        l2 = iList([4,5,6])
        l1.freeze()
        with pytest.raises(AttributeError) as e:
            l1 += l2
        assert str(e.value) == 'iList frozen object cannot be modified.'


    def test_ilist_sub_case01(self):
        l1 = iList([1,2,3,4,5,6])
        l2 = iList([4,5,6])
        assert l1 - l2 == [1,2,3]

    def test_ilist_sub_case02(self):
        l1 = iList([1,2,3,4,5,6])
        l2 = list([4,5,6])
        assert l1 - l2 == [1,2,3]

    def test_ilist_mul_case01(self):
        l1 = iList([1,2,3])
        assert l1 * 3 == [1,2,3,1,2,3,1,2,3]

    def test_ilist_imul_case02(self):
        l1 = iList([1,2,3])
        l1.freeze()
        assert l1 * 3 == [1,2,3,1,2,3,1,2,3]

    def test_ilist_imul_case03(self):
        l1 = iList([1,2,3])
        l1.freeze()
        with pytest.raises(AttributeError) as e:
            l1 *= 3
        assert str(e.value) == 'iList frozen object cannot be modified.'

    def test_ilist_and_case01(self):
        l1 = iList([1,2,3,4,5,6])
        l2 = iList([4,5,6])
        assert ( l1 & l2 ) == [4,5,6]

    def test_ilist_and_case02(self):
        l1 = iList([1,4,2,5,3,6])
        l2 = list([6,4,5])
        assert (l1 & l2 ) == [4,5,6]

    def test_ilist_find_case01(self):
        l = iList([1,2,3,[4,5]])
        assert l.find(2) == [1]

    def test_ilist_find_case02(self):
        l = iList([1,2,3,[4,5]])
        assert l.find(0) == None

    def test_ilist_find_case03(self):
        l = iList([1,2,3,[4,5]])
        assert l.find([2,3]) == [1,2]

    def test_ilist_find_case04(self):
        l = iList([1,2,3,[4,5]])
        assert l.find((2,3)) == [1,2]


    def test_ilist_append_case01(self):
        l1 = iList([])
        l1.append(4)
        assert l1 == [4]

    def test_ilist_append_case02(self):
        l1 = iList([])
        l1.append([4,5,6])
        assert l1 == [[4,5,6]]

    def test_ilist_append_case04(self):
        l1 = iList([1,2,3,4,5,6])
        l1.freeze()
        with pytest.raises(AttributeError) as e:
            l1.append(4)
        assert str(e.value) == 'iList frozen object cannot be modified.'


    def test_ilist_pop_case01(self):
        l1 = iList([1,2,3,4,5,6])
        l1.pop()
        assert l1 == [1,2,3,4,5]

    def test_ilist_pop_case02(self):
        l1 = iList([1,2,3,4,5,6])
        l1.pop(0)
        assert l1 == [2,3,4,5,6]

    def test_ilist_pop_case04(self):
        l1 = iList([1,2,3,4,5,6])
        l1.freeze()
        with pytest.raises(AttributeError) as e:
            l1.pop(2)
        assert str(e.value) == 'iList frozen object cannot be modified.'


    def test_ilist_remove_case01(self):
        l1 = iList([1,2,3,4,5,6])
        l1.remove(3)
        assert l1 == [1,2,4,5,6]

    def test_ilist_remove_case02(self):
        l1 = iList([1,2,3,4,5,6])
        with pytest.raises(ValueError) as e:
            l1.remove(0)
        assert str(e.value) == "list.remove(x): x not in list"

    def test_ilist_remove_case04(self):
        l1 = iList([1,2,3,4,5,6])
        l1.freeze()
        with pytest.raises(AttributeError) as e:
            l1.remove(1)
        assert str(e.value) == 'iList frozen object cannot be modified.'


    def test_ilist_without_case01(self):
        l1 = iList([1,2,3,4,5,6])
        result = l1.without([3])
        assert result == [1,2,4,5,6]

    def test_ilist_without_case02(self):
        l1 = iList([1,2,3,4,5,6])
        with pytest.raises(TypeError) as e:
            result = l1.without(3)
        assert str(e.value) == "'int' object is not iterable"

    def test_ilist_without_case03(self):
        l1 = iList([1,2,3,4,5,6])
        result = l1.without([0])
        assert result == l1

    def test_ilist_without_case04(self):
        l1 = iList([1,2,3,4,5,6])
        l2 = [3,4,5]
        result = l1.without(l2)
        assert result == [1,2,6]

    def test_ilist_without_case04(self):
        l1 = iList([1,2,3,4,5,6])
        l2 = [3,4]
        l3 = [5,6]
        result = l1.without(l2, l3)
        assert result == [1,2]

    def test_ilist_without_case06(self):
        l1 = iList([1,2,3,4,5,6])
        l1.freeze()
        result = l1.without([1])
        assert result == [2,3,4,5,6]



    def test_ilist_replace_case01(self):
        l1 = iList([1,2,3,1,2,3])
        result = l1.replace(3, 5)
        assert result == [1,2,5,1,2,5]

    def test_ilist_replace_case02(self):
        def func(index, old, new):
            if index > 3:
                return new
            else:
                return old

        l1 = iList([1,2,3,1,2,3])
        result = l1.replace(3, 5, func)
        assert result == [1,2,3,1,2,5]


    def test_ilist_sort_case01(self):
        l1 = iList([1,5,2,4,3,6])
        l1.sort()
        assert l1 == [1,2,3,4,5,6]

    def test_ilist_sort_case02(self):
        l1 = iList([1,2,3,4,5,6])
        l1.sort(reverse=True)
        assert l1 == [6,5,4,3,2,1]

    def test_ilist_sort_case02(self):
        data = [
                [1, 9, 9],
                [2, 2, 8],
                [3, 7, 7],
                [4, 4, 6],
                [5, 5, 5],
                [6, 6, 4],
                [7, 3, 3],
                [8, 8, 2],
                [9, 1, 1],
            ]
        expect = [
                [9, 1, 1],
                [8, 8, 2],
                [7, 3, 3],
                [6, 6, 4],
                [5, 5, 5],
                [4, 4, 6],
                [3, 7, 7],
                [2, 2, 8],
                [1, 9, 9]
            ]

        def func(v):
            return v[2]

        l1 = iList(data)
        l1.sort(key=func)
        assert l1 == expect

