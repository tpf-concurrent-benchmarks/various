# Automated rendering and downloading of Grafana metrics

This repository contains a helpful script to programmatically define
the metrics you want to download as .png files from Grafana

## Requirements

For the script to work, you need the following:
- A running Grafana instance with anonymous access enabled
- [Grafana Image Renderer](https://grafana.com/grafana/plugins/grafana-image-renderer/) plugin installed

## Usage

```shell
python3 download_metrics.py -p <path_to_config_file> -c <path_to_context_folder>
```

For more information, run

```shell
python3 download_metrics.py -h
```

## Configuration yaml file

### Example
```yaml
grafana_url: http://localhost:8081
dashboard_uid: grid_search_dashboard
folders:
  4-Workers:
    from: 1700111859229
    to: 1700112759229
  8-Workers:
    from: 1700115459229
    to: 1700116359229
  16-Workers:
    from: 1700119059229
    to: 1700119959229
panels:
  - CPU Usage (Workers)
  - Memory Usage (Workers)
  - Network Usage (Workers)
  - Disk Usage (Workers)
  - Per node throughput
  - Combined throughput
  - Coefficient of variation
size:
  width: 1000
  height: 400
theme: light
```