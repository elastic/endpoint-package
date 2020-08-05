## Metadata Current

The metadata current index will hold the most recent event for each Endpoint. This will allow us 
to query the current state and apply more flexible filtering. It also have performance value. It
is also different from the other index schema because it comprises of the metadata schema. 
This approach was taken to avoid duplication and also avoid misses when the metadata schema is 
updated. If we miss any mapping then we loose the ability to query for that field. Hence the
final field properties are imported from the metadata fields set. 