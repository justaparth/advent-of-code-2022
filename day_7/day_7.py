from __future__ import annotations
import unittest

MAX_SIZE_P1 = 100000
FS_SIZE = 70000000
AMOUNT_NEEDED = 30000000


class Filesystem:
    def __init__(self):
        self.folder = Folder("/")

    # assume path always starts with '/'
    # will also initialize empty folders where necessary
    def folder_at_path(self, path: list[str]) -> Folder:
        ptr = self.folder
        for part in path[1:]:
            if part not in ptr.subfolders:
                ptr.subfolders[part] = Folder(part)
            ptr = ptr.subfolders[part]
        return ptr

    # recursively computes sizes
    # instead of doing this on every file addition, doing once at the
    # end should be better, i think
    def compute_sizes(self):
        self.folder.fix_sizes()


class Folder:
    def __init__(self, name: str):
        self.size: int = 0
        self.name: str = name
        self.files: dict[str, int] = {}
        self.subfolders: dict[str, Folder] = {}

    def fix_sizes(self):
        total = 0
        for size in self.files.values():
            total += size
        for subfolder in self.subfolders.values():
            subfolder.fix_sizes()
            total += subfolder.size
        self.size = total


def main():
    f = open("day_7_input.txt", "r")
    filesystem = parse_filesystem(f.read().strip())
    # total = part_1(filesystem)
    total = part_2(filesystem)
    print(total)


def parse_filesystem(contents: str) -> Filesystem:
    filesystem = Filesystem()
    lines = [x.strip() for x in contents.split("\n")]
    i = 0
    dirstack = []

    while i < len(lines):
        # handle directory changes
        if lines[i].startswith("$ cd"):
            parts = lines[i].split(" ")
            if parts[2] == "..":
                dirstack.pop()
            elif parts[2] == "/":
                dirstack = ["/"]
            else:
                dirstack.append(parts[2])
            print(dirstack)
            i += 1

        # handle list operations
        elif lines[i].startswith("$ ls"):
            folder = filesystem.folder_at_path(dirstack)
            i += 1
            while i < len(lines) and not lines[i].startswith("$"):
                line = lines[i]
                if line.startswith("dir"):
                    i += 1
                    continue
                parts = line.strip().split(" ")
                size = int(parts[0])
                folder.files[parts[1]] = size
                i += 1
        else:
            raise Exception("unknown error")

    filesystem.compute_sizes()
    return filesystem


def part_1(filesystem: Filesystem) -> int:
    # figure out the sum of all folder sizes that are less than the threshold
    total = 0
    q: list[Folder] = [filesystem.folder]
    while len(q) != 0:
        elem = q.pop()
        if elem.size <= MAX_SIZE_P1:
            total += elem.size
        for sub in elem.subfolders.values():
            q.append(sub)

    return total


def part_2(filesystem: Filesystem) -> int:
    # figure out the smallest folder to delete to get us underneath the threshold set
    space_used = filesystem.folder.size
    print(space_used)
    best = space_used + 1
    q: list[Folder] = [filesystem.folder]
    while len(q) != 0:
        elem = q.pop()
        if space_used - elem.size <= (FS_SIZE - AMOUNT_NEEDED):
            if elem.size < best:
                best = elem.size
                print(best)
        for sub in elem.subfolders.values():
            q.append(sub)

    return best


class Day7Test(unittest.TestCase):
    input = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()

    def test_part1(self):
        filesystem = parse_filesystem(self.input)
        self.assertEqual(95437, part_1(filesystem))

    def test_part1(self):
        filesystem = parse_filesystem(self.input)
        self.assertEqual(24933642, part_2(filesystem))


if __name__ == "__main__":
    # unittest.main()
    main()
