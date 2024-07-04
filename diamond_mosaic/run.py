import time
from img_to_mosaic import img_to_mosaic
import cProfile
import pstats


def main():
    start_time = time.time()

    mosaic_number_h = 400
    mosaic_number_w = 5
    img = "img3.png"

    with cProfile.Profile() as pr:
        img_to_mosaic(img, mosaic_number_w, mosaic_number_h)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    print(f"DONE! Run time = {time.time() - start_time}")


if __name__ == "__main__":
    main()
