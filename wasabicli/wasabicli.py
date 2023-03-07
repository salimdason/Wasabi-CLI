import concurrent
import boto3
from time import sleep
import botocore.config
from wasabicli.wasabicli.utils.formatter import indicators
from concurrent.futures import ThreadPoolExecutor



class WasabiPurge:
    def __init__(self, ACCESS_KEY_ID, SECRET_ACCESS_KEY, ENDPOINT, BUCKET_NAME):
        self.accessKey = ACCESS_KEY_ID
        self.secretAccessKey = SECRET_ACCESS_KEY
        self.endPoint = ENDPOINT
        self.bucketName = BUCKET_NAME

        self.config = botocore.config.Config(
            retries=dict(max_attempts=10),
            connect_timeout=120,
            read_timeout=120,
            max_pool_connections=90,
        )

        self.S3Resource = boto3.resource(
            "s3",
            endpoint_url=self.endPoint,
            aws_access_key_id=self.accessKey,
            aws_secret_access_key=self.secretAccessKey,
            config=self.config,
        )

        self.S3Client = boto3.resource(
            "s3",
            endpoint_url=self.endPoint,
            aws_access_key_id=self.accessKey,
            aws_secret_access_key=self.secretAccessKey,
            config=self.config,
        )

        self.bucket = self.S3Resource.Bucket(self.bucketName)

    def deleteNonCurrents(self):
        print(
            f"{indicators.HEADER}You have chosen to delete Non-current Objects!{indicators.ENDC}"
        )
        bucket = self.S3Resource.Bucket(self.bucketName)
        counter = 0
        paginator = self.S3Resource.meta.client.get_paginator("list_object_versions")

        print(f"{indicators.HEADER}Script is starting. Please wait...{indicators.ENDC}")
        for page in paginator.paginate(Bucket=self.bucketName):
            objects_to_delete = []
            for version in page.get("Versions", []):
                if version["IsLatest"] == False:
                    objects_to_delete.append(
                        {"VersionId": version["VersionId"], "Key": version["Key"]}
                    )
                if len(objects_to_delete) == 50000:
                    bucket.delete_objects(Delete={"Objects": objects_to_delete})
                    for i in range(len(objects_to_delete)):
                        print(
                            f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting non-current objects: {i + 1} out of {len(objects_to_delete)}{indicators.ENDC}",
                            end="",
                        )
                        sleep(0.01)
                    objects_to_delete = []
                    counter += 1
            if len(objects_to_delete) > 0:
                bucket.delete_objects(Delete={"Objects": objects_to_delete})
                for i in range(len(objects_to_delete)):
                    print(
                        f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting non-current objects: {i + 1} out of {len(objects_to_delete)}{indicators.ENDC}",
                        end="",
                    )
                    sleep(0.01)
                objects_to_delete = []
                counter += 1

    def deleteObjects(self):
        # print(f"{indicators.HEADER}You have chosen to delete Objects!{indicators.ENDC}")
        # Delete objects in batches of 50K
        counter = 0
        objects_to_delete = []
        for obj in self.bucket.objects.all():
            objects_to_delete.append({"Key": obj.key})
            if len(objects_to_delete) == 50000:
                self.bucket.delete_objects(Delete={"Objects": objects_to_delete})
                for i in range(len(objects_to_delete)):
                    print(
                        f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting objects: {i + 1} out of {len(objects_to_delete)}{indicators.ENDC}",
                        end="",
                    )
                    sleep(0.01)
                objects_to_delete = []
                counter += 1
        if len(objects_to_delete) > 0:
            self.bucket.delete_objects(Delete={"Objects": objects_to_delete})
            for i in range(len(objects_to_delete)):
                print(
                    f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting objects: {i + 1} out of {len(objects_to_delete)}{indicators.ENDC}",
                    end="",
                )
                sleep(0.01)
            counter += 1

        # Delete the bucket
        # bucket.delete()
        print("\nObjects deleted successfully!")

    def deleteObjectsV2(self):
        # Delete objects in batches of 50K
        counter = 1
        objects_to_delete = []
        for obj in self.bucket.objects.all():
            objects_to_delete.append({"Key": obj.key})
            if len(objects_to_delete) == 50000:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = []
                    for i, obj in enumerate(objects_to_delete):
                        futures.append(executor.submit(self.bucket.delete_objects, Delete={"Objects": [obj]}))
                    for i, future in enumerate(concurrent.futures.as_completed(futures)):
                        print(f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting objects: {i + 1} out of {len(objects_to_delete)}{indicators.ENDC}", end="")
                objects_to_delete = []
                counter += 1
        if len(objects_to_delete) > 0:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for i, obj in enumerate(objects_to_delete):
                    futures.append(executor.submit(self.bucket.delete_objects, Delete={"Objects": [obj]}))
                for i, future in enumerate(concurrent.futures.as_completed(futures)):
                    print(f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting objects: {i + 1} out of {len(futures)}{indicators.ENDC}", end="")
            counter += 1
        print("\nObjects deleted successfully!")

    def deleteVersionsandObjects(self):

        self.deleteNonCurrentsV2()
        self.deleteObjectsV2()

    def purgeDeleteMarkers(self):
        print(
            f"{indicators.HEADER}You have chosen to purge all delete markers (DMs)!{indicators.ENDC}"
        )
        bucket_name = self.bucketName

        # Paginate through all the delete markers in the bucket
        delete_markers = []

        paginator = self.S3Resource.meta.client.get_paginator("list_object_versions")
        for page in paginator.paginate(Bucket=bucket_name):
            for version in page.get("Versions", []):
                if version.get("IsDeleteMarker"):
                    delete_markers.append(
                        {
                            "VersionId": version.get("VersionId"),
                            "Key": version.get("Key"),
                        }
                    )

                    # Delete a batch of 50000 delete markers
                    if len(delete_markers) == 50000:
                        for delete_marker in delete_markers:
                            self.S3Client.delete_object(
                                Bucket=bucket_name,
                                Key=delete_marker["Key"],
                                VersionId=delete_marker["VersionId"],
                            )
                        delete_markers = []

        # Delete any remaining delete markers
        for delete_marker in delete_markers:
            self.S3Resource.delete_object(
                Bucket=bucket_name,
                Key=delete_marker["Key"],
                VersionId=delete_marker["VersionId"],
            )

        print(
            f"{indicators.OKBLUE}Delete Markets Successfully Purged from {self.bucketName}{indicators.OKBLUE}"
        )

    def deleteBucket(self):

        self.deleteVersionsandObjects()
        self.purgeDeleteMarkers()

        bucket = self.S3Resource.Bucket(self.bucketName)

        # Ensure nothing else remains
        bucket.objects.all().delete()

        # Delete the bucket
        bucket.delete()

        print(f"{indicators.HEADER}Bucket deletion successful{indicators.ENDC}")

    def deleteNonCurrentsV2(self):
        # print(
        #     f"{indicators.HEADER}You have chosen to delete Non-current Objects!{indicators.ENDC}"
        # )
        bucket = self.S3Resource.Bucket(self.bucketName)
        counter = 1
        deleted = 0
        paginator = self.S3Resource.meta.client.get_paginator("list_object_versions")

        print(f"{indicators.HEADER}Script is starting. Please wait...{indicators.ENDC}")
        with ThreadPoolExecutor(max_workers=50) as executor:
            for page in paginator.paginate(Bucket=self.bucketName):
                objects_to_delete = []
                futures = []
                for version in page.get("Versions", []):
                    if version["IsLatest"] == False:
                        objects_to_delete.append(
                            {"VersionId": version["VersionId"], "Key": version["Key"]}
                        )
                    if len(objects_to_delete) == 50000:
                        # print(f"Deleted so far: {deleted}\n")
                        future = executor.submit(
                            self.bucket.delete_objects,
                            Delete={"Objects": objects_to_delete},
                        )
                        futures.append(future)
                        deleted += len(objects_to_delete)
                        objects_to_delete = []

                        counter += 1
                        for i in range(deleted):
                            print(
                                f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting non-current objects: {deleted} total deletions{indicators.ENDC}",
                                end="",
                            )
                            sleep(0.01)
                        futures = []
                # batch_size
                if len(objects_to_delete) > 0:
                    # print(f"Number of deletions == {deleted}")
                    future = executor.submit(
                        self.bucket.delete_objects,
                        Delete={"Objects": objects_to_delete},
                    )
                    futures.append(future)
                    deleted += len(objects_to_delete)
                    objects_to_delete = []
                    counter += 1
                    for i in range(deleted):
                        print(
                            f"\r{indicators.OKGREEN}Batch Number [{counter}] <<<--->>> Deleting non-current objects: {deleted} total deletions{indicators.ENDC}",
                            end="",
                        )
                        sleep(0.01)
                    futures = []






