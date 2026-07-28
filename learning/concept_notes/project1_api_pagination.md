# API Pagination

## Core Idea

Pagination is the practice of dividing a large collection of API results into smaller responses called **pages**.

An API may limit how many records it returns in one response so that the server and client do not have to transfer or process an entire large dataset at once. A client that needs the complete dataset must request every page and combine the results.

## Simple Example

Suppose a roads dataset contains 25,000 records, but the API returns at most 5,000 records per request:

```text
Page 1: records     1-5,000
Page 2: records 5,001-10,000
Page 3: records 10,001-15,000
Page 4: records 15,001-20,000
Page 5: records 20,001-25,000
```

If Extract requests only the first page, the resulting raw artifact contains 5,000 records rather than the complete 25,000-record dataset.

## Limit and Offset Pagination

Some APIs use `limit` and `offset` query parameters:

```text
?limit=5000&offset=0
?limit=5000&offset=5000
?limit=5000&offset=10000
```

- `limit` specifies the maximum number of records to return.
- `offset` specifies how many earlier records to skip.

A client increases the offset until a response contains fewer records than the limit or the API otherwise indicates that no results remain.

## Other Pagination Styles

APIs can paginate in several ways:

### Page Numbers

```text
?page=1&page_size=5000
?page=2&page_size=5000
```

The client increments the page number.

### Continuation Tokens

```text
?next_token=abc123
```

The response provides an opaque token that the client sends with the next request. The client should use the token exactly as documented rather than trying to interpret it.

### Next-Page Links

The response includes a complete URL for the next page. The client follows that link until no next link is present.

Different APIs define different stopping rules, maximum page sizes, ordering guarantees, and rate limits. Their documentation is part of the source contract.

## Why Pagination Matters in ETL

Pagination can create a silent completeness problem. The first request may return:

```text
HTTP 200 OK
```

That status proves the request succeeded, but it does not prove that every record was retrieved.

A robust Extract stage should determine:

- whether the endpoint paginates results
- which pagination method it uses
- the maximum allowed page size
- how to detect the final page
- whether records have a stable ordering
- whether the source reports a total record count
- how rate limits and retries affect requests

## Pagination and Changing Data

Offset pagination can be especially risky when source data changes during a multi-page extraction.

For example, if records are inserted or removed after page 1 but before page 2, offsets may shift. The client could skip a record or retrieve one twice. Stable sorting, snapshot-capable APIs, identifiers, and post-extract checks can reduce this risk.

This is one reason that retrieving multiple pages is not automatically equivalent to capturing one consistent source snapshot.

## Pagination and Provenance

The source URL is provenance evidence, but pagination behavior also affects what the URL returns. Two runs against the same endpoint can produce different raw artifacts when:

- the source records change
- the default page size changes
- filtering or ordering rules change
- the extraction follows a different number of pages
- a continuation token expires or fails

Useful provenance for a paginated extract may include the retrieval time, page count, total rows collected, request status for each page, and final output checksum.

## Pagination and Quality Checks

QA should not assume that a nonempty file is complete. Useful completeness checks can include:

- comparison with a source-reported total count
- expected minimum or historical row-count ranges
- duplicate identifier checks across combined pages
- missing identifier checks
- verification that the final-page condition was reached

These checks cannot guarantee source correctness, but they can catch common pagination failures.

## This Project

The project currently retrieves configured GeoJSON source URLs as complete responses. Before using the same approach with a different endpoint or a larger dataset, inspect that API's documentation and test whether it imposes pagination or record limits.

A source that begins paginating responses could still return a valid HTTP response while causing Extract to preserve only a partial raw snapshot. That behavior should be treated as a source-contract change.

## Plain-Language Definition

> Pagination is how an API delivers a large dataset through several smaller responses instead of one large response.

## Related Resources

- [Data provenance](project1_provenance.md)
- [Data artifacts](project1_data_artifacts.md)
- [Data contracts and stage boundaries](project1_data_contracts.md)
- [Module 3 Extract reference](../reference/project1_module_3_extract_reference.md)
- [Module 3 Extract practice](../practice/project1_module_3_extract_practice.ipynb)
