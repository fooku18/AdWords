from googleads import adwords

def main(client):
    feed_service = client.GetService('FeedService',version='v201708')
    operation = {
        'operator': 'ADD',
        'operand':{
            'name':'Test_Feed',
            'attributes':[
                {'type': 'URL_LIST', 'name': 'Page URL'},
                {'type': 'STRING_LIST', 'name': 'Label'}
            ],
            'origin':'USER'
        }
    }
    feed = feed_service.mutate([operation])
    print feed
if __name__ == "__main__":
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    main(adwords_client)