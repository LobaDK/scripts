import os
from math import ceil

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ['https://www.googleapis.com/auth/youtube.readonly',
          'https://www.googleapis.com/auth/youtube.upload']

def main():

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_oauth.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    search_query = str(input('Search query: '))

    response = youtube.search().list(
        part='snippet',
        forMine=True,
        maxResults=50,
        q=search_query,
        type='video'
    ).execute()

    total_results = int(response['pageInfo']['totalResults'])
    results_per_page = int(response['pageInfo']['resultsPerPage'])
    i = 1
    if total_results != 0:
        while 'nextPageToken' in response:
            total_pages = ceil(total_results / results_per_page)
            print(f'page {i} of {total_pages}')
            for video in response['items']:
                print(video['snippet']['title'])
            
            response = youtube.search().list(
                part='snippet',
                forMine=True,
                maxResults=50,
                pageToken=str(response['nextPageToken']),
                q=search_query,
                type='video'
            ).execute()

            i += 1

        else:
            total_pages = ceil(total_results / results_per_page)
            print(f'page {i} of {total_pages if total_pages > 0 else 1}')
            for video in response['items']:
                print(video['snippet']['title'])

if __name__ == '__main__':
    main()