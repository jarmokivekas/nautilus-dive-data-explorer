# Grafana

## Install

```
sudo echo deb https://packagecloud.io/grafana/stable/debian/ stretch main >> /etc/apt/sources.list.d/grafana.list

sudo apt-get update
sudo apt-get install grafana
```

Got to http port 3000, login as admin:admin and change the grafana admin password (automatic prompt)

## Config

The grafana config file is in /etc/grafana/grafana.ini

Set auth.anonymous.enabled to trua, and org_name to the name of the organization with id 1 (called Main Org by default)

```
[auth.anonymous]
# enable anonymous access
enabled = true

# specify organization name that should be used for unauthenticated users
org_name = Nautilus viewers
```

For more functionality for Viewers, set the viewers_can_edit key to true.

```
# Viewers can edit/inspect dashboard settings in the browser. But not save the dashboard.
viewers_can_edit = true
```

### Eventlogs as annotations

Grafana does not have a similar time cursor for tabular time series as Chronograf. However, eventlog entries can be [added as annotations from influx](http://docs.grafana.org/reference/annotations/)



# Influx

```
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update
sudo apt-get install influxdb
```


# start services

```
sudo service grafana-server start
sudo systemctl start influxdb
```

# nautilus data crawler

```
apt-get install python3-influxdb
adduser nautilus-data
su nautilus-data
cd
git clone https://github.com/jarmokivekas/nautilus-dive-data-explorer.git
```
