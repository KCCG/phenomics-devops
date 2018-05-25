import boto3

def upload_file( filename ):
    session = boto3.Session()
    s3_client = session.client( 's3' )

    try:
        print("Uploading file:", filename)

        tc = boto3.s3.transfer.TransferConfig()
        t = boto3.s3.transfer.S3Transfer( client=s3_client,
                                          config=tc )
        t.upload_file( filename, 'phenomics-graph-db-backup', "2018-03-26.dump")


    except Exception as e:
        print ("Error uploading: %s" % ( e ))






def download_file( filename ):
    session = boto3.Session()
    s3_client = session.client( 's3' )

    try:
        print("Downloading file:", filename)

        tc = boto3.s3.transfer.TransferConfig()
        t = boto3.s3.transfer.S3Transfer( client=s3_client,
                                          config=tc )

        t.download_file('phenomics-graph-db-backup', filename, '/var/lib/neo4j/data/backup/2018-03-26.dump')

    except Exception as e:
        print ("Error downloading: %s" % ( e ))



# upload_file("2018-03-26.dump")
download_file("2018-03-26.dump")