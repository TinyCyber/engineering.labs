import logging
import hashlib
import asyncio
import pickle
from pathlib import Path
from typing import Mapping, Union, Any

import pandas as pd


def file_exists(file_path: Path) -> bool:
    if file_path.exists():
        if not file_path.is_file():
            raise ValueError(f"{str(file_path)} already exists, but it is not a file.")
        else:
            logging.info(f"{str(file_path)} already exists.")
            return True
    else:
        return False


def verify_checksum(file_path: Path, checksum: str) -> bool:
    if checksum == "skip":
        logging.warning(f"Skip checksum verification for {str(file_path)}.")
        return True
    logging.info(f"Checking hash for {str(file_path)}, should be {checksum}")
    hasher = hashlib.new("sha256")
    buffer = bytearray(16 * 1024 * 1024)  # 16 MB
    view = memoryview(buffer)
    with file_path.open("rb", buffering=0) as stream:
        read = stream.readinto(buffer)
        while read:
            hasher.update(view[:read])
            read = stream.readinto(buffer)
    got_checksum = hasher.hexdigest()
    logging.info(f"Got {got_checksum} " + ("(match!)" if got_checksum == checksum else "(don't match!)"))
    return got_checksum == checksum


async def run_subproc(exe: str, *args: str) -> None:
    logging.info(f"Running '{exe} {' '.join(args)}'")
    subproc = await asyncio.create_subprocess_exec(exe, *args)
    try:
        return_code = await subproc.wait()
        if return_code != 0:
            raise SystemExit(return_code)
    finally:
        if subproc.returncode is None:
            # Kill process if not finished
            # (e.g. if KeyboardInterrupt or cancellation was received)
            subproc.kill()
            await subproc.wait()


def dump(dump_root: Path, objects: Mapping[str, Union[pd.DataFrame, Any]]) -> None:
    if dump_root.exists():
        if not dump_root.is_dir():
            raise ValueError(f"{dump_root} is not a directory.")
    else:
        dump_root.mkdir(parents=True, exist_ok=True)
    for obj_name, obj in objects.items():
        file_path = dump_root / obj_name
        logging.info(f"Saving {obj_name} as {str(file_path)}")
        if type(obj) == pd.DataFrame:
            obj.to_pickle(str(file_path))
        else:
            with open(file_path, 'wb') as fd:
                pickle.dump(obj=obj, file=fd, protocol=pickle.HIGHEST_PROTOCOL)
