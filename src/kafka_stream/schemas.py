SCHEMA_API = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "APIRequest",
  "description": "An API request",
  "type": "object",
  "properties": {
    "ip": {
      "description": "Source IP address",
      "type": "string"
    },
    "method": {
      "description": "HTTP method",
      "type": "string"
    },
    "path": {
      "description": "Request path",
      "type": "string"
    },
    "service": {
      "description": "Microservice name",
      "type": "string"
    }
  },
  "required": ["ip", "method", "path", "service"]
}
"""
