"""
OBS Manager - Main class for Huawei Cloud OBS operations

Copyright 2025 CCVASS - Lima, Peru

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: contact@ccvass.com
"""
import os
import sys
from typing import Optional, List, Dict, Any, Generator, Tuple
from obs import ObsClient, SetObjectMetadataHeader
from config import Config
from logger import get_logger


class OBSManager:
    """Manager class for Huawei Cloud OBS operations"""
    
    def __init__(self, config_file: str = "obs_config.json"):
        """
        Initialize OBS Manager
        
        Args:
            config_file: Path to configuration file
        """
        self.config = Config(config_file)
        self.logger = get_logger(__name__)
        self.client: Optional[ObsClient] = None
        
        if not self.config.validate_credentials():
            self.logger.error("Invalid or missing credentials in configuration")
            raise ValueError("Invalid or missing credentials. Please check your configuration.")
        
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize OBS client with credentials"""
        try:
            self.client = ObsClient(
                access_key_id=self.config.get('access_key_id'),
                secret_access_key=self.config.get('secret_access_key'),
                server=self.config.get('server')
            )
            self.logger.info("OBS client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize OBS client: {e}")
            raise
    
    def _validate_inputs(self, bucket: str, route: str = "") -> Tuple[str, str]:
        """
        Validate and sanitize input parameters
        
        Args:
            bucket: Bucket name
            route: Object route/prefix
            
        Returns:
            Tuple of validated (bucket, route)
        """
        if not bucket or not isinstance(bucket, str):
            raise ValueError("Bucket name is required and must be a string")
        
        bucket = bucket.strip()
        route = route.strip() if route else ""
        
        return bucket, route
    
    def _paginated_list_objects(self, bucket: str, prefix: str = "", max_keys: int = None) -> Generator[Any, None, None]:
        """
        Generator for paginated object listing
        
        Args:
            bucket: Bucket name
            prefix: Object prefix filter
            max_keys: Maximum keys per request
            
        Yields:
            Object content items
        """
        if max_keys is None:
            max_keys = self.config.get('max_keys', 1000)
        
        marker = None
        
        while True:
            try:
                resp = self.client.listObjects(bucket, marker=marker, prefix=prefix, max_keys=max_keys)
                
                if resp.status >= 300:
                    self.logger.error(f"Failed to list objects: {resp.errorCode} - {resp.errorMessage}")
                    break
                
                for content in resp.body.contents:
                    yield content
                
                if not resp.body.is_truncated:
                    break
                    
                marker = resp.body.next_marker
                
            except Exception as e:
                self.logger.error(f"Error during object listing: {e}")
                break
    
    def list_objects(self, bucket: str, route: str = "") -> int:
        """
        List objects in bucket
        
        Args:
            bucket: Bucket name
            route: Object route/prefix
            
        Returns:
            Number of objects processed
        """
        bucket, route = self._validate_inputs(bucket, route)
        count = 0
        
        try:
            self.logger.info(f"Listing objects in bucket: {bucket}, prefix: {route}")
            
            for content in self._paginated_list_objects(bucket, route):
                print(f"Key: {content.key}")
                print(f"Last Modified: {content.lastModified}")
                print(f"Size: {content.size}")
                print(f"Owner: {content.owner.owner_name}")
                print(f"Storage Class: {content.storageClass}")
                print("-" * 50)
                count += 1
            
            self.logger.info(f"Listed {count} objects")
            
        except Exception as e:
            self.logger.error(f"Error listing objects: {e}")
            raise
        
        return count
    
    def change_storage_class(self, bucket: str, route: str = "", storage_class: str = "COLD") -> int:
        """
        Change storage class for objects
        
        Args:
            bucket: Bucket name
            route: Object route/prefix
            storage_class: Target storage class (COLD, WARM, STANDARD)
            
        Returns:
            Number of objects processed
        """
        bucket, route = self._validate_inputs(bucket, route)
        
        if storage_class not in ["COLD", "WARM", "STANDARD"]:
            raise ValueError("Storage class must be one of: COLD, WARM, STANDARD")
        
        count = 0
        success_count = 0
        
        try:
            self.logger.info(f"Changing storage class to {storage_class} for bucket: {bucket}, prefix: {route}")
            
            for content in self._paginated_list_objects(bucket, route):
                count += 1
                
                try:
                    metadata = {"storageClass": storage_class}
                    headers = SetObjectMetadataHeader()
                    
                    resp = self.client.setObjectMetadata(bucket, content.key, metadata, headers)
                    
                    if resp.status < 300:
                        self.logger.info(f"Successfully changed storage class for: {content.key}")
                        success_count += 1
                        print(f"✓ {content.key} -> {storage_class}")
                    else:
                        self.logger.warning(f"Failed to change storage class for: {content.key}")
                        print(f"✗ Failed: {content.key}")
                        
                except Exception as e:
                    self.logger.error(f"Error changing storage class for {content.key}: {e}")
                    print(f"✗ Error: {content.key} - {e}")
            
            self.logger.info(f"Processed {count} objects, {success_count} successful")
            
        except Exception as e:
            self.logger.error(f"Error changing storage class: {e}")
            raise
        
        return count
    
    def restore_objects(self, bucket: str, route: str = "", days: int = None, tier: str = None) -> int:
        """
        Restore archived objects
        
        Args:
            bucket: Bucket name
            route: Object route/prefix
            days: Number of days to keep restored
            tier: Restore tier (Expedited, Standard, Bulk)
            
        Returns:
            Number of objects processed
        """
        bucket, route = self._validate_inputs(bucket, route)
        
        if days is None:
            days = self.config.get('restore_days', 30)
        if tier is None:
            tier = self.config.get('restore_tier', 'Expedited')
        
        if tier not in ["Expedited", "Standard", "Bulk"]:
            raise ValueError("Restore tier must be one of: Expedited, Standard, Bulk")
        
        count = 0
        success_count = 0
        
        try:
            self.logger.info(f"Restoring objects for {days} days with {tier} tier in bucket: {bucket}, prefix: {route}")
            
            for content in self._paginated_list_objects(bucket, route):
                count += 1
                
                try:
                    resp = self.client.restoreObject(bucket, content.key, days, tier)
                    
                    if resp.status < 300:
                        self.logger.info(f"Successfully initiated restore for: {content.key}")
                        success_count += 1
                        print(f"✓ Restore initiated: {content.key}")
                    else:
                        self.logger.warning(f"Failed to restore: {content.key}")
                        print(f"✗ Failed: {content.key}")
                        
                except Exception as e:
                    self.logger.error(f"Error restoring {content.key}: {e}")
                    print(f"✗ Error: {content.key} - {e}")
            
            self.logger.info(f"Processed {count} objects, {success_count} restore requests initiated")
            
        except Exception as e:
            self.logger.error(f"Error restoring objects: {e}")
            raise
        
        return count
    
    def download_objects(self, bucket: str, route: str = "", download_path: str = None) -> int:
        """
        Download objects from bucket
        
        Args:
            bucket: Bucket name
            route: Object route/prefix
            download_path: Local download path (optional)
            
        Returns:
            Number of objects downloaded
        """
        bucket, route = self._validate_inputs(bucket, route)
        count = 0
        success_count = 0
        
        try:
            self.logger.info(f"Downloading objects from bucket: {bucket}, prefix: {route}")
            
            for content in self._paginated_list_objects(bucket, route):
                count += 1
                
                try:
                    local_path = download_path or content.key
                    
                    # Create directory if needed
                    local_dir = os.path.dirname(local_path)
                    if local_dir and not os.path.exists(local_dir):
                        os.makedirs(local_dir)
                    
                    resp = self.client.getObject(bucket, content.key, downloadPath=local_path)
                    
                    if resp.status < 300:
                        self.logger.info(f"Successfully downloaded: {content.key}")
                        success_count += 1
                        print(f"✓ Downloaded: {content.key} -> {local_path}")
                    else:
                        self.logger.warning(f"Failed to download: {content.key}")
                        print(f"✗ Failed: {content.key}")
                        
                except Exception as e:
                    self.logger.error(f"Error downloading {content.key}: {e}")
                    print(f"✗ Error: {content.key} - {e}")
            
            self.logger.info(f"Processed {count} objects, {success_count} downloaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error downloading objects: {e}")
            raise
        
        return count
    
    def download_single_file(self, bucket: str, object_key: str, download_path: str = None) -> bool:
        """
        Download a single file
        
        Args:
            bucket: Bucket name
            object_key: Object key to download
            download_path: Local download path (optional)
            
        Returns:
            True if successful, False otherwise
        """
        bucket, object_key = self._validate_inputs(bucket, object_key)
        
        try:
            local_path = download_path or object_key
            
            # Create directory if needed
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir)
            
            resp = self.client.getObject(bucket, object_key, downloadPath=local_path)
            
            if resp.status < 300:
                self.logger.info(f"Successfully downloaded: {object_key}")
                print(f"✓ Downloaded: {object_key} -> {local_path}")
                return True
            else:
                self.logger.error(f"Failed to download {object_key}: {resp.errorCode} - {resp.errorMessage}")
                print(f"✗ Failed: {object_key}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error downloading {object_key}: {e}")
            print(f"✗ Error: {object_key} - {e}")
            return False
    
    def search_objects(self, search_text: str, bucket: str = "", route: str = "") -> int:
        """
        Search for objects by name
        
        Args:
            search_text: Text to search for in object names
            bucket: Bucket name (empty to search all buckets)
            route: Object route/prefix
            
        Returns:
            Number of matching objects found
        """
        if not search_text:
            raise ValueError("Search text is required")
        
        search_text = search_text.lower()
        count = 0
        
        try:
            if not bucket:
                # Search in all buckets
                resp = self.client.listBuckets(True)
                if resp.status < 300:
                    for bucket_info in resp.body.buckets:
                        count += self._search_in_bucket(bucket_info.name, route, search_text)
                else:
                    self.logger.error(f"Failed to list buckets: {resp.errorCode} - {resp.errorMessage}")
            else:
                # Search in specific bucket
                bucket, route = self._validate_inputs(bucket, route)
                count = self._search_in_bucket(bucket, route, search_text)
            
            self.logger.info(f"Search completed. Found {count} matching objects")
            
        except Exception as e:
            self.logger.error(f"Error during search: {e}")
            raise
        
        return count
    
    def _search_in_bucket(self, bucket: str, route: str, search_text: str) -> int:
        """
        Search for objects in a specific bucket
        
        Args:
            bucket: Bucket name
            route: Object route/prefix
            search_text: Text to search for (lowercase)
            
        Returns:
            Number of matching objects found
        """
        count = 0
        
        try:
            for content in self._paginated_list_objects(bucket, route):
                if search_text in content.key.lower():
                    count += 1
                    print(f"Bucket: {bucket}")
                    print(f"File: {content.key}")
                    print(f"Last Modified: {content.lastModified}")
                    print(f"Size: {content.size}")
                    print(f"Owner: {content.owner.owner_name}")
                    print(f"Storage Class: {content.storageClass}")
                    print("-" * 50)
                    
        except Exception as e:
            self.logger.error(f"Error searching in bucket {bucket}: {e}")
        
        return count
    
    def close(self):
        """Close OBS client connection"""
        if self.client:
            try:
                self.client.close()
                self.logger.info("OBS client connection closed")
            except Exception as e:
                self.logger.error(f"Error closing OBS client: {e}")
