import logging

from logger import Logger
from routeoptimizer import RouteOptimizer
from utils import print_time


@print_time
def car(logger):
    input_files = [
        r'E:\Google\Trasy\Opel Astra',
    ]

    output_file = r'..\data\Car.gpx'

    route_optimizer = RouteOptimizer(logger)
    route_optimizer.load(input_files)

    total_distance = route_optimizer.get_total_distance() / 1000
    logger.info(F'Total distance: {total_distance:.2f} km')

    route_optimizer.optimize(5, 10)
    route_optimizer.save_as_tracks(output_file)


@print_time
def bicycle(logger):
    input_files = [
        r'E:\Google\Trasy\Rower'
    ]

    output_file = r'..\data\Rower.gpx'

    route_optimizer = RouteOptimizer(logger)
    route_optimizer.load(input_files)

    total_distance = route_optimizer.get_total_distance() / 1000
    logger.info(F'Total distance: {total_distance:.2f} km')

    route_optimizer.optimize(2, 10)
    route_optimizer.save_as_tracks(output_file)


@print_time
def motorcycle(logger):
    input_files = [
        r'E:\Google\Trasy\Motocykl',
    ]

    output_file = r'..\data\Moto.gpx'

    route_optimizer = RouteOptimizer(logger)
    route_optimizer.load(input_files)

    total_distance = route_optimizer.get_total_distance() / 1000
    logger.info(F'Total distance: {total_distance:.2f} km')

    route_optimizer.optimize(5, 10)
    route_optimizer.save_as_tracks(output_file)


@print_time
def offroad(logger):
    input_files = [
        r'E:\Google\Trasy\Nissan Patrol',
    ]

    output_file = r'..\data\Patrol.gpx'

    route_optimizer = RouteOptimizer(logger)
    route_optimizer.load(input_files)

    total_distance = route_optimizer.get_total_distance() / 1000
    logger.info(F'Total distance: {total_distance:.2f} km')

    route_optimizer.optimize(5, 10)
    route_optimizer.save_as_tracks(output_file)


if __name__ == '__main__':
    logger = Logger()
    logger.set_level(logging.DEBUG)

    # car(logger)
    # bicycle(logger)
    motorcycle(logger)
    # offroad(logger)
