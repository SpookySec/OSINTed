#! /usr/bin/env python3

"""
Sherlock: Find Usernames Across Social Networks Module

This module contains the main logic to search for usernames at social
networks.
"""
import os
import re
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from time import monotonic

import requests

from requests_futures.sessions import FuturesSession
from sherlock.sherlock.result import QueryStatus
from sherlock.sherlock.result import QueryResult
from sherlock.sherlock.notify import QueryNotifyPrint
from sherlock.sherlock.sites  import SitesInformation

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

class SherlockFuturesSession(FuturesSession):
    def request(self, method, url, hooks={}, *args, **kwargs):
        #Record the start time for the request.
        start = monotonic()

        def response_time(resp, *args, **kwargs):
            resp.elapsed = monotonic() - start

            return

        #Install hook to execute when response completes.
        #Make sure that the time measurement hook is first, so we will not
        #track any later hook's execution time.
        try:
            if isinstance(hooks['response'], list):
                hooks['response'].insert(0, response_time)
            elif isinstance(hooks['response'], tuple):
                #Convert tuple to list and insert time measurement hook first.
                hooks['response'] = list(hooks['response'])
                hooks['response'].insert(0, response_time)
            else:
                #Must have previously contained a single hook function,
                #so convert to list.
                hooks['response'] = [response_time, hooks['response']]
        except KeyError:
            #No response hook was already defined, so install it ourselves.
            hooks['response'] = [response_time]

        return super(SherlockFuturesSession, self).request(method,
                                                           url,
                                                           hooks=hooks,
                                                           *args, **kwargs)

def get_response(request_future, error_type, social_network):

    #Default for Response object if some failure occurs.
    response = None

    error_context = "General Unknown Error"
    expection_text = None
    try:
        response = request_future.result()
        if response.status_code:
            #status code exists in response object
            error_context = None
    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        expection_text = str(errh)
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        expection_text = str(errp)
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        expection_text = str(errc)
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        expection_text = str(errt)
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        expection_text = str(err)

    return response, error_context, expection_text


