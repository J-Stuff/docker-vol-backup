# docker-vol-backup
A Docker Container that automatically backs up all all docker volumes daily and exports them to a Discord channel using a webhook.

## Usage

Deployment is made easy, using a docker-compose file. 

```yaml
version: '3.7'
services:
    docker-vol-backup:
        image: ghcr.io/j-stuff/docker-vol-backup:latest
        volumes:
            - /var/lib/docker/volumes:/volumes # Mount the docker volumes directory
        environment:
            - WEBHOOK_URL=CHANGE_ME🚨
            # Optional
            # - TZ=Europe/London # Defaults to UTC | https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
            # - BACKUP_TIME=00:00 # Defaults to 00:00 | Use 24 hour format (HH:MM)
            # - LOG_LEVEL=INFO # Defaults to INFO | DEBUG, INFO (Debugging only! This will spam your logs)
```
