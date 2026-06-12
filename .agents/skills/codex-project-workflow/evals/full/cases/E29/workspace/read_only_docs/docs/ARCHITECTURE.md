# Architecture

The API process owns request validation and writes directly to the reporting
database. The worker process also owns the reporting database schema.

The API may call the worker package directly when the queue is unavailable.
