#!/usr/bin/env python3
"""
Secure OBS Manager with Multi-Level Security
Enhanced version of OBSManager with security level verification
"""

import os
from obs import ObsClient
from config import Config
from logger import get_logger
from typing import Generator, Tuple, Optional
import logging

# Try to import security levels (optional)
try:
    from security_levels import MultiLevelSecurity, SecurityLevel

    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False
    print("⚠️  Security levels module not available. Running without multi-level security.")

logger = get_logger(__name__)


class SecureOBSManager:
    """Enhanced OBS Manager with multi-level security"""

    def __init__(self, config_file: str = "obs_config.json", enable_security_levels: bool = True):
        """
        Initialize Secure OBS Manager

        Args:
            config_file: Configuration file path
            enable_security_levels: Enable multi-level security system
        """
        self.config = Config(config_file)
        self.obs_client = None
        self.logger = logger

        # Initialize security levels if available and enabled
        self._security_levels = None
        if SECURITY_AVAILABLE and enable_security_levels:
            try:
                self._security_levels = MultiLevelSecurity()
                self.logger.info("Multi-level security system initialized")
            except Exception as e:
                self.logger.warning(f"Could not initialize security levels: {e}")

        self._initialize_client()

    def _initialize_client(self):
        """Initialize OBS client with configuration"""
        try:
            if not self.config.validate_credentials():
                raise ValueError("Invalid or missing credentials in configuration")

            self.obs_client = ObsClient(
                access_key_id=self.config.get("access_key_id"),
                secret_access_key=self.config.get("secret_access_key"),
                server=self.config.get("server"),
                region=self.config.get("region", "sa-peru-1"),
            )

            self.logger.info("OBS client initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize OBS client: {e}")
            raise

    def _validate_inputs(self, bucket: str, route: str = "") -> Tuple[str, str]:
        """Validate and sanitize input parameters"""
        if not bucket or not isinstance(bucket, str):
            raise ValueError("Bucket name must be a non-empty string")

        bucket = bucket.strip()
        route = route.strip() if route else ""

        return bucket, route

    def _verify_security_access(self, operation: str, details: str = "") -> bool:
        """Verify security access for operation"""
        if not self._security_levels:
            return True  # No security levels configured

        # Verify access level
        if not self._security_levels.verify_access(operation):
            return False

        # Require confirmation for sensitive operations
        if not self._security_levels.require_confirmation(operation, details):
            self.logger.info(f"Operation '{operation}' cancelled by user")
            return False

        return True

    def _paginated_list_objects(self, bucket: str, prefix: str = "", max_keys: int = None) -> Generator:
        """Generator for paginated object listing"""
        if max_keys is None:
            max_keys = self.config.get("max_keys", 1000)

        marker = None

        while True:
            try:
                resp = self.obs_client.listObjects(bucketName=bucket, prefix=prefix, marker=marker, max_keys=max_keys)

                if resp.status < 300:
                    contents = resp.body.contents if resp.body.contents else []

                    for content in contents:
                        yield content

                    # Check if there are more objects
                    if resp.body.isTruncated:
                        marker = resp.body.nextMarker
                    else:
                        break
                else:
                    self.logger.error(f"Error listing objects: {resp.errorCode} - {resp.errorMessage}")
                    break

            except Exception as e:
                self.logger.error(f"Error during object listing: {e}")
                break

    def list_objects(self, bucket: str, route: str = "") -> int:
        """
        List objects in bucket (READ_ONLY level)

        Args:
            bucket: Bucket name
            route: Object route/prefix

        Returns:
            Number of objects processed
        """
        # Security check
        if not self._verify_security_access("list", f"List objects in bucket '{bucket}'"):
            self.logger.error("Access denied for list operation")
            return 0

        bucket, route = self._validate_inputs(bucket, route)
        count = 0

        try:
            self.logger.info(f"Listing objects in bucket: {bucket}, prefix: {route}")

            for content in self._paginated_list_objects(bucket, route):
                print(f"📄 Key: {content.key}")
                print(f"   Last Modified: {content.lastModified}")
                print(f"   Size: {content.size} bytes")
                print(f"   Owner: {content.owner.owner_name}")
                print(f"   Storage Class: {content.storageClass}")
                print("-" * 50)
                count += 1

            self.logger.info(f"Listed {count} objects")
            print(f"✅ Total objects listed: {count}")

        except Exception as e:
            self.logger.error(f"Error listing objects: {e}")
            print(f"❌ Error listing objects: {e}")
            return 0

        return count

    def change_storage_class(self, bucket: str, route: str = "", storage_class: str = "COLD") -> int:
        """
        Change storage class for objects (STANDARD level)

        Args:
            bucket: Bucket name
            route: Object route/prefix
            storage_class: Target storage class (COLD, WARM, STANDARD)

        Returns:
            Number of objects processed
        """
        # Security check
        operation_details = f"Change storage class to {storage_class} for objects in bucket '{bucket}'"
        if route:
            operation_details += f" with prefix '{route}'"

        if not self._verify_security_access("archive", operation_details):
            self.logger.error("Access denied for storage class change operation")
            return 0

        bucket, route = self._validate_inputs(bucket, route)
        count = 0

        try:
            self.logger.info(f"Changing storage class to {storage_class} in bucket: {bucket}, prefix: {route}")

            for content in self._paginated_list_objects(bucket, route):
                try:
                    # Skip if already in target storage class
                    if content.storageClass == storage_class:
                        print(f"⏭️  Skipping {content.key} (already {storage_class})")
                        continue

                    # Copy object with new storage class
                    resp = self.obs_client.copyObject(
                        sourceBucketName=bucket,
                        sourceObjectKey=content.key,
                        destBucketName=bucket,
                        destObjectKey=content.key,
                        storageClass=storage_class,
                    )

                    if resp.status < 300:
                        print(f"✅ Changed {content.key} to {storage_class}")
                        count += 1
                    else:
                        print(f"❌ Failed to change {content.key}: {resp.errorMessage}")

                except Exception as e:
                    print(f"❌ Error processing {content.key}: {e}")
                    continue

            self.logger.info(f"Changed storage class for {count} objects")
            print(f"✅ Total objects processed: {count}")

        except Exception as e:
            self.logger.error(f"Error changing storage class: {e}")
            print(f"❌ Error changing storage class: {e}")
            return 0

        return count

    def restore_objects(self, bucket: str, route: str = "", days: int = None, tier: str = None) -> int:
        """
        Restore archived objects (STANDARD level)

        Args:
            bucket: Bucket name
            route: Object route/prefix
            days: Days to keep restored
            tier: Restore tier (Expedited, Standard, Bulk)

        Returns:
            Number of objects processed
        """
        # Security check
        operation_details = f"Restore objects in bucket '{bucket}'"
        if route:
            operation_details += f" with prefix '{route}'"
        operation_details += f" for {days or 30} days using {tier or 'Expedited'} tier"

        if not self._verify_security_access("restore", operation_details):
            self.logger.error("Access denied for restore operation")
            return 0

        bucket, route = self._validate_inputs(bucket, route)

        if days is None:
            days = self.config.get("restore_days", 30)
        if tier is None:
            tier = self.config.get("restore_tier", "Expedited")

        count = 0

        try:
            self.logger.info(f"Restoring objects in bucket: {bucket}, prefix: {route}, days: {days}, tier: {tier}")

            for content in self._paginated_list_objects(bucket, route):
                try:
                    # Only restore COLD storage objects
                    if content.storageClass != "COLD":
                        print(f"⏭️  Skipping {content.key} (not in COLD storage)")
                        continue

                    resp = self.obs_client.restoreObject(bucketName=bucket, objectKey=content.key, days=days, tier=tier)

                    if resp.status < 300:
                        print(f"✅ Restore initiated for {content.key}")
                        count += 1
                    else:
                        print(f"❌ Failed to restore {content.key}: {resp.errorMessage}")

                except Exception as e:
                    print(f"❌ Error processing {content.key}: {e}")
                    continue

            self.logger.info(f"Initiated restore for {count} objects")
            print(f"✅ Total restore operations initiated: {count}")

        except Exception as e:
            self.logger.error(f"Error restoring objects: {e}")
            print(f"❌ Error restoring objects: {e}")
            return 0

        return count

    def download_objects(self, bucket: str, route: str = "", download_path: str = None) -> int:
        """
        Download objects from bucket (READ_ONLY level)

        Args:
            bucket: Bucket name
            route: Object route/prefix
            download_path: Local download path

        Returns:
            Number of objects downloaded
        """
        # Security check
        operation_details = f"Download objects from bucket '{bucket}'"
        if route:
            operation_details += f" with prefix '{route}'"
        if download_path:
            operation_details += f" to '{download_path}'"

        if not self._verify_security_access("download", operation_details):
            self.logger.error("Access denied for download operation")
            return 0

        bucket, route = self._validate_inputs(bucket, route)

        if download_path is None:
            download_path = f"./downloads_{bucket}"

        # Create download directory
        os.makedirs(download_path, exist_ok=True)

        count = 0

        try:
            self.logger.info(f"Downloading objects from bucket: {bucket}, prefix: {route}")

            for content in self._paginated_list_objects(bucket, route):
                try:
                    # Create local file path
                    local_file = os.path.join(download_path, content.key.replace("/", os.sep))
                    local_dir = os.path.dirname(local_file)

                    # Create directory if needed
                    if local_dir:
                        os.makedirs(local_dir, exist_ok=True)

                    # Download object
                    resp = self.obs_client.getObject(bucketName=bucket, objectKey=content.key, downloadPath=local_file)

                    if resp.status < 300:
                        print(f"✅ Downloaded {content.key} to {local_file}")
                        count += 1
                    else:
                        print(f"❌ Failed to download {content.key}: {resp.errorMessage}")

                except Exception as e:
                    print(f"❌ Error downloading {content.key}: {e}")
                    continue

            self.logger.info(f"Downloaded {count} objects")
            print(f"✅ Total objects downloaded: {count}")

        except Exception as e:
            self.logger.error(f"Error downloading objects: {e}")
            print(f"❌ Error downloading objects: {e}")
            return 0

        return count

    def search_objects(self, search_text: str, bucket: str = "", route: str = "") -> int:
        """
        Search objects by name (READ_ONLY level)

        Args:
            search_text: Text to search for
            bucket: Bucket name (empty for all buckets)
            route: Object route/prefix

        Returns:
            Number of objects found
        """
        # Security check
        operation_details = f"Search for objects containing '{search_text}'"
        if bucket:
            operation_details += f" in bucket '{bucket}'"
        else:
            operation_details += " in all buckets"

        if not self._verify_security_access("search", operation_details):
            self.logger.error("Access denied for search operation")
            return 0

        if not search_text:
            raise ValueError("Search text cannot be empty")

        count = 0

        try:
            if bucket:
                # Search in specific bucket
                bucket, route = self._validate_inputs(bucket, route)
                count = self._search_in_bucket(bucket, route, search_text)
            else:
                # Search in all buckets
                resp = self.obs_client.listBuckets()
                if resp.status < 300:
                    for bucket_info in resp.body.buckets:
                        bucket_count = self._search_in_bucket(bucket_info.name, route, search_text)
                        count += bucket_count
                else:
                    print(f"❌ Error listing buckets: {resp.errorMessage}")

            print(f"✅ Total objects found: {count}")

        except Exception as e:
            self.logger.error(f"Error searching objects: {e}")
            print(f"❌ Error searching objects: {e}")
            return 0

        return count

    def _search_in_bucket(self, bucket: str, route: str, search_text: str) -> int:
        """Search for objects in a specific bucket"""
        count = 0
        search_lower = search_text.lower()

        try:
            for content in self._paginated_list_objects(bucket, route):
                if search_lower in content.key.lower():
                    print(f"🔍 Found: {bucket}/{content.key}")
                    print(f"   Size: {content.size} bytes")
                    print(f"   Modified: {content.lastModified}")
                    print(f"   Storage Class: {content.storageClass}")
                    print()
                    count += 1

        except Exception as e:
            self.logger.error(f"Error searching in bucket {bucket}: {e}")

        return count

    def delete_objects(self, bucket: str, route: str = "", confirm: bool = False) -> int:
        """
        Delete objects from bucket (DESTRUCTIVE level)

        Args:
            bucket: Bucket name
            route: Object route/prefix
            confirm: Skip confirmation if True

        Returns:
            Number of objects deleted
        """
        # Security check
        operation_details = f"DELETE objects from bucket '{bucket}'"
        if route:
            operation_details += f" with prefix '{route}'"
        operation_details += " - THIS ACTION CANNOT BE UNDONE!"

        if not self._verify_security_access("delete", operation_details):
            self.logger.error("Access denied for delete operation")
            return 0

        # Additional confirmation for destructive operations
        if not confirm:
            print(f"\n⚠️  DESTRUCTIVE OPERATION WARNING ⚠️")
            print(f"You are about to DELETE objects from bucket '{bucket}'")
            if route:
                print(f"With prefix: '{route}'")
            print("THIS ACTION CANNOT BE UNDONE!")

            confirmation = input("Type 'DELETE' to confirm: ").strip()
            if confirmation != "DELETE":
                print("❌ Operation cancelled")
                return 0

        bucket, route = self._validate_inputs(bucket, route)
        count = 0

        try:
            self.logger.warning(f"DESTRUCTIVE: Deleting objects in bucket: {bucket}, prefix: {route}")

            # Collect objects to delete
            objects_to_delete = []
            for content in self._paginated_list_objects(bucket, route):
                objects_to_delete.append(content.key)

            if not objects_to_delete:
                print("ℹ️  No objects found to delete")
                return 0

            print(f"Found {len(objects_to_delete)} objects to delete")

            # Delete objects in batches
            batch_size = 1000
            for i in range(0, len(objects_to_delete), batch_size):
                batch = objects_to_delete[i : i + batch_size]

                # Prepare delete request
                delete_objects = [{"key": key} for key in batch]

                resp = self.obs_client.deleteObjects(bucketName=bucket, deleteObjects=delete_objects)

                if resp.status < 300:
                    batch_count = len(batch)
                    count += batch_count
                    print(f"✅ Deleted batch of {batch_count} objects")
                else:
                    print(f"❌ Failed to delete batch: {resp.errorMessage}")

            self.logger.warning(f"DESTRUCTIVE: Deleted {count} objects")
            print(f"✅ Total objects deleted: {count}")

        except Exception as e:
            self.logger.error(f"Error deleting objects: {e}")
            print(f"❌ Error deleting objects: {e}")
            return 0

        return count

    def setup_security_levels(self):
        """Setup multi-level security system"""
        if not SECURITY_AVAILABLE:
            print("❌ Security levels module not available")
            return False

        if not self._security_levels:
            self._security_levels = MultiLevelSecurity()

        return self._security_levels.setup_security_levels()

    def list_security_levels(self):
        """List configured security levels"""
        if not self._security_levels:
            print("ℹ️  Multi-level security not configured")
            return

        self._security_levels.list_security_levels()

    def close(self):
        """Close OBS client connection"""
        if self.obs_client:
            try:
                self.obs_client.close()
                self.logger.info("OBS client connection closed")
            except Exception as e:
                self.logger.error(f"Error closing OBS client: {e}")


# Compatibility alias
OBSManager = SecureOBSManager
