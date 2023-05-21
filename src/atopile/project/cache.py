import contextlib
import functools
import hashlib
import pickle
import uuid
from pathlib import Path
from typing import Callable, Dict, List

import yaml

from atopile.project.project import Project


class CachedAsset:
    def __init__(self, manager: "CacheManager", path: Path, loader: Callable):
        self.path = path
        self.manager = manager
        self.loader = loader

        self.cache_data = self.manager.manifest_data.setdefault(self.cache_id, {})
        self.cache_data["path"] = self.snapshot_path

        self._snapshot = None

    @functools.cached_property
    def cache_id(self) -> str:
        path_as_bytes = str(self.path).encode('utf-8')
        hashed_path = hashlib.blake2b(path_as_bytes, digest_size=16).digest()
        return str(uuid.UUID(bytes=hashed_path))

    @property
    def snapshot_time(self) -> float:
        return self.cache_data.get('snapshot_time', 0)

    @snapshot_time.setter
    def snapshot_time(self, value: float):
        self.cache_data['snapshot_time'] = value

    @property
    def snapshot_path(self) -> Path:
        return self.manager.project.cache_dir / self.cache_id

    def get_src_modified_time(self):
        return self.path.stat().st_mtime

    def load_src(self):
        self._snapshot = self.loader(self.path)
        self.snapshot_time = self.get_src_modified_time()

    def save(self):
        with open(self.snapshot_path, 'wb') as f:
            pickle.dump(self._snapshot, f)

    def get(self) -> object:
        if self.snapshot_time >= self.get_src_modified_time():
            try:
                with open(self.snapshot_path, 'rb') as f:
                    self._snapshot = pickle.load(f)
            except FileNotFoundError:
                self.load_src()
        else:
            self.load_src()
        return self._snapshot

class CacheManager:
    def __init__(self, project: Project):
        self.project = project
        self.cache_dir = self.project.cache_dir
        self.assets: List[CachedAsset] = []
        self.manifest_data: Dict[str, dict] = {}
        self.loaded = False

    def load(self):
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.project.cache_manifest.exists():
            with self.project.cache_manifest.open() as f:
                self.manifest_data = yaml.safe_load(f)
        else:
            self.manifest_data = {}
        self.loaded = True

    def purge_untouched(self):
        touched_entries: List[str] = [a.cache_id for a in self.assets]
        untouched_entries: List[str] = []
        for manifest_key in list[self.manifest_data.keys()]:
            if manifest_key not in touched_entries:
                del self.manifest_data[manifest_key]
                untouched_entries.append(manifest_key)
        for entry in untouched_entries:
            (self.cache_dir / entry).unlink()

    def save(self, purge_untouched: bool = True):
        if not self.loaded:
            raise RuntimeError('cache manager is not loaded')

        for asset in self.assets:
            asset.save()

        if purge_untouched:
            self.purge_untouched()

        with self.project.cache_manifest.open('w') as f:
            yaml.dump(self.manifest_data, f)

    def get(self, path: Path, loader: Callable) -> object:
        if not self.loaded:
            raise RuntimeError('cache manager is not loaded')

        # first try return it from the cache
        for asset in self.assets:
            if asset.path == path:
                return asset.get()

        # otherwise load it and add it to the cache
        asset = CachedAsset(self, path, loader)
        self.assets.append(asset)
        return asset.get()

    @contextlib.contextmanager
    def open(self):
        self.load()
        yield
        self.save()
