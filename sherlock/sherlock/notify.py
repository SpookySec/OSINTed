"""Sherlock Notify Module

This module defines the objects for notifying the caller about the
results of queries.
"""
from sherlock.sherlock.result import QueryStatus

white = '\033[97m'
green = '\033[92m'
red = '\033[91m'
yellow = '\033[93m'
end = '\033[0m'
info = '\033[93m[!] \033[0m'
que = '\033[94m[?] \033[0m'
bad = '\033[91m[-] \033[0m'
good = '\033[32m[+] \033[0m'
run = '\033[97m[~] \033[0m' 


class QueryNotify():
    """Query Notify Object.

    Base class that describes methods available to notify the results of
    a query.
    It is intended that other classes inherit from this base class and
    override the methods to implement specific functionality.
    """
    def __init__(self, result=None):
        """Create Query Notify Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """

        self.result = result

        return

    def start(self, message=None):
        """Notify Start.

        Notify method for start of query.  This method will be called before
        any queries are performed.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        message                -- Object that is used to give context to start
                                  of query.
                                  Default is None.

        Return Value:
        Nothing.
        """

        return

    def update(self, result):
        """Notify Update.

        Notify method for query result.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """

        self.result = result

        return

    def finish(self, message=None):
        return

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        result = str(self.result)

        return result


class QueryNotifyPrint(QueryNotify):
    """Query Notify Print Object.

    Query notify class that prints results.
    """
    def __init__(self, result=None, verbose=False, print_found_only=False,
                 color=True):
        """Create Query Notify Print Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        verbose                -- Boolean indicating whether to give verbose output.
        print_found_only       -- Boolean indicating whether to only print found sites.
        color                  -- Boolean indicating whether to color terminal output

        Return Value:
        Nothing.
        """

        # Colorama module's initialization.
        return

    def start(self, message):
        title = "Checking username"
        print(run + white + f"{title}" + yellow + f" {message}" + white + " on:" + end)
        return

    def update(self, result):

        self.result = result

        #Output to the terminal is desired.
        if result.status == QueryStatus.CLAIMED:
            print(good + yellow + f"{self.result.site_name}: " + end + f"{self.result.site_url_user}")

        elif result.status == QueryStatus.AVAILABLE:
            print(bad +
                yellow + f"{self.result.site_name}:" +
                red + " Not found!" + end)
        elif result.status == QueryStatus.UNKNOWN:
            print(
                bad + yellow + f"{self.result.site_name}:" +
                red + f" {self.result.context}" + end)
        elif result.status == QueryStatus.ILLEGAL:
            msg = "Username illegal for this website!"
            print(bad + yellow +
                    f"{self.result.site_name}:" +
                    red + f" {msg}" + end)
        else:
            #It should be impossible to ever get here...
            raise ValueError(f" WOWWWW GOOOODLUCK YOU'RE A PRO TESTER... Unknown Query Status '{str(result.status)}' for "
                             f"site '{self.result.site_name}'")

        return

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        result = str(self.result)

        return result
