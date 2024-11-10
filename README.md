# Anker Info
Checks if Anker is on sale

Checks are performed each Monday at 10:00. The most recent data is available shortly afterwards.

### Polling


### Webhooks
If you URL is listed in the Webhooks data on [https://github.com/noahzarro/anker-data/tree/main](), then you receive a POST request every time the new promotions are loaded. It has a payload like the following:

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