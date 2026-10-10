import urllib.request

urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuUSC60HFeFXwoWGHnzOEY_C0L1RjS4bWeSPIfnUe39yRz1QaaC3_xoDCacNrYjFl4zxKwxfOD7BUMO8uIupHpeppeft4m7s6h8xFv_pQgDHr8o2NtJIxVjSPv5Cbk90-RgY5FJdTf5By2kFgIbiPoR9jWDBqOvAUQU58rWj1GTCRusIgXSPhbqXDAR5ZG_k3IUWUb4O5dFK0KkR9tOHIjTFTja2KpZE4=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFF-Tjtcfn9QXljTa8Ya0ovcvjEdKU4W_DLw34HK9CKSBQXLLWtUmPLOm70maL-uYWJL0gZVFq0hFEN_Jz-QnDkhUhbein3yfwoo4h75wcZ1y2HWZdfc9Rjqe84mJN7i8gwJ_9ScPDSV96aqH3NT8vtiiDO9_HAffm7THqa6c5BX1_cKfLIBJ8r8Rut1esvSffhFwhVyzJOxFDkXZjMqm99No7H8TZ7LiCqXR48TxIvNA=="
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            print("Redirects to:", resp.geturl())
    except Exception as e:
        print("Error:", e)
