import folium
import googlemaps
import gmplot
import gpxpy
import logging
import sys

from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from config import Config
from logger import Logger


def main1(logger):
    gmaps = googlemaps.Client(key=Config.GOOGLE_MAPS_KEY)

    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)

    logger.info(directions_result)


def main2(logger):
    gpx_file = open('../data/Rower.gpx', 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
    latitude = sum(p[0] for p in points) / len(points)
    longitude = sum(p[1] for p in points) / len(points)
    myMap = folium.Map(location=[latitude, longitude], zoom_start=13)
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(myMap)

    myMap.save('a.html')


class WebEnginePage(QWebEnginePage):
    def __init__(self, logger, browser):
        super().__init__(browser)

        self.logger = logger

    def javaScriptConsoleMessage(self, QWebEnginePage_JavaScriptConsoleMessageLevel, p_str, p_int, p_str_1):
        self.logger.info(p_str)


class MainWindow(QMainWindow):
    def __init__(self, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = logger

        layout = QHBoxLayout(self)
        layout.addWidget(QPushButton("Left-Most"), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QPushButton("Center"), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QPushButton("Right-Most"), alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        """
        menu_bar = self.menuBar()

        self.exit_action = QAction("&Exit...", self)
        self.exit_action.triggered.connect(self.do_exit_action)

        self.file_menu = menu_bar.addMenu("&File")
        self.file_menu.addAction(self.exit_action)

        self.load_action = QAction("&Load...", self)
        self.load_action.triggered.connect(self.do_load_action)

        self.gpx_menu = menu_bar.addMenu("&GPX")
        self.gpx_menu.addAction(self.load_action)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Name'])

        self.browser = QWebEngineView()
        self.browser.setPage(WebEnginePage(self.logger, self.browser))
        self.browser.setHtml('<script>document.write("hello");console.log("hello");</script>')

        self.layout = QHBoxLayout()
        self.layout.addWidget(QPushButton("Left-Most"), alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(QPushButton("R-Most"), alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        """

    def load_gpx(self, file_names):
        self.logger.info(f'Loading {file_names}')

        map = folium.Map()

        for file_name in file_names:
            with open(file_name, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)

                for track in gpx.tracks:
                    for segment in track.segments:
                        points = []

                        for point in segment.points:
                            points.append(tuple([point.latitude, point.longitude]))

                        folium.PolyLine(points, color='red', weight=2.5, opacity=1).add_to(map)

                        latitude = sum(p[0] for p in points) / len(points)
                        longitude = sum(p[1] for p in points) / len(points)

                        map.location = [latitude, longitude]

        map.save('data/map.html')



        # self.browser.setHtml(map.get_root().render())
        # self.logger.info(map.get_root().render())



        latitude_list = [30.3358376, 30.307977, 30.3216419]
        longitude_list = [77.8701919, 78.048457, 78.0413095]

        gmap3 = gmplot.GoogleMapPlotter(30.3164945,
                                        78.03219179999999, 13, apikey=Config.GOOGLE_MAPS_KEY)

        # scatter method of map object
        # scatter points on the google map
        gmap3.scatter(latitude_list, longitude_list, '# FF0000',
                      size=40, marker=False)

        # Plot method Draw a line in
        # between given coordinates
        gmap3.plot(latitude_list, longitude_list, 'cornflowerblue', edge_width=2.5)
        gmap3.draw('data/map.html')



        self.browser.setUrl(QUrl("file:///data/map.html"))

    def do_exit_action(self):
        self.close()

    def do_load_action(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter('GPX Files (*.gpx)')
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec_():
            self.load_gpx(dialog.selectedFiles())


def main():
    logger = Logger()
    logger.set_level(logging.DEBUG)

    app = QApplication(sys.argv)

    window = MainWindow(logger)
    window.resize(1500, 1000)
    window.setWindowTitle('GPX')
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
