import multiprocessing as mp

from logger import Logger
from routeoptimizer import RouteOptimizer
from utils import print_time


@print_time
def process_tracks(logger: Logger, input_directories: list, output_file: str, min_distance: float=10.0, min_angle: float=1.0, save_as_tracks=True):
    route_optimizer = RouteOptimizer(logger)
    route_optimizer.load(input_directories)

    total_distance = route_optimizer.get_total_distance() / 1000.0
    logger.info(f'Total distance: {total_distance:.2f} km')

    route_optimizer.optimize(min_distance, min_angle)

    if save_as_tracks:
        route_optimizer.save_as_tracks(output_file)
    else:
        route_optimizer.save_as_segments(output_file)


def main():
    logger = Logger(__name__)
    logger.info(f'Using {mp.cpu_count()} CPUs')

    process_tracks(logger, [r'D:\Projects\travel\data\GPX\Recorded\Bicycle'], r'D:\Projects\travel\data\GPX\Visited\Bicycle.gpx')
    process_tracks(logger, [r'D:\Projects\travel\data\GPX\Recorded\Car'], r'D:\Projects\travel\data\GPX\Visited\Car.gpx')
    process_tracks(logger, [r'D:\Projects\travel\data\GPX\Recorded\Motorcycle'], r'D:\Projects\travel\data\GPX\Visited\Motorcycle.gpx')

    process_tracks(logger, [r'D:\Projects\travel\data\GPX\Recorded\Motorcycle\BMW F 800 GS\Bałkany'], r'D:\Projects\travel\data\GPX\Visited\Balkans.gpx')
    process_tracks(logger, [r'D:\Projects\travel\data\GPX\Recorded\Motorcycle\BMW F 800 GS\Czechy'], r'D:\Projects\travel\data\GPX\Visited\Czech.gpx')
    process_tracks(logger, [r'D:\Projects\travel\data\GPX\Recorded\Motorcycle\BMW F 800 GS\Słowenia'], r'D:\Projects\travel\data\GPX\Visited\Slovenia.gpx')

    paths = [
        r'D:\Projects\travel\data\GPX\Recorded\Motorcycle\BMW F 800 GS\Słowacja 1',
        r'D:\Projects\travel\data\GPX\Recorded\Motorcycle\BMW F 800 GS\Słowacja 2',
        r'D:\Projects\travel\data\GPX\Recorded\Motorcycle\BMW F 800 GS\Słowacja 3',
        r'D:\Projects\travel\data\GPX\Recorded\Motorcycle\BMW F 800 GS\Słowacja 4',
    ]

    process_tracks(logger, paths, r'D:\Projects\travel\data\GPX\Visited\Slovakia.gpx')


if __name__ == '__main__':
    main()