def sherlock(username, site_data, query_notify):

    #Notify caller that we are starting the query.
    query_notify.start(username)

    underlying_session = requests.session()
    underlying_request = requests.Request()

    #Limit number of workers to 20.
    #This is probably vastly overkill.
    if len(site_data) >= 20:
        max_workers=20
    else:
        max_workers=len(site_data)

    #Create multi-threaded session for all requests.
    session = SherlockFuturesSession(max_workers=max_workers,
                                     session=underlying_session)


    # Results from analysis of all sites
    results_total = {}

    # First create futures for all requests. This allows for the requests to run in parallel
    for social_network, net_info in site_data.items():

        # Results from analysis of this specific site
        results_site = {}

        # Record URL of main site
        results_site['url_main'] = net_info.get("urlMain")

        # A user agent is needed because some sites don't return the correct
        # information since they think that we are bots (Which we actually are...)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }

        if "headers" in net_info:
            # Override/append any extra headers required by a given site.
            headers.update(net_info["headers"])

        # URL of user on site (if it exists)
        url = net_info["url"].format(username)

        # Don't make request if username is invalid for the site
        regex_check = net_info.get("regexCheck")
        if regex_check and re.search(regex_check, username) is None:
            # No need to do the check at the site: this user name is not allowed.
            results_site['status'] = QueryResult(username,
                                                 social_network,
                                                 url,
                                                 QueryStatus.ILLEGAL)
            results_site["url_user"] = ""
            results_site['http_status'] = ""
            results_site['response_text'] = ""
            query_notify.update(results_site['status'])
        else:
            # URL of user on site (if it exists)
            results_site["url_user"] = url
            url_probe = net_info.get("urlProbe")
            if url_probe is None:
                # Probe URL is normal one seen by people out on the web.
                url_probe = url
            else:
                # There is a special URL for probing existence separate
                # from where the user profile normally can be found.
                url_probe = url_probe.format(username)

            if (net_info["errorType"] == 'status_code' and 
                net_info.get("request_head_only", True) == True):
                #In most cases when we are detecting by status code,
                #it is not necessary to get the entire body:  we can
                #detect fine with just the HEAD response.
                request_method = session.head
            else:
                #Either this detect method needs the content associated
                #with the GET response, or this specific website will
                #not respond properly unless we request the whole page.
                request_method = session.get

            if net_info["errorType"] == "response_url":
                # Site forwards request to a different URL if username not
                # found.  Disallow the redirect so we can capture the
                # http status from the original URL request.
                allow_redirects = False
            else:
                # Allow whatever redirect that the site wants to do.
                # The final result of the request will be what is available.
                allow_redirects = True

            # This future starts running the request in a new thread, doesn't block the main thread
            future = request_method(url=url_probe, headers=headers,
                                    allow_redirects=allow_redirects)

            # Store future in data for access later
            net_info["request_future"] = future

        # Add this site's results into final dictionary with all of the other results.
        results_total[social_network] = results_site

    # Open the file containing account links
    # Core logic: If tor requests, make them here. If multi-threaded requests, wait for responses
    for social_network, net_info in site_data.items():

        # Retrieve results again
        results_site = results_total.get(social_network)

        # Retrieve other site information again
        url = results_site.get("url_user")
        status = results_site.get("status")
        if status is not None:
            # We have already determined the user doesn't exist here
            continue

        # Get the expected error type
        error_type = net_info["errorType"]

        # Retrieve future and ensure it has finished
        future = net_info["request_future"]
        r, error_text, expection_text = get_response(request_future=future,
                                                     error_type=error_type,
                                                     social_network=social_network)

        #Get response time for response of our request.
        try:
            response_time = r.elapsed
        except AttributeError:
            response_time = None

        # Attempt to get request information
        try:
            http_status = r.status_code
        except:
            http_status = "?"
        try:
            response_text = r.text.encode(r.encoding)
        except:
            response_text = ""

        if error_text is not None:
            result = QueryResult(username,
                                 social_network,
                                 url,
                                 QueryStatus.UNKNOWN,
                                 query_time=response_time,
                                 context=error_text)
        elif error_type == "message":
            error = net_info.get("errorMsg")
            # Checks if the error message is in the HTML
            if not error in r.text:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.CLAIMED,
                                     query_time=response_time)
            else:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.AVAILABLE,
                                     query_time=response_time)
        elif error_type == "status_code":
            # Checks if the status code of the response is 2XX
            if not r.status_code >= 300 or r.status_code < 200:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.CLAIMED,
                                     query_time=response_time)
            else:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.AVAILABLE,
                                     query_time=response_time)
        elif error_type == "response_url":
            # For this detection method, we have turned off the redirect.
            # So, there is no need to check the response URL: it will always
            # match the request.  Instead, we will ensure that the response
            # code indicates that the request was successful (i.e. no 404, or
            # forward to some odd redirect).
            if 200 <= r.status_code < 300:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.CLAIMED,
                                     query_time=response_time)
            else:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.AVAILABLE,
                                     query_time=response_time)
        else:
            #It should be impossible to ever get here...
            raise ValueError(f"Unknown Error Type '{error_type}' for "
                             f"site '{social_network}'")


        #Notify caller about results of query.
        query_notify.update(result)

        # Save status of request
        results_site['status'] = result

        # Save results from request
        results_site['http_status'] = http_status
        results_site['response_text'] = response_text

        # Add this site's results into final dictionary with all of the other results.
        results_total[social_network] = results_site

    #Notify caller that all queries are finished.
    query_notify.finish()

    return results_total


def UserSearch(username):
    site_data_all = {}
    try:
        sites = SitesInformation(None)
        
    except Exception as error:
        print(f"ERROR:  {error}")
        sys.exit(1)

    for site in sites:
        site_data_all[site.name] = site.information

    site_data = site_data_all

    query_notify = QueryNotifyPrint(result=None)
    results = sherlock(username, site_data, query_notify)
    exists_counter = 0
    for website_name in results:
        dictionary = results[website_name]
        if dictionary.get("status").status == QueryStatus.CLAIMED:
            exists_counter += 1
    
    print(good + white + f"Total websites username detected : {exists_counter}")