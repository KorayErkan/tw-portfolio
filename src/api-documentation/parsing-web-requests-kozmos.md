# Parsing Web Requests with the _GoodWeb_&trade; API (Kozmos)

[_John Saysitall_](mailto:john.saysitall@goodcode.example)

---

## Table of Contents

* [The Purpose of the API](#the-purpose-of-the-api)
* [Structure of URLs](#structure-of-urls)
* [Functions for Parsing URLs](#functions-for-parsing-urls)
  * [CreateRequest](#createrequest)
  * [GetProtocol](#getprotocol)
  * [GetRootDomain](#getrootdomain)
  * [GetSubdomain](#getsubdomain)
  * [GetEndpoint](#getendpoint)
  * [GetQueryParameters](#getqueryparameters)
* [References](#references)

---

This document describes the URL-parsing functions of the **GoodWeb** API. The server uses these functions to break down the URL of an incoming request, so that it can respond with the information the user asked for.

All code examples in this document are written in _Kozmos_, a C#-like language. The same API is also available from JavaScript; see [Parsing Web Requests with the GoodWeb API (JavaScript)](parsing-web-requests-javascript.md).

## The Purpose of the API

Users interact with web sites by sending requests. Each request is addressed with a _Uniform Resource Locator_, or _URL_. When a request arrives at the site, the server passes its URL to the API, which parses it and creates a request object. The request object exposes the parts of the URL, from which the server determines what information is being requested, whether it exists, and, if it does, which part of the site should respond.

The purpose of this API is to provide the functionality necessary to carry out this process.

## Structure of URLs

The syntax of a request URL that the API accepts can be summarized in _EBNF_ (Extended Backus-Naur Form) as follows. Square brackets (`[ ]`) enclose optional items, and curly braces (`{ }`) enclose items that can be repeated zero or more times:

```ebnf
url                 ::= protocol "://" host [ endpoint ] [ query-string ]
protocol            ::= letter { letter }
host                ::= [ subdomain "." ] root-domain
subdomain           ::= label { "." label }
root-domain         ::= label "." label
endpoint            ::= "/" [ path-segment { "/" path-segment } ]
path-segment        ::= alphanumeric-token { ( "-" | "_" | "." ) alphanumeric-token }
label               ::= alphanumeric-token { "-" alphanumeric-token }

query-string        ::= "?" field-value-pair { "&" field-value-pair }
field-value-pair    ::= field-name operator field-value
field-name          ::= alphanumeric-token { "-" alphanumeric-token }
operator            ::= "=" | "<" | ">" | "<=" | ">="
field-value         ::= alphanumeric-string | numeric-token

alphanumeric-string ::= alphanumeric-token { "+" alphanumeric-token }
alphanumeric-token  ::= letter { letter | digit }
numeric-token       ::= digit { digit }
letter              ::= "A" | ... | "Z" | "a" | ... | "z"
digit               ::= "0" | ... | "9"
```

The API always treats the last two labels of the host as the root domain, and any labels before them as the subdomain.

A URL may contain the following components, which, when present, must appear in this order:

1. The protocol used to access the site
2. The subdomain
3. The root domain
4. The endpoint
5. The query string

Only the protocol and the root domain are required. The table below briefly describes each component:

| Component | Description |
| --- | --- |
| Protocol | The name of the set of rules that the user's browser and the site's server observe to communicate with each other, such as _http_, _https_, or _ftp_. It is followed by `://`. |
| Subdomain | Any labels to the left of the root domain. In `https://diabetic.goodfood.example` the subdomain is _diabetic_, and in `https://www.diabetic.goodfood.example` it is _<www.diabetic>_. |
| Root Domain | The registered domain name of the site: the last two labels of the host name. In `https://www.goodfood.example` the root domain is _goodfood.example_. |
| Endpoint | The full path that follows the host name, up to the query string, if any. It identifies the part of the site that responds to the request. In `https://www.goodfood.example/vegetarian/products` the endpoint is _/vegetarian/products_. |
| Query String | The parameters sent to the endpoint to request specific information. It starts at the question mark (`?`) and consists of parameters separated by ampersands (`&`). Each parameter is a name, followed by a relational operator (`=`, `<`, `>`, `<=`, or `>=`), followed by a value. In `https://www.goodfood.example/vegetarian/products?brand=elite&price<=15&home-delivery=true` the query string is `?brand=elite&price<=15&home-delivery=true`. |

> **Note:** Before a request reaches the site, the browser resolves the _full_ host name (subdomain included) to an IP address through DNS. The API does not take part in that lookup; it only splits the host name into its subdomain and root domain so that the server can route the request.

<!-- separate notes -->

> **Note:** Browsers send `<` and `>` percent-encoded (as `%3C` and `%3E`). `CreateRequest` decodes the URL before parsing it, so the functions below always see the plain characters.

## Functions for Parsing URLs

The API provides the functions documented below for parsing URLs. Before calling any of them, pass the URL to the server's `CreateRequest` method.

### CreateRequest

The first responder for the URL. This method does the preliminary work of parsing and validating the URL.

```csharp
WebServer.CreateRequest(url: String): WebServer.Request
```

If the URL is empty, no request object is created and `null` is returned. If the URL does not match the syntax above (for example, if it has no protocol, or its host has only one label), a `MalformedURLException` is raised. Otherwise, a request object is returned, on which the other methods can be called to return the parts indicated by their names.

Typical use:

```csharp
try {
    var request = server.CreateRequest(url)
    if request == null {
        // URL is empty: nothing to process
        return
    }
    // proceed to other actions
    ...
}
catch exception: MalformedURLException {
    server.DisplayErrorPage(exception.Message)
}
```

### GetProtocol

Returns the protocol used to access the site. This determines, for example, whether the connection is secure, or whether the user wants to view pages or download files. Because `CreateRequest` rejects URLs without a protocol, this method never returns an empty string. If the protocol is not supported, a `ProtocolNotSupportedException` is raised.

```csharp
WebServer.Request.GetProtocol(): String
```

The table below shows the protocols that can be parsed from a URL:

| URL | Result | Use |
| --- | --- | --- |
| `http://www.goodfood.example` | _http_ | Hypertext is served |
| `https://www.goodfood.example` | _https_ | Hypertext is served over a secure connection |
| `ftp://www.goodfood.example` | _ftp_ | Files available to the public can be downloaded |
| `news://www.goodfood.example` | _news_ | The news feed is provided |
| `file://www.goodfood.example` | Raises `ProtocolNotSupportedException` | `file` is not a supported protocol |
| `www.goodfood.example` | No request object: `CreateRequest` raises `MalformedURLException` | The protocol is missing |

Typical use:

```csharp
try {
    // create request, etc.
    ...
    var protocol = request.GetProtocol()
    request.CommunicateOver(protocol)
    // proceed to other actions
    ...
}
catch exception: ProtocolNotSupportedException {
    server.DisplayErrorPage(exception.Message)
}
```

### GetRootDomain

Returns the root domain of the URL. This can be used, for example, to check which of the sites hosted on the server the user is trying to access.

```csharp
WebServer.Request.GetRootDomain(): String
```

The table below shows the root domains returned for various URLs:

| URL | Root Domain |
| --- | --- |
| `https://www.goodfood.example` | _goodfood.example_ |
| `https://goodfood.example` | _goodfood.example_ |
| `https://www.diabetic.goodfood.example` | _goodfood.example_ |
| `https://goodfood` | No request object: `CreateRequest` raises `MalformedURLException` |

Typical use:

```csharp
// create request, etc.
...
var root = request.GetRootDomain()
request.SetRootTo(root)
// proceed to other actions
...
```

### GetSubdomain

Returns the subdomain of the URL, or an empty string if the URL has none. If the subdomain is part of the site, the user can then be redirected to it.

```csharp
WebServer.Request.GetSubdomain(): String
```

The table below shows the subdomains returned for various URLs:

| URL | Subdomain |
| --- | --- |
| `https://diabetic.goodfood.example` | _diabetic_ |
| `https://www.diabetic.goodfood.example` | _<www.diabetic>_ |
| `https://www.goodfood.example` | _www_ |
| `https://goodfood.example` | Empty string: no subdomain |

Typical use:

```csharp
// create request, etc.
...
var subdomain = request.GetSubdomain()
if subdomain != "" and subdomain != "www" {
    server.RedirectTo(subdomain)
}
// ... etc.
```

### GetEndpoint

Returns the endpoint the URL addresses: the full path after the host name. If the URL has no path, `/` (the root of the site) is returned. The server can use the endpoint to verify that it exists and to route the request, including its query string, to the part of the site that handles it.

```csharp
WebServer.Request.GetEndpoint(): String
```

The table below shows the endpoints returned for various URLs:

| URL | Endpoint |
| --- | --- |
| `https://www.goodfood.example` | _/_ (no path specified) |
| `https://www.goodfood.example/products` | _/products_ |
| `https://www.goodfood.example/recipes/vegetarian` | _/recipes/vegetarian_ |

Typical use:

```csharp
// create request, etc.
...
var endpoint = request.GetEndpoint()
if server.Endpoints.Contains(endpoint) {
    server.RouteToEndpoint(endpoint)
}
else {
    server.DisplayNotFoundPage(endpoint)
}
```

### GetQueryParameters

Returns the parameters in the query string as a dictionary. The parameter names are used as keys. Each value is a `Condition` object whose `Operator` property holds the relational operator and whose `Value` property holds the value. If the URL has no query string, an empty dictionary is returned.

Before the dictionary is created, each parameter _name_ is checked against the parameters the endpoint recognizes. If a name is not recognized (for example, because of a misspelling), a `ParameterNotFoundException` is raised. Its message names the unrecognized parameter(s). Parameter _values_ are not validated by this method; a value that matches nothing simply produces an empty result set.

Once the dictionary is created, the server can proceed to display the results from the site database.

```csharp
WebServer.Request.GetQueryParameters(): Dictionary<String, Condition>
```

The table below shows the dictionaries created for various URLs:

| URL | Parameter Names | Conditions |
| --- | --- | --- |
| `https://www.goodfood.example/vegetarian/products?brand=elite&price<=15&home-delivery=true` | _brand_, _price_, _home-delivery_ | `= elite`, `<= 15`, `= true` |
| `https://www.goodfood.example/products?brnad=elite` | None: raises `ParameterNotFoundException` | The endpoint _/products_ has no parameter named _brnad_ |
| `https://www.goodfood.example/products` | None: empty dictionary | No query string |

Typical use:

```csharp
try {
    // create request, etc.
    ...
    var parameters = request.GetQueryParameters()
    if parameters.Count > 0 {
        var database = Database.Instance()
        var dataset = database.GetDatasetFor(parameters)
        server.DisplayPageFor(dataset)
        // other actions
        ...
    }
}
catch exception: ParameterNotFoundException {
    server.DisplayErrorPage(exception.Message)
    // etc.
    ...
}
```

---

## References

* The **GoodWeb** API Handbook, pp. 18–22
* The [GoodWeb Server](https://goodweb.example) API discussion thread
* The **GoodWeb** message board on [Pro-Coders](https://procoders.example)
