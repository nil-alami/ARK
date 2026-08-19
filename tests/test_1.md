Organization
    └── Business = tenant/data-isolation boundary


Organization owner/admin
        ↓
configures source + permissions
        ↓
Platform API client/service account
        ↓
authorized for Business A
        ↓
ingests Customers / Products / Transactions

**Nothing accesses the lake directly**
Capability → ❌ Object Storage
Capability → ❌ Parquet files
Capability → ❌ S3 paths
Capability → ❌ customer table

except:
the large-upload mechanism from your document intentionally allows:
Platform
   ↓
short-lived pre-signed upload URL
   ↓
one exact object-storage location
`The client gets permission to perform something equivalent to:`
PUT exactly this object
before 10:42
maximum 5 GB
for tenant X
for upload session Y

It does not receive object-store credentials or browsing/read access.


## one giant "Data Exposer" module