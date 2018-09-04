
# NautilusLive dive data explorer


This repository contains a few work-in-progress projects exploring the dive data form [E/V Nautilus dives](http://nautiluslive.org)

# About The Data

The data presented on NautilusLive.org is not the
full/complete scientific record. Please go to http://www.oet.org for
information on accessing the archived dataset.

The used dive data is available as a JSON object at

```
http://nautiluslive.org/sites/default/files/nautilus-vehicle-data.json
```

# Organization of this repository

data
dispair
fetch-nautilus-json-data.py
img
osm.html
plot.py
plots-and-data-manipulation.ipynb
README.md
static-web-plot
test-nautilus-json-data.py
webview



# Development Ideas


1. individually linkable views of data from one dive
    - by date of the dive/name of location (any unique ID)
    - post process data, split it into individual dive sized chunks
    - serve static site with static data, but interactive plots (plotly + json in files)
2. link to individual dive by passing start and end time as parameters
    - choronograf and grafana should both support this without extra config
    - should be trivial to add to other solutions as well.
3. Make a map of dive locations
    - each marker on map links to a view of the data for that dive
        - overview on hover, click thorough to dashboard
    - leaflet, openLayers
    - source for global ocean floor topography tiles?
    - OSM boring with featureless sea
4. include Herc camera screenshots
    - how to download individual frames from live stream?
    - numpy for image processing
    - image URL with timestamp into influx
    - always show image closest in time to cursor timestamp
    - grafana may have built-in visualization for showing timestamped images
    - process images to small thumbnails that can be delayed with minimal delay when moving timestamp cursor. Using full resolution images will likely leave the image view feel
5. make static plots with eventlog
    - matplotlib
    - label placement logic
6. Figure out if it is possible to get a cross site request header (XCORS?) configured.
    - Currently it is not possible to fetch JSON data from the API with AJAX calls from javascript from a webpage due to security restrictions. Modern browsers have a same-origin policy. A web page can't AJAX to a resource on a third party domain unless the third party server can include correct Cross-origin headers.
    Using cross-origin requests would allow hosting a dashboard with live data without a backend server (eg. on github pages)
7. Add option to run JSON fetch sctipt as a cronjob instead of using an infinite while loop.
8. Make polar plots of wind data
    - use wind direction as angle, time as distance from origin
    - use wind direction as angle, wind speed as distance, and a colormap to relay time information. This is essentially a 2d histogram with polar coordinates. This is definetly doable with matplotlib, and likely with plotly (may need some datamangling). Maybe Grafana, definetly not with Chronograf. See antenna radiation pattern plots for boilerplate code.

## Dataprocessing tasks


1. determine ship longitude based on timestampa and tide data from Hercules. Tide data is visible in the Hercules depth data during long stays on the seafloor. Tides are visible as a dirft of few decimeters/hour is the depth data. See the datasets for the hot tub of despair and a dive on 06-25-2018. There are likely other datasets as well. Use wind direction data from Nautilus in concert with radar wind data to narrow down the possible locations.
    - Are there remote sensing tide data freely available?
    - Find global tide model to calculate baseline for locating based on Hercules tide data
    - Find source for global remote sensing wind data/modelled wind data.
    - Write algorithm to find datasets with tide data available





# InfluxFB

InfluxDB is a time series database that allows easy integration with several monitoring/graphing tools.


## Using the InfluxDB sandbox

The Sandbox is a docker based distribution for configuring a development environment.

go to `<install location>/influxdb/sandbox` and start the influxDB sandbox:

```bash
sudo ./sandbox up
```

This should also open firefox tabs. If not, then open `localhost:8888` and `localhost:3010`

Stop influxDB:

```bash
sudo ./sandbox stop
```


## Proper InfluxDB Install


Digital ocean [has a nice write-up on how to install infulxDB](https://www.digitalocean.com/community/tutorials/how-to-monitor-system-metrics-with-the-tick-stack-on-ubuntu-16-04), and other related components (Chronograf, kapacitor, telegraf)


```
systemctl start influxdb
systemctl start chronograf.service
influx
```

# Chronograf

Chronograf

- synchronized cursors in all graphs
- timeseries plots
- timestamped lists
- move and resize plots at will


- Very little cusomizatbility in plot types (only suitable for timeseries)
- autozoom sometimes a little strange


# Grafana

A more full-featured alternative to Chronograf.

- InfulxDB integration
- timeseries plots
- timestamped lists
- maps
- many visualizations for non timeseries data

## Install grafana

Dowload and install the .deb from:

```
https://grafana.com/grafana/download?platform=linux
```

start the grafana server, by default on localhost:3000:
```
sudo service grafana-server start
```

the default user name and password combinations is `adimn:admin`




## Grafana dashboard

- TODO: configure public user


## Eventlogs as annotations

Grafana does not seem to have a similar time cursor for tabular time series as Chronograf.

Eventlog entries can ba added as annotations from influx

http://docs.grafana.org/reference/annotations/
