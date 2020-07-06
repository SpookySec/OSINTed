import whois

class Domain:
    def __init__(self, domain):
        domainlookup = whois.query(domain)
        self.name_servers = list(domainlookup.name_servers)
        self.owner = str(domainlookup.registrar)
        self.servers = list(domainlookup.name_servers)
        self.creation = str(domainlookup.creation_date)
        self.experation = str(domainlookup.expiration_date)
        self.update = str(domainlookup.last_updated)