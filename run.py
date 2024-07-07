import time
import cProfile
import pstats

from diamond_mosaic.img_to_mosaic import img_to_mosaic


def main():
    start_time = time.time()

    mosaic_number_h = 50 
    mosaic_number_w = 5
    img = "doge.jpg"

    with cProfile.Profile() as pr:
        img_to_mosaic(img, mosaic_number_w, mosaic_number_h)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    #    stats.print_stats(100)

    print(f"DONE! Run time = {time.time() - start_time}")


if __name__ == "__main__":
    main()
