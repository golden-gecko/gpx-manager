import gpxpy
import multiprocessing as mp
import os

from concurrent.futures import ThreadPoolExecutor
from route import Route
from utils import print_time


class RouteOptimizer:
    def __init__(self, logger):
        self.logger = logger
        self.routes = []

    def load(self, filenames):
        for filename in filenames:
            if os.path.isdir(filename):
                for root, dirs, files in os.walk(filename):
                    for file in files:
                        self.routes.append(Route(self.logger, os.path.join(root, file)))
            else:
                self.routes.append(Route(self.logger, filename))

    @print_time
    def get_total_distance(self):
        with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
            results = [executor.submit(route.get_total_distance) for route in self.routes]

        return sum([x.result() for x in results])

    @print_time
    def optimize(self, min_distance, min_angle):
        with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
            for route in self.routes:
                executor.submit(route.optimize, args=(min_distance, min_angle))

    def save_as_points(self, filename):
        document = Route(self.logger)

        for route in self.routes:
            for track in route.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        document.waypoints.append(gpxpy.gpx.GPXWaypoint(point.latitude, point.longitude))

        document.save(filename)

    def save_as_tracks(self, filename):
        document = Route(self.logger)

        for route in self.routes:
            for track in route.tracks:
                new_track = gpxpy.gpx.GPXTrack()

                for segment in track.segments:
                    new_segment = gpxpy.gpx.GPXTrackSegment()

                    for point in segment.points:
                        new_point = gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude)
                        new_segment.points.append(new_point)

                    new_track.segments.append(new_segment)

                document.tracks.append(new_track)

        document.save(filename)
