import gpxpy
import math

from geopy import distance
from geographiclib.geodesic import Geodesic


class Route:
    def __init__(self, logger, filename=None):
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

    def optimize(self, min_distance, min_angle):
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
                    elif self.check_angle(a, b, c, min_angle):
                        delete_because_of_angle.append(i + 1)

                self.print_summary(segment.points, delete_because_of_distance)
                self.print_summary(segment.points, delete_because_of_angle)

                to_delete = delete_because_of_distance + delete_because_of_angle
                to_delete.sort(reverse=True)

                for index in to_delete:
                    del segment.points[index]

    def check_distance(self, a, b, min_distance):
        distance_between = distance.geodesic((a.latitude, a.longitude), (b.latitude, b.longitude)).meters

        return distance_between < min_distance

    def check_angle(self, a, b, c, min_angle):
        d = Geodesic.WGS84.Inverse(a.latitude, a.longitude, b.latitude, b.longitude)
        e = Geodesic.WGS84.Inverse(b.latitude, b.longitude, c.latitude, c.longitude)

        angle_between = math.fabs(d['azi1'] - e['azi1'])

        return angle_between < min_angle

    def print_summary(self, points, indices):
        points_to_delete_len = len(indices)
        points_len = len(points)
        percentage = points_to_delete_len / points_len * 100

        self.logger.info(F'Deleting {points_to_delete_len} from {points_len} points ({percentage:.0f}%)')

    def save(self, filename):
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
        return F'Routes: {len(self.routes)}, Tracks: {len(self.tracks)}, Waypoints: {len(self.waypoints)}'
