
import logging
import os
import shutil
import time

from discord_webhook import DiscordWebhook, DiscordEmbed

def _getAllVolumePaths() -> list[str]:
    logging.debug("Getting all volume paths")
    paths = [ f.path for f in os.scandir("/volumes") if f.is_dir() ]
    logging.info(f"Found {len(paths)} volume paths")
    logging.debug(f"Volume paths: {paths}")
    return paths

def _cleanCacheDir() -> None:
    logging.debug("Cleaning cache folder")
    shutil.rmtree('./cache')
    logging.debug("Cache folder cleaned")

def _ensureCleanCacheDirExists() -> None:
    logging.debug("Ensuring cache folder exists")
    if os.path.exists('./cache'):
        logging.debug("Cache folder exists! Cleaning up...")
        shutil.rmtree('./cache')
    os.makedirs('./cache')
    logging.debug("Cache folder created")

def _archiveVolume(volumePath:str, name:str) -> str:
    if os.getenv("LOG_LEVEL") != "DEBUG":
        logging.info(f"Archiving {volumePath}... (This can take a VERY long time. If this takes more than 60 minutes, consider enabling DEBUG logging and see whats going on)")
        archive_path = f"./cache/{name}"
        shutil.make_archive(archive_path, 'zip', volumePath)
    else:
        logging.debug(f"Archiving {volumePath}... (debug logging enabled)")
        archive_path = f"./cache/{name}"
        debug_logger = logging.getLogger()
        debug_logger.setLevel(logging.DEBUG)
        shutil.make_archive(archive_path, 'zip', volumePath, logger=debug_logger)
    archive_path = f"{archive_path}.zip"
    logging.debug(f"Archived {volumePath} as {archive_path}")
    return archive_path

def _isArchiveTooLarge(archivePath: str) -> bool:
    logging.debug(f"Checking if archive {archivePath} is too large")
    size = os.path.getsize(archivePath)
    size_in_mb = size / 1024 / 1024
    logging.debug(f"Archive size: {size} ({size_in_mb}MB)")
    if size > 20000000: # 20MB
        logging.debug(f"Archive {archivePath} is too large! ({size} | {size_in_mb}MB)")
        return True
    logging.debug(f"Archive {archivePath} is not too large")
    return False

def _splitArchive(archivePath: str) -> list[str]:
    logging.info(f"Splitting archive {archivePath} into 20MB chunks")
    split_paths = []
    chunk_size = 20 * 1024 * 1024  # 20 MB in bytes
    with open(archivePath, 'rb') as file:
        index = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunk_path = f"{archivePath}.part{index}"
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            split_paths.append(chunk_path)
            index += 1
    logging.debug(f"Split archive {archivePath} into {len(split_paths)} chunks")
    logging.debug(f"Split paths: {split_paths}")
    return split_paths

def _uploadAsSingleFile(archivePath: str, time:str, name:str) -> None:
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url is None:
        logging.error("No webhook URL set! Cannot upload archive")
        return
    webhook = DiscordWebhook(url=webhook_url, username="BackupBot", rate_limit_retry=True)
    embed = DiscordEmbed(title=f"Backup - {name}", description=f"Backup of volume {name} @ <t:{time}:F>", color=242424)
    webhook.add_embed(embed)
    webhook.add_file(file=open(archivePath, 'rb').read(), filename=archivePath.split('/')[-1])
    response = webhook.execute()
    logging.info(f"Uploaded {archivePath} to Discord")

def _uploadAsMultipleFiles(archivePaths: list[str], time:str, name:str) -> None:
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url is None:
        logging.error("No webhook URL set! Cannot upload archive")
        return
    
    webhook = DiscordWebhook(url=webhook_url, username="BackupBot", rate_limit_retry=True, wait=False)
    embed = DiscordEmbed(title=f"Backup - {name}", description=f"Backup of volume {name} @ <t:{time}:F>", color=242424)
    reassemble_tool = DiscordEmbed(title="Reassemble Tool", description="Please use this file to reassemble the archive parts into a single file.", color=242424)
    webhook.add_file(file=open("resources/reassemble.py", 'rb').read(), filename="reassemble.py")
    webhook.add_embed(embed)
    webhook.add_embed(reassemble_tool)
    response = webhook.execute()


    pathCount = 0
    for path in archivePaths:
        pathCount += 1
        webhook = DiscordWebhook(url=webhook_url, username="BackupBot", rate_limit_retry=True, wait=False)
        webhook.add_file(file=open(path, 'rb').read(), filename=path.split('/')[-1])
        webhook.execute()
    logging.info(f"Uploaded {len(archivePaths)} parts of {name} to Discord")

def run_backup():
    logging.info("Starting backup...")
    volumesAsPaths = _getAllVolumePaths()
    current_unix = str(int(time.time()))
    _ensureCleanCacheDirExists()
    for volume in volumesAsPaths:
        volume_name = volume.split('/')[-1]
        archive_path = _archiveVolume(volume, volume_name)
        if _isArchiveTooLarge(archive_path):
            split_paths = _splitArchive(archive_path)
            _uploadAsMultipleFiles(split_paths, current_unix, volume_name)
        else:
            _uploadAsSingleFile(archive_path, current_unix, volume_name)
        logging.info(f"Backup of volume {volume} complete!")
        if os.getenv("LOG_LEVEL") != "DEBUG":
            _cleanCacheDir()
    logging.info("Backup complete!")