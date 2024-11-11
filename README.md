# Anker Info
Checks if Anker is on sale

Checks are performed each Monday at 08:00. The most recent data is available shortly afterwards.

### Polling
Visit https://anker.uzwil-to-tokyo.ch/api/promotion for the newest promotion data. The data is formatted as described [here](#payload)

### Webhooks
If you URL is listed in the Webhooks data on [https://github.com/noahzarro/anker-data/tree/main](), then you receive a POST request every time the new promotions are loaded. It has a payload like described [here](#payload)

### Payload

```jsonc
{
    "hasPromotion": true,
    "isHalfPrice": true,
    "promotionString": "50% ab jetzt", // (string or null)
    "checkedAt": 1234235654, // seconds since epoch
    "signedData": "srtzw.dhrert.sfgrth" // a jwt as explained in chapter Signature
}
```

### Signature
The `signedData` contains a JWT, containing all data in the payload, except for (obviously) the signedData. Like this, the response is still human readable, but also secure from attacks from the [adversary](https://pascscha.ch/). He will attempt to send fake POST requests to the registered webhook clients.

The signature is calculated using the `ES512` algorithm. It can easily be checked with a JWT library. An example is provided below:

```bash
pip install pyjwt[crypto]
```

```python
public_key_pem = """
-----BEGIN PUBLIC KEY-----
MIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQBDLErTusEhI/Dbxw7HwRjugx5A1sg
13CKQXCpdOfPbfN3YyF1sSOlXdeztU6LHVnx+xNVVLKPKbei370laJpxq3EAHEqX
guTVasOeTvBnqMugZUH+SLDx0ZgraMjFE75kNQAHRZvA8inPoDPXJZ30onuYupkO
7gnhEQEkU6qsAvhBiFE=
-----END PUBLIC KEY-----
"""

decoded_data = jwt.decode(signed_data, public_key_pem, algorithms=["ES512"])
```

This code will throw a `jwt.exceptions.InvalidSignatureError` if the signature is incorrect.
The same public key is used as in the example


### TODO:
Add Reviews Request:
[https://www.coop.ch/rest/v2/coopathome/products/3458809/reviews?currentPage=0&pageSize=20&sort=most_helpful&language=en]()

### Deployment
Note to myself:
Start Docker Desktop to start the docker container that is also used by WSL
Build and publish the docker container like this
```bash
docker build -t noahzarro/anker-api:v3 .
docker push noahzarro/anker-api:v3
```
Create new Container in Portainer and select correct docker image (`noahzarro/anker-api:v3`) and add a name (`anker-api`). Create the container and then add it to the `npm` network. Then add forwarding rule to the reverse proxy manager (`anker.uzwil-to-tokyo.ch` -> `anker-api:5000`) only for `http`. Then add a let's encrypt certificate and save.