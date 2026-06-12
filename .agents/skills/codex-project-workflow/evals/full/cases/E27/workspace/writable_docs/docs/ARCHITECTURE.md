# Architecture

## Ownership

The catalog service owns product descriptions and publication status.

## Dependencies

The checkout service may read catalog data through the catalog API. The catalog
service must not import checkout modules.
