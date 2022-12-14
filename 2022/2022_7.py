import typing
from functools import lru_cache

from puzzle import Puzzle


class FileObject:
    ROOT: "FileObject" = None

    def __init__(
            self,
            label: str,
            parent: typing.Optional["FileObject"],
            size: typing.Optional[int] = 0
    ):
        self.label = label
        if label == "/":
            FileObject.ROOT = self
        self.parent = parent
        self.size = size
        self.children: typing.Dict[str, "FileObject"] = {}

    def __repr__(self):
        return f"FileObject {self.label}, size: {self.size}"

    @lru_cache()  # Should be lazy property
    def get_size(self):
        total_size = self.size + sum([
            child.get_size() for child in self.children.values()
        ])
        # print(f"Total size of {self.label} is {total_size}")
        return total_size

    def cd(self, label: str):
        if label == "..":
            return self.parent
        if label == "/":
            return self.ROOT
        self.add_child(label, 0)
        return self.children[label]

    def add_child(self, label: str, size: int):
        if label not in self.children:
            self.children[label] = FileObject(label, parent=self, size=size)
        elif self.children[label].size != size:
            raise ValueError("Size changed despite same location")

    def is_directory(self):
        return self.size == 0

    def get_self_and_all_descendants(self) -> typing.Set["FileObject"]:
        return {self}.union({
            descendant for child in self.children.values()
            for descendant in child.get_self_and_all_descendants()
        })

    def get_small_child_directories(self, maximum_size=100000):
        if self.is_directory() and self.get_size() <= maximum_size:
            return [
                child for child in self.get_self_and_all_descendants()
                if child.is_directory()
            ]
        return [
            descendant for child in self.children.values()
            for descendant in child.get_small_child_directories(maximum_size)
        ]

    def get_big_directories(self, minimum_size=3000000):
        if self.get_size() < minimum_size:
            return set()
        return {self}.union({
            descendant for child in self.children.values()
            for descendant in child.get_big_directories()
            if (
                child.is_directory()
                and child.get_size() >= minimum_size
                and descendant.is_directory()
                and descendant.get_size() >= minimum_size
            )
        })


class Day7(Puzzle, day=7):
    TOTAL_SPACE = 70000000
    NEEDED_SPACE = 30000000

    @staticmethod
    def parse_file_structure(lines: typing.Iterator[str]):
        current_folder = FileObject("/", None)
        listing_files = False
        for line in lines:
            line_split = line.split(" ")
            if line_split[0] == "$":
                listing_files = False
                if line_split[1] == "cd":
                    current_folder = current_folder.cd(
                        line_split[2]
                    )
                elif line_split[1] == "ls":
                    listing_files = True
            elif not listing_files:
                raise ValueError("Not meant to be listing files")
            elif line_split[0] == "dir":
                current_folder.add_child(line_split[1], 0)
            else:
                current_folder.add_child(line_split[1], size=int(line_split[0]))

    def solve_part_1(self, lines: typing.Iterator[str]):
        self.parse_file_structure(lines)
        print(FileObject.ROOT.get_small_child_directories())
        print(sum(
            file_object.get_size() for file_object
            in FileObject.ROOT.get_small_child_directories()
        ))

    def solve_part_2(self, lines: typing.Iterator[str]):
        self.parse_file_structure(lines)
        minimum_size = self.NEEDED_SPACE - (
                self.TOTAL_SPACE - FileObject.ROOT.get_size()
        )
        print(f"Minimum delete needed: {minimum_size}")
        print(FileObject.ROOT.get_big_directories(minimum_size=minimum_size))
        print(min(
            FileObject.ROOT.get_big_directories(minimum_size=minimum_size),
            key=lambda file_object: file_object.get_size()
        ).get_size())


if __name__ == "__main__":
    puzzle = Day7()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)