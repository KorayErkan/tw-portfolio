# Stripe API Documentation

## Table of Contents

* Introduction: What is Stripe API, how was it designed (RESTful, etc.)
* What can the target audience (developers) expect
* How to connect to the API (base URL, registering for an API key, etc.)
* How to authenticate (token and bearer type)
* Requests and responses: what requests to send and what responses to expect

## Functionality

What can be done using the API. As a developer you can do the following:

* Handle balances
* Balance transactions
* Calculate charges
* Work with customers
* Handle disputes
* Create events
* Create files

### The Balance object

You can use the balance object to request the balance of a specific credit card with a `get` operation.

Only `GET` operation is possible for this request. Endpoint for it:

`'{{base_url}}/v1/balance'`

The response will return the standard status code, along with the parameters in JSON format:

> Code: 200 OK
>
> JSON:

```{JSON}
{
    "object": "balance",
    "available": [
        {
            "amount": 0,
            "currency": "usd",
            "source_types": {
                "card": 0
            }
        }
    ],
    "livemode": false,
    "pending": [
        {
            "amount": 0,
            "currency": "usd",
            "source_types": {
                "card": 0
            }
        }
    ]
}
```

#### Parameters

These will be _key-value_ pairs.
