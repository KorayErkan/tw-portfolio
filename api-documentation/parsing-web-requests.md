# Parsing Web Requests With _GoodWeb_&trade; API

[_John Saysitall_](mailto:john.saysitall@goodcode.com)

---

## Table of Contents

* [URL Structure](#url-structure)
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
  * [GetFragment](#getfragment)
  * [ParseRequestBody](#parserequestbody)
* [References](#references)

---

The **GoodWeb** API provides functions to parse URL request strings and extract their components for web request processing.

## URL Structure

URLs contain up to five components in this order:

```
https://subdomain.domain.com/endpoint/path?param=value&param2=value2
[1]    [2]       [3]    [4] [5]          [6]
```

| Component | Required | Example | Purpose |
|-----------|----------|---------|---------|
| **Protocol** | Yes | `https`, `http`, `ftp` | Communication method |
| **Subdomain** | No | `www`, `api`, `admin` | Service routing |
| **Domain** | Yes | `goodfood.com` | Site identification |
| **Endpoint** | No | `/products`, `/api/v1` | Resource path |
| **Query** | No | `?brand=elite&price=15` | Parameter data |

## Core Functions

### CreateRequest

Creates and validates a web request object from a URL string.

**Syntax:** `WebServer.CreateRequest(url: String): WebServer.Request`

**Parameters:** 
- `url` - URL string to parse

**Returns:** `WebServer.Request` object or `null` if URL is empty

**Exceptions:** `MalformedURLException` if URL format is invalid

**Example:**
```javascript
try {
    var request = server.CreateRequest("https://api.goodfood.com/products");
    if (request == null) return;
    // Process request...
} catch (MalformedURLException e) {
    server.DisplayErrorPage(e.Message);
}
```

### GetProtocol

Extracts the protocol (scheme) from the request URL.

**Syntax:** `WebServer.Request.GetProtocol(): String`

**Returns:** Protocol string (`http`, `https`, `ftp`, `news`) or defaults to `https` if empty

**Exceptions:** `ProtocolNotSupportedException` for unsupported protocols

**Supported Protocols:**
- `http` - Standard web traffic
- `https` - Secure web traffic  
- `ftp` - File transfer
- `news` - News feeds

**Example:**
```javascript
try {
    var protocol = request.GetProtocol();
    if (protocol == "") protocol = "https";
    request.CommunicateOver(protocol);
} catch (ProtocolNotSupportedException e) {
    server.DisplayErrorPage(e.Message);
}
```

### GetRootDomain

Extracts the root domain from the URL.

**Syntax:** `WebServer.Request.GetRootDomain(): String`

**Returns:** Root domain string (e.g., `goodfood.com`)

**Exceptions:** `MalformedURLException` for invalid domain formats

**Example:**
```javascript
try {
    var root = request.GetRootDomain();
    request.SetRootTo(root);
} catch (MalformedURLException e) {
    // Handle error
}
```

### GetSubdomain

Extracts the subdomain from the URL.

**Syntax:** `WebServer.Request.GetSubdomain(): String`

**Returns:** Subdomain string or empty if none exists

**Examples:** `www`, `api`, `admin` from `https://api.goodfood.com`

**Example:**
```javascript
var subdomain = request.GetSubdomain();
if (subdomain != "" && subdomain != "www") {
    server.RedirectTo(subdomain);
}
```

### GetEndpoint

Extracts the endpoint path from the URL.

**Syntax:** `WebServer.Request.GetEndpoint(): String`

**Returns:** Endpoint path string or empty if none exists

**Examples:** `/products`, `/api/v1/users`

**Example:**
```javascript
var endpoint = request.GetEndpoint();
if (endpoint != "" && server.Endpoints.Contains(endpoint)) {
    server.RouteToEndpoint(endpoint);
}
```

### GetQueryParameters

Parses URL query string into key-value dictionary.

**Syntax:** `WebServer.Request.GetQueryParameters(): Dictionary`

**Returns:** Dictionary of parameter names and values, or empty dictionary if no query string

**Exceptions:** `ParameterNotFoundException` for invalid parameter names/values

**Query Format:** `?key1=value1&key2=value2&key3=value3`

**Example:**
```javascript
try {
    var params = request.GetQueryParameters();
    if (params.Count > 0) {
        var dataset = database.GetDatasetFor(params);
        server.DisplayPageFor(dataset);
    }
} catch (ParameterNotFoundException e) {
    server.DisplayErrorPage(e.Message);
}
```

## Utility Functions

### ValidateURL

Validates URL format without creating a request object.

**Syntax:** `WebServer.ValidateURL(url: String): Boolean`

**Parameters:** 
- `url` - URL string to validate

**Returns:** `true` if URL format is valid, `false` otherwise

**Example:**
```javascript
if (WebServer.ValidateURL("https://api.goodfood.com")) {
    // URL is valid, proceed with processing
}
```

### GetHTTPMethod

Extracts the HTTP method from the request.

**Syntax:** `WebServer.Request.GetHTTPMethod(): String`

**Returns:** HTTP method (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`)

**Default:** Returns `GET` if method not specified

**Example:**
```javascript
var method = request.GetHTTPMethod();
switch (method) {
    case "GET": server.HandleGetRequest(request); break;
    case "POST": server.HandlePostRequest(request); break;
}
```

### GetHeaders

Extracts HTTP headers from the request.

**Syntax:** `WebServer.Request.GetHeaders(): Dictionary`

**Returns:** Dictionary of header names and values

**Common Headers:** `Content-Type`, `Authorization`, `Accept`, `User-Agent`

**Example:**
```javascript
var headers = request.GetHeaders();
var contentType = headers.Get("Content-Type");
var auth = headers.Get("Authorization");
```

### GetFragment

Extracts URL fragment (anchor) portion.

**Syntax:** `WebServer.Request.GetFragment(): String`

**Returns:** Fragment string without the `#` symbol, or empty if none exists

**Example:** For `https://example.com/page#section1` returns `section1`

**Example:**
```javascript
var fragment = request.GetFragment();
if (fragment != "") {
    server.ScrollToSection(fragment);
}
```

### ParseRequestBody

Parses request body content (JSON, form data, XML).

**Syntax:** `WebServer.Request.ParseRequestBody(format: String): Dictionary`

**Parameters:**
- `format` - Expected format (`json`, `form`, `xml`)

**Returns:** Dictionary of parsed data

**Exceptions:** `InvalidFormatException` for malformed data

**Example:**
```javascript
try {
    var data = request.ParseRequestBody("json");
    var userId = data.Get("user_id");
    var email = data.Get("email");
} catch (InvalidFormatException e) {
    server.ReturnBadRequest(e.Message);
}
```

---

## References

* The **GoodWeb** API Handbook, pp. 18–22
* The [GoodWeb Server](www.goodweb-server.com) API discussion thread
* The **GoodWeb** message board on [Pro-Coders](www.pro-coders.com)
