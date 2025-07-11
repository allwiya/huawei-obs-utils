# import fireducks.pandas as pd
# import pandas as pd
# from dateutil.relativedelta import relativedelta
import glob
import logging
import os
import sys
from datetime import datetime

from obs import ObsClient, SetObjectMetadataHeader

dt_now = datetime.now()

format_string = "%Y-%m-%d_%H-%M-%S"
log_file = dt_now.strftime(format_string) + ".log"


# logging.basicConfig(
#    level=logging.DEBUG,
#    filename=log_file,
#    encoding="utf-8",
#    filemode="a",
#    style="{",
#    datefmt="%Y-%m-%d %H:%M",
#    format="%(levelname)s:%(name)s:%(message)s",
#    )
logger = logging.getLogger(__name__)
logging.basicConfig(filename=log_file, encoding="utf-8", level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
# logger = logging.getLogger(__name__)
# console_handler = logging.StreamHandler()
# file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)
# formatter = logging.Formatter(
#    "{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
# )
# console_handler.setFormatter(formatter)

mark = None

logger.info("Start")

ak = "GZYXMS5FHDV5Z9DWCWQS"
sk = "RbkBHmfu6dSMifRtkfff3ZOii4AIIgCWW1u6U5TU"
server = "https://obs.sa-peru-1.myhuaweicloud.com/"

operacion = input(
    "(l) listar - (a) archivar - (i) infrecuente - (r) recover - (d) download ruta - f (download file) - (x)  Buscar buckets: "
)
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
bucket = input("Ingrese el Bucket (Presione [ENTER] para buscar en todos los buckets): ")
route = input("Ingrese la Ruta (Presione [ENTER] para la ruta inicial): ")

if len(bucket) < 2 and operacion != "x":
    sys.exit()

if operacion == "l":
    index = 0
    while True:
        resp = obsClient.listObjects(bucket, marker=mark, prefix=route, max_keys=1000)
        if resp.status < 300:
            #            print('requestId:', resp.requestId)
            print("name:", resp.body.name)
            print("prefix:", resp.body.prefix)
            #           print('max_keys:', resp.body.max_keys)
            #           print('is_truncated:', resp.body.is_truncated)
            for content in resp.body.contents:
                # print('object [' + str(index) + ']')
                print("key:", content.key)
                print("lastModified:", content.lastModified)
                # print('etag:', content.etag)
                print("size:", content.size)
                # print('owner_id:', content.owner.owner_id)
                print("owner_name:", content.owner.owner_name)
                print("storage_class:", content.storageClass)
                index += 1
        else:
            print("errorCode:", resp.errorCode)
            print("errorMessage:", resp.errorMessage)
        if resp.body.is_truncated is True:
            mark = resp.body.next_marker
        else:
            break
    print("Items Procesados:", index)
elif operacion == "a":
    index = 0
    while True:
        resp = obsClient.listObjects(bucket, marker=mark, prefix=route, max_keys=1000)
        if resp.status < 300:
            #           print('requestId:', resp.requestId)
            print("name:", resp.body.name)
            print("prefix:", resp.body.prefix)
            #           print('max_keys:', resp.body.max_keys)
            #           print('is_truncated:', resp.body.is_truncated)
            for content in resp.body.contents:
                print("key:", content.key)
                print("lastModified:", content.lastModified)
                print("storage_class:", content.storageClass)
                try:
                    # metadata = {"x-obs-storage-class":"COLD"}
                    metadata = {"storageClass": "COLD"}
                    headers = SetObjectMetadataHeader()
                    bucketName = bucket
                    objectKey = content.key
                    resp2 = obsClient.setObjectMetadata(bucketName, objectKey, metadata, headers)
                    if resp2.status < 300:
                        print("Set Object Metadata Succeeded")
                        logging.info("Set Object Metadata Succeeded")
                        print("requestId:", resp.requestId)
                        logging.info(objectKey)
                    else:
                        print("Set Object Metadata Failed")
                        logging.warning("Set Object Metadata Failed")
                        # print('requestId:', resp.requestId)
                        # logging.warning(resp.errorCode)
                        # logging.warning(resp.errorMessage)
                        logging.warning(objectKey)
                    index += 1
                except Exception as e:
                    logging.error("Set Object Metadata Failed")
                    logging.error(e)
        if resp.body.is_truncated is True:
            mark = resp.body.next_marker
        else:
            break
    print("Items Procesados:", index)
elif operacion == "i":
    index = 0
    while True:
        resp = obsClient.listObjects(bucket, marker=mark, prefix=route, max_keys=1000)
        # print(resp)
        if resp.status < 300:
            #            print('requestId:', resp.requestId)
            print("name:", resp.body.name)
            print("prefix:", resp.body.prefix)
            #            print('max_keys:', resp.body.max_keys)
            #            print('is_truncated:', resp.body.is_truncated)
            # index = 1
            for content in resp.body.contents:
                print("key:", content.key)
                print("lastModified:", content.lastModified)
                print("storage_class:", content.storageClass)
                try:
                    metadata = {"storageClass": "WARM"}
                    headers = SetObjectMetadataHeader()
                    bucketName = bucket
                    objectKey = content.key
                    resp3 = obsClient.setObjectMetadata(bucketName, objectKey, metadata, headers)
                    if resp3.status < 300:
                        print("Set Object Metadata Succeeded")
                        logger.info("Set Object Metadata Succeeded")
                        print("requestId:", resp.requestId)
                        logger.info(objectKey)
                    else:
                        print("Set Object Metadata Failed")
                        logger.warning("Set Object Metadata Failed")
                        # print('requestId:', resp.requestId)
                        # logging.warning(resp.errorCode)
                        # logging.warning(resp.errorMessage)
                        logger.warning(objectKey)
                    index += 1
                except Exception as e:
                    logger.error("Set Object Metadata Failed")
                    logger.error(e)
        if resp.body.is_truncated is True:
            mark = resp.body.next_marker
        else:
            break
    print("Items Procesados:", index)
elif operacion == "r":
    index = 0
    while True:
        resp = obsClient.listObjects(bucket, prefix=route, marker=mark, max_keys=1000)
        if resp.status < 300:
            # print('requestId:', resp.requestId)
            print("name:", resp.body.name)
            print("prefix:", resp.body.prefix)
            # print('max_keys:', resp.body.max_keys)
            # print('is_truncated:', resp.body.is_truncated)
            for content in resp.body.contents:
                print("file_name:", content.key)
                print("lastModified:", content.lastModified)
                print("storage_class:", content.storageClass)
                try:
                    bucketName = bucket
                    objectKey = content.key
                    days = 30
                    tier = "Expedited"
                    resp3 = obsClient.restoreObject(bucketName, objectKey, days, tier)
                    if resp3.status < 300:
                        print("Set Object Metadata Succeeded")
                        logger.info("Set Object Metadata Succeeded")
                        print("requestId:", resp.requestId)
                        logger.info(objectKey)
                    else:
                        print("Set Object Metadata Failed")
                        logger.warning("Set Object Metadata Failed")
                        logger.warning(objectKey)
                    index += 1
                except Exception as e:
                    logger.error("Set Object Metadata Failed")
                    logger.error(e)
        if resp.body.is_truncated is True:
            mark = resp.body.next_marker
        else:
            break
    print("Items Procesados:", index)
elif operacion == "x":
    if route == "":
        route = "."
    text = input("Ingrese la cadena del archivo a encontrar: ")
    if text == "":
        sys.exit()
    if bucket == "":
        resp = obsClient.listBuckets(True)
        if resp.status < 300:
            index2 = 1
            for bucket in resp.body.buckets:
                index = 0
                try:
                    logger.info("Found: ")
                    while True:
                        resp2 = obsClient.listObjects(bucket.name, marker=mark, prefix=route, max_keys=1000)
                        if resp2.status < 300:
                            for content in resp2.body.contents:
                                arch = content.key
                                if arch.lower().find(text) >= 0:
                                    logger.info(arch)
                                    # print('object [' + str(index) + ']')
                                    print("bucket:", resp2.body.name)
                                    print("prefix:", resp2.body.prefix)
                                    print("file_name:", arch)
                                    print("lastModified:", content.lastModified)
                                    # print('etag:', content.etag)
                                    print("size:", content.size)
                                    # print('owner_id:', content.owner.owner_id)
                                    print("owner_name:", content.owner.owner_name)
                                    print("storage_class:", content.storageClass)
                                    index += 1
                        else:
                            print("errorCode:", resp2.errorCode)
                            print("errorMessage:", resp2.errorMessage)
                        if resp2.body.is_truncated is True:
                            mark = resp2.body.next_marker
                        else:
                            break
                    index2 += 1
                except Exception as error:
                    print(error)
        else:
            print("errorCode:", resp.errorCode)
            print("errorMessage:", resp.errorMessage)
    else:
        index = 0
        logger.info("Found: ")
        while True:
            resp2 = obsClient.listObjects(bucket, marker=mark, prefix=route, max_keys=1000)
            if resp2.status < 300:
                for content in resp2.body.contents:
                    arch = content.key
                    if arch.lower().find(text) >= 0:
                        logger.info(arch)
                        print("bucket:", resp2.body.name)
                        print("prefix:", resp2.body.prefix)
                        # print('object [' + str(index) + ']')
                        print("file_name:", arch)
                        print("lastModified:", content.lastModified)
                        # print('etag:', content.etag)
                        print("size:", content.size)
                        # print('owner_id:', content.owner.owner_id)
                        print("owner_name:", content.owner.owner_name)
                        print("storage_class:", content.storageClass)
                        index += 1
            else:
                print("errorCode:", resp2.errorCode)
                print("errorMessage:", resp2.errorMessage)
            if resp2.body.is_truncated is True:
                mark = resp2.body.next_marker
            else:
                break
    print("Items Procesados:", index)
elif operacion == "d":
    index = 0
    while True:
        resp = obsClient.listObjects(bucket, marker=mark, prefix=route, max_keys=1000)
        if resp.status < 300:
            try:
                for content in resp.body.contents:
                    arch = content.key
                    try:
                        resp2 = obsClient.getObject(bucket, arch, downloadPath=arch)
                        if resp2.status < 300:
                            print("file_name:", arch)
                            print("lastModified:", content.lastModified)
                            # print('etag:', content.etag)
                            print("size:", content.size)
                            # print('owner_id:', content.owner.owner_id)
                            print("owner_name:", content.owner.owner_name)
                            print("storage_class:", content.storageClass)
                            # print('requestId:', resp2.requestId)
                            # print('url:', resp2.body.url)
                            index += 1
                        else:
                            print("errorCode:", resp2.errorCode)
                            print("errorMessage:", resp2.errorMessage)
                    except Exception as error:
                        print(error)
                        print("storage_class:", content.storageClass)
                print("errorCode:", resp.errorCode)
                print("errorMessage:", resp.errorMessage)
                if resp.body.is_truncated is True:
                    mark = resp.body.next_marker
                else:
                    break
            except Exception as error:
                print(error)
    print("Items Procesados:", index)
elif operacion == "f":
    index = 0
    try:
        resp = obsClient.getObject(bucket, route, downloadPath=route)
        if resp.status < 300:
            # print('requestId:', resp.requestId)
            print("file_name:", resp.body.url)
            index += 1
        else:
            print("errorCode:", resp.errorCode)
            print("errorMessage:", resp.errorMessage)
    except Exception as error:
        print(error)
    print("Items Procesados:", index)
