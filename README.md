# Anker Info
Checks if Anker is on sale

Checks are performed each Monday at 10:00. The most recent data is available shortly afterwards.

### Polling
Visit [https://anker.uzwil-to-tokyo.ch/api/promotion] for the newest promotion data. The data is formatted as described [here](#payload)

### Webhooks
If you URL is listed in the Webhooks data on [https://github.com/noahzarro/anker-data/tree/main](), then you receive a POST request every time the new promotions are loaded. It has a payload like described [here](#payload)

### Payload

```jsonc
{
    "hasPromotion": true,
    "isHalfPrice": true,
    "promotionString": "50% ab jetzt" // optional
}
```

### TODO:
Add Reviews Request:
[https://www.coop.ch/rest/v2/coopathome/products/3458809/reviews?currentPage=0&pageSize=20&sort=most_helpful&language=en]()

### Deployment
Note to myself:
Start Docker Desktop to start the docker container that is also used by WSL
Build and publish the docker container like this
```bash
docker build -t noahzarro/anker-api:v2 .
docker push noahzarro/anker-api:v2
```
Select 