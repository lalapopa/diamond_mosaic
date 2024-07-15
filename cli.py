import dataclasses
import pathlib
import tyro

from diamond_mosaic.img_to_mosaic import img_to_mosaic


@dataclasses.dataclass
class Args:
    """Convert your image to diamond painting canvas."""

    image: pathlib.Path
    """Path to `.png` or `.jpg` image."""

    d_num_w: int = 100
    """How many diamonds (dots) will be along horizontal side."""

    d_num_h: int = 0
    """
    How many diamonds (dots) will be along vertical side. You can skip this 
    value if you defined `d_num_w`, using image pixel ratio this
    value will be calculated.
    """

    save_name: str = "result"
    """
    Output files name.
    """

    d_d: float = 0.25
    """
    Diamond diameter in centimeter.
    """


def main():
    args = tyro.cli(Args)
    img_to_mosaic(args.image, args.d_num_w, args.d_num_h, args.d_d, args.save_name)


if __name__ == "__main__":
    main()
