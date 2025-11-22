import multiprocessing as mp

from logger import Logger
from routeoptimizer import RouteOptimizer
from utils import print_time


@print_time
def process_tracks(logger: Logger, input_directory: str, output_file: str, save_as_tracks=True):
    route_optimizer = RouteOptimizer(logger)
    route_optimizer.load(input_directory)

    total_distance = route_optimizer.get_total_distance() / 1000.0
    logger.info(f'Total distance: {total_distance:.2f} km')

    route_optimizer.optimize(10.0, 1.0)

    if save_as_tracks:
        route_optimizer.save_as_tracks(output_file)
    else:
        route_optimizer.save_as_segments(output_file)


def main():
    logger = Logger(__name__)
    logger.info(f'Using {mp.cpu_count()} CPUs')

    # process_tracks(logger, r'D:\Projects\travel\data\GPX\Recorded\Bicycle', r'D:\Projects\travel\data\GPX\Recorded\Bicycle.gpx')
    # process_tracks(logger, r'D:\Projects\travel\data\GPX\Recorded\Car', r'D:\Projects\travel\data\GPX\Recorded\Car.gpx')
    process_tracks(logger, r'D:\Projects\travel\data\GPX\Recorded\Motorcycle', r'D:\Projects\travel\data\GPX\Recorded\Motorcycle.gpx')

if __name__ == '__main__':
    main()
