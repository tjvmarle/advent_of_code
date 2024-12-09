from Util.input import get_lines
from typing import Dict, List


class Lens:
    def __init__(self, label: str, focal: str) -> None:
        self.label = label
        self.focal = int(focal)

    def __eq__(self, other: 'Lens') -> bool:
        return self.label == other.label


def parse_instruction(instruction: str):  # This is basically 15a
    val = 0
    label = []
    for char in instruction:

        if (isequals := (char == "=")) or char == "-":
            return (val, "".join(label), "=" if isequals else "-")

        label.append(char)

        val += ord(char)
        val *= 17
        val %= 256


def solve() -> int:
    gen = get_lines(tst=False)

    box_map: Dict[int, List[Lens]] = {val: [] for val in range(0, 256)}
    for line in gen:
        hash_val, label, operation = parse_instruction(line)

        # The rest here is 15b
        box_lens = Lens(label, line[-1] if operation == "=" else "0")

        lens_box = box_map[hash_val]
        if operation == "-":  # Remove the lens by label, ignore focal
            if box_lens in lens_box:
                lens_box.remove(Lens(label, "0"))
        else:  # Add or update the lens
            if box_lens in lens_box:
                lens_index = lens_box.index(box_lens)
                lens_box[lens_index] = box_lens
            else:
                lens_box.append(box_lens)

    # Calc focus power
    acc: int = 0
    for box_nr, box_lenses in box_map.items():
        for index, lens in enumerate(box_lenses, 1):
            acc += (box_nr + 1) * index * lens.focal

    # Printer for the entire map
    # for key in box_map.keys():
    #     lens_list = box_map[key]
    #     if not lens_list:
    #         continue
    #     lens_str = [f"[{lens.label} {lens.focal}]" for lens in lens_list]
    #     print(f"Box {key}: {' '.join(lens_str)}")

    return acc


if __name__ == "__main__":
    print(solve())
