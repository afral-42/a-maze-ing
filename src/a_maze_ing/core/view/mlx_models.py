from dataclasses import dataclass


@dataclass
class MlxWindow:
    mlx_ptr: int
    win_ptr: int


@dataclass
class MlxImage:
    win: MlxWindow
    img_ptr: int
    img_addr: memoryview
    bits_per_pixed: int
    line_size: int
    endian: int
    width: int
    height: int
