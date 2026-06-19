from pathlib import Path

from qgis.core import (
    QgsSpatialIndex,
    QgsVectorFileWriter,
    QgsVectorLayer,
)

#Import zones géographiques avec spatial index
zones = QgsVectorLayer("C:/Users/mon/Chemin/vers/zones.shp", "zones", "ogr")
spatial_index_zones = QgsSpatialIndex(zones.getFeatures())

#Import points de morts depuis csv
csv_uri_path = Path("C:/Users/mon/Chemin/vers/listOfDeath.csv").resolve().as_uri()
uri = (
    f"{csv_uri_path}"
    "?type=csv"
    "&delimiter=;"
    "&xField=longitude"
    "&yField=latitude"
    "&crs=EPSG:4326"
    "&detectTypes=yes"
    "&trimFields=yes"
    )
deaths = QgsVectorLayer(uri, "points_csv", "delimitedtext")
spatial_index_deaths = QgsSpatialIndex(deaths.getFeatures())

featGood = QgsVectorLayer("Point?crs=EPSG:4326", "points_associes", "memory")
featNotGood = QgsVectorLayer("Point?crs=EPSG:4326", "points_non_associes", "memory")

#intersection entre les points de morts et les zones géographiques
for death_feature in deaths.getFeatures() :
    ok = False
    death_geom = death_feature.geometry()
    for zone_feature in zones.getFeatures ():
        zone_geom = zone_feature.geometry()
        if death_geom.intersects(zone_geom):
            zone_name = zone_feature['nom']
            provider = featGood.dataProvider()
            provider.addFeature(death_feature)
            featGood.updateExtents()
            ok = True
            break
    if not ok:
        provider = featNotGood.dataProvider()
        provider.addFeature(death_feature)
        featNotGood.updateExtents()

#Export de couches pour featGood et featNotGood
output_path_good = Path("C:/Users/mon/Chemin/vers/avec_zone.shp")
output_path_not_good = Path("C:/Users/mon/Chemin/vers/sans_zone.shp")
QgsVectorFileWriter.writeAsVectorFormat(featGood, str(output_path_good), "  utf-8", driverName="ESRI Shapefile")
QgsVectorFileWriter.writeAsVectorFormat(featNotGood, str(output_path_not_good   ), "  utf-8", driverName="ESRI Shapefile")