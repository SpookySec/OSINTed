from mac_vendor_lookup import MacLookup

def GetVendor(address):
    return MacLookup().lookup(address)