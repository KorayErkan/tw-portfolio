# Parsing Web Requests with the _GoodWeb_&trade; API (JavaScript)

[_John Saysitall_](mailto:john.saysitall@goodcode.example)

---

## Table of Contents

* [Overview](#overview)
* [URL Structure](#url-structure)
* [Setup](#setup)
* [Core Functions](#core-functions)
  * [CreateRequest](#createrequest)
  * [GetProtocol](#getprotocol)
  * [GetRootDomain](#getrootdomain)
  * [GetSubdomain](#getsubdomain)
  * [GetEndpoint](#getendpoint)
  * [GetQueryParameters](#getqueryparameters)
* [Utility Functions](#utility-functions)
  * [ValidateURL](#validateurl)
  * [GetHTTPMethod](#gethttpmethod)
  * [GetHeaders](#getheaders)
  * [ParseRequestBody](#parserequestbody)
* [References](#references)

---

## Overview

The **GoodWeb** API parses incoming web requests for a server written in JavaScript. The same API is also documented for the Kozmos language in [Parsing Web Requests with the GoodWeb API (Kozmos)](parsing-web-requests-kozmos.md); both bindings behave identically.

When the server receives an HTTP request, it passes the request URL to `CreateRequest`. The returned `Request` object wraps the _whole_ HTTP request:

* The **core functions** parse the request URL into its components.
* The **utility functions** validate URLs and read the other parts of the HTTP request: its method, headers, and body.

Each example below ends with a `// →` comment showing the result for the sample URL.

## URL Structure

URLs contain up to five components, in this order:

```text
https://www.goodfood.example/vegetarian/products?brand=elite
└─1─┘   └2┘ └──────3───────┘└────────4─────────┘└────5─────┘
```

| # | Component | Required | Example | Purpose |
|---|-----------|----------|---------|---------|
| 1 | **Protocol** | Yes | `https`, `http`, `ftp` | Communication method |
| 2 | **Subdomain** | No | `www`, `api`, `www.diabetic` | Service routing |
| 3 | **Root domain** | Yes | `goodfood.example` | Site identification |
| 4 | **Endpoint** | No | `/products`, `/vegetarian/products` | Resource path |
| 5 | **Query string** | No | `?brand=elite&price<=15` | Parameter data |

The root domain is always the last two labels of the host name; everything before it is the subdomain. Query parameters use one of the relational operators `=`, `<`, `>`, `<=`, or `>=` between the name and the value.

## Setup

The examples below assume that the API has been loaded, and a server object and a database object have been created:

```javascript
const {
    WebServer,
    Database,
    MalformedURLException,
    ProtocolNotSupportedException,
    ParameterNotFoundException,
    InvalidFormatException,
} = require("goodweb");

const server = new WebServer();
const database = Database.Instance();
```

All exception types are subclasses of JavaScript's `Error`, so they carry a `message` property and can be told apart with `instanceof`.

## Core Functions

### CreateRequest

Creates and validates a request object from the URL of an incoming HTTP request.

**Syntax:** `WebServer.CreateRequest(url: String): WebServer.Request`

**Parameters:**

* `url`: the URL string to parse

**Returns:** a `WebServer.Request` object, or `null` if the URL is empty

**Exceptions:** `MalformedURLException` if the URL is not well formed, including when it has no protocol (the protocol is required)

**Example:**

```javascript
function handle(url) {
    try {
        const request = server.CreateRequest(url);
        if (request === null) return; // empty URL: nothing to process
        // Process request...
        return request;
    } catch (e) {
        if (e instanceof MalformedURLException) {
            server.DisplayErrorPage(e.message);
        } else {
            throw e;
        }
    }
}

handle("https://api.goodfood.example/products"); // → Request object
handle("api.goodfood.example/products");         // → error page: protocol missing
```

### GetProtocol

Extracts the protocol (scheme) from the request URL. Because `CreateRequest` rejects URLs without a protocol, this function never returns an empty string.

**Syntax:** `WebServer.Request.GetProtocol(): String`

**Returns:** the protocol string: `http`, `https`, `ftp`, or `news`

**Exceptions:** `ProtocolNotSupportedException` for any other protocol, such as `file`

**Supported protocols:**

* `http`: standard web traffic
* `https`: secure web traffic
* `ftp`: file transfer
* `news`: news feeds

**Example:**

```javascript
// request = server.CreateRequest("https://www.goodfood.example")
try {
    const protocol = request.GetProtocol(); // → "https"
    request.CommunicateOver(protocol);
} catch (e) {
    if (e instanceof ProtocolNotSupportedException) {
        server.DisplayErrorPage(e.message);
    } else {
        throw e;
    }
}
```

### GetRootDomain

Extracts the root domain (the last two labels of the host name) from the URL. A host with fewer than two labels, such as `https://goodfood`, is already rejected by `CreateRequest`.

**Syntax:** `WebServer.Request.GetRootDomain(): String`

**Returns:** the root domain string

**Example:**

```javascript
// request = server.CreateRequest("https://www.diabetic.goodfood.example")
const root = request.GetRootDomain(); // → "goodfood.example"
request.SetRootTo(root);
```

### GetSubdomain

Extracts the subdomain (all labels before the root domain) from the URL.

**Syntax:** `WebServer.Request.GetSubdomain(): String`

**Returns:** the subdomain string, or an empty string if there is none

**Results for sample URLs:**

| URL | Result |
|-----|--------|
| `https://api.goodfood.example` | `"api"` |
| `https://www.diabetic.goodfood.example` | `"www.diabetic"` |
| `https://goodfood.example` | `""` |

**Example:**

```javascript
// request = server.CreateRequest("https://api.goodfood.example")
const subdomain = request.GetSubdomain(); // → "api"
if (subdomain !== "" && subdomain !== "www") {
    server.RedirectTo(subdomain);
}
```

### GetEndpoint

Extracts the endpoint (the full path after the host name) from the URL.

**Syntax:** `WebServer.Request.GetEndpoint(): String`

**Returns:** the endpoint path, or `"/"` if the URL has no path

**Results for sample URLs:**

| URL | Result |
|-----|--------|
| `https://www.goodfood.example` | `"/"` |
| `https://www.goodfood.example/products` | `"/products"` |
| `https://www.goodfood.example/recipes/vegetarian` | `"/recipes/vegetarian"` |

**Example:**

```javascript
// request = server.CreateRequest("https://www.goodfood.example/recipes/vegetarian")
const endpoint = request.GetEndpoint(); // → "/recipes/vegetarian"
if (server.Endpoints.includes(endpoint)) {
    server.RouteToEndpoint(endpoint);
} else {
    server.DisplayNotFoundPage(endpoint);
}
```

### GetQueryParameters

Parses the query string into a `Map`. The keys are the parameter names; each value is an object of the form `{ operator, value }`.

**Syntax:** `WebServer.Request.GetQueryParameters(): Map<String, {operator: String, value: String}>`

**Returns:** a `Map` of parameter names and conditions, or an empty `Map` if the URL has no query string

**Exceptions:** `ParameterNotFoundException` if a parameter _name_ is not recognized by the endpoint (for example, `?brnad=elite` on `/products`). Parameter values are not validated.

**Query format:** `?name1=value1&name2<=value2&name3=value3`

**Example:**

```javascript
// request = server.CreateRequest(
//     "https://www.goodfood.example/vegetarian/products?brand=elite&price<=15&home-delivery=true")
try {
    const params = request.GetQueryParameters();
    // → Map(3) {
    //     "brand" => { operator: "=", value: "elite" },
    //     "price" => { operator: "<=", value: "15" },
    //     "home-delivery" => { operator: "=", value: "true" } }
    if (params.size > 0) {
        const dataset = database.GetDatasetFor(params);
        server.DisplayPageFor(dataset);
    }
} catch (e) {
    if (e instanceof ParameterNotFoundException) {
        server.DisplayErrorPage(e.message);
    } else {
        throw e;
    }
}
```

## Utility Functions

### ValidateURL

Checks whether a URL is well formed without creating a request object. It applies the same rules as `CreateRequest`, so a URL without a protocol is invalid.

**Syntax:** `WebServer.ValidateURL(url: String): Boolean`

**Parameters:**

* `url`: the URL string to validate

**Returns:** `true` if the URL is well formed, `false` otherwise

**Example:**

```javascript
WebServer.ValidateURL("https://api.goodfood.example"); // → true
WebServer.ValidateURL("api.goodfood.example");         // → false (no protocol)
```

### GetHTTPMethod

Returns the method of the HTTP request that the request object wraps.

**Syntax:** `WebServer.Request.GetHTTPMethod(): String`

**Returns:** the HTTP method in upper case, such as `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, or `OPTIONS`

**Example:**

```javascript
const method = request.GetHTTPMethod(); // → "GET" for a page load
switch (method) {
    case "GET":
        server.HandleGetRequest(request);
        break;
    case "POST":
        server.HandlePostRequest(request);
        break;
    default:
        server.ReturnMethodNotAllowed(method);
}
```

### GetHeaders

Returns the headers of the HTTP request that the request object wraps.

**Syntax:** `WebServer.Request.GetHeaders(): Map<String, String>`

**Returns:** a `Map` of header names and values. Header names are stored in lower case, because HTTP header names are case-insensitive.

**Common headers:** `content-type`, `authorization`, `accept`, `user-agent`

**Example:**

```javascript
const headers = request.GetHeaders();
const contentType = headers.get("content-type"); // → "application/json"
const auth = headers.get("authorization");       // → undefined if not sent
```

### ParseRequestBody

Parses the body of the HTTP request that the request object wraps. The body is typically sent with `POST`, `PUT`, and `PATCH` requests.

**Syntax:** `WebServer.Request.ParseRequestBody(format: String): Object`

**Parameters:**

* `format`: the expected format: `json`, `form`, or `xml`

**Returns:** a plain object containing the parsed data

**Exceptions:** `InvalidFormatException` if the body is not valid in the given format

**Example:**

```javascript
// Body: {"user_id": 42, "email": "jane@goodfood.example"}
try {
    const data = request.ParseRequestBody("json");
    const userId = data.user_id; // → 42
    const email = data.email;    // → "jane@goodfood.example"
    server.UpdateUser(userId, email);
} catch (e) {
    if (e instanceof InvalidFormatException) {
        server.ReturnBadRequest(e.message);
    } else {
        throw e;
    }
}
```

---

## References

* The **GoodWeb** API Handbook, pp. 18–22
* The [GoodWeb Server](https://goodweb.example) API discussion thread
* The **GoodWeb** message board on [Pro-Coders](https://procoders.example)
