from enum import unique

import gpxpy
import math

from geopy import distance
from geographiclib.geodesic import Geodesic

from logger import Logger


class Route:
    def __init__(self, logger: Logger, filename: str | None = None):
        self.logger = logger
        self.document = None

        if filename:
            self.load(filename)
        else:
            self.clear()

    def clear(self):
        self.document = gpxpy.gpx.GPX()

    def load(self, filename):
        self.logger.info(f'Loading {filename}')

        with open(filename, 'r') as file:
            self.document = gpxpy.parse(file)

    def get_total_distance(self):
        total_distance = 0

        for track in self.tracks:
            for segment in track.segments:
                for i in range(len(segment.points) - 1):
                    a = segment.points[i]
                    b = segment.points[i + 1]

                    total_distance += distance.geodesic((a.latitude, a.longitude), (b.latitude, b.longitude)).meters

        return total_distance

    def optimize(self, min_distance: float, min_angle: float):
        for track in self.tracks:
            for segment in track.segments:
                delete_because_of_distance = []
                delete_because_of_angle = []

                for i in range(len(segment.points) - 2):
                    a = segment.points[i]
                    b = segment.points[i + 1]
                    c = segment.points[i + 2]

                    if self.check_distance(a, b, min_distance):
                        delete_because_of_distance.append(i + 1)

                    if self.check_angle(a, b, c, min_angle):
                        delete_because_of_angle.append(i + 1)

                self.print_summary(segment.points, delete_because_of_distance, 'distance')
                self.print_summary(segment.points, delete_because_of_angle, 'angle')

                to_delete = delete_because_of_distance + delete_because_of_angle
                to_delete = list(set(to_delete))
                to_delete.sort(reverse=True)

                for index in to_delete:
                    del segment.points[index]

    def check_distance(self, a, b, min_distance: float):
        distance_between = distance.geodesic((a.latitude, a.longitude), (b.latitude, b.longitude)).meters

        return distance_between < min_distance

    def check_angle(self, a, b, c, min_angle: float):
        d = Geodesic.WGS84.Inverse(a.latitude, a.longitude, b.latitude, b.longitude)
        e = Geodesic.WGS84.Inverse(b.latitude, b.longitude, c.latitude, c.longitude)

        angle_a_b = d['azi1']
        angle_b_c = e['azi1']

        if angle_a_b < 0.0:
            angle_a_b = 180.0 + 180.0 - math.fabs(angle_a_b)

        if angle_b_c < 0.0:
            angle_b_c = 180.0 + 180.0 - math.fabs(angle_b_c)

        angle_between = math.fabs(angle_a_b - angle_b_c)

        return angle_between < min_angle

    def print_summary(self, points : list, indices : list, reason: str):
        points_to_delete_len = len(indices)
        points_len = len(points)
        percentage = points_to_delete_len / points_len * 100

        self.logger.info(f'Deleting {points_to_delete_len} from {points_len} points ({percentage:.0f}%) because of {reason}')

    def save(self, filename: str):
        if self.document:
            with open(filename, 'w') as f:
                f.write(self.document.to_xml())

    @property
    def routes(self):
        return self.document.routes

    @property
    def tracks(self):
        return self.document.tracks

    @property
    def waypoints(self):
        return self.document.waypoints

    def __str__(self):
        return f'Routes: {len(self.routes)}, Tracks: {len(self.tracks)}, Waypoints: {len(self.waypoints)}'
