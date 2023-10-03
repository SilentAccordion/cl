import requests               # To get the pages
from bs4 import BeautifulSoup # and to process them

from time import sleep      # Allowing us to pause between pulls
from random import random   # And allowing that pause to be random

# import textwrap             # Useful for our wrapped output

import os
import os.path

# from bs4.element import Comment

import sqlite3
from sqlite3 import Error

import hashlib

def fetch(url):

    # print(output_file_name)
    
    if os.path.isfile(output_file_name):
        print("skipping: "+output_file_name)
        with open(output_file_name,'r') as infile :
            return infile.read()
    # pull the page 
    r = requests.get(url)
    
    # write out the page to a file with the appropriate name
    with open(output_file_name,'w') as outfile :
        # for piece in textwrap.wrap(r.text) :
            # outfile.write(piece+'\n')
        outfile.write(r.text)

    # sleep(wait_time)
    return r.text

def generate_filename_from_url(url) :
    
    # Put code here from scraping exercise
    # return("")
    
    # initial attempt to just grab actual file name from link
    # return(url.split('/')[-1]+'.txt')
    
    if not url :
        return None
    
    # drop the http or https
    name = url.replace("https","").replace("http","")

    # Replace useless chareacters with UNDERSCORE
    name = name.replace("://","").replace(".","_").replace("/","_")
    
    # remove last underscore
    last_underscore_spot = name.rfind("_")
    
    name = name[:last_underscore_spot] + name[(last_underscore_spot+1):]

    # tack on .txt
    name = "data/" + name + ".txt"
    
    return(name)

def process_file(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.find_all("li", class_="cl-static-search-result")

def process_listings(listings):
    hrefs = []
    for listing in listings:
        # print(listing)
        # for a in 
        href = listing.find('a', href=True).attrs['href']
        # print(href)
        # print(a)
        # print("Found the URL:", a['href'])
        hrefs.append(href)
    return hrefs

protocol = "https://"
url =".craigslist.org/search/cta"


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    
    return False


conn = create_connection(r"./db/sqlite.db")


if conn:

    c = conn.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS "links" ( \
	"ID"	INTEGER, \
	"url"	TEXT, \
	"status"	INTEGER, \
	PRIMARY KEY("ID" AUTOINCREMENT) \
    );'
    c.execute(sql)

    cities = ["auburn","bham","dothan","shoals","gadsden","huntsville","mobile","montgomery","tuscaloosa","anchorage","fairbanks","kenai","juneau","flagstaff","mohave","phoenix","prescott","showlow","sierravista","tucson","yuma","fayar","fortsmith","jonesboro","littlerock","texarkana","bakersfield","chico","fresno","goldcountry","hanford","humboldt","imperial","inlandempire","losangeles","mendocino","merced","modesto","monterey","orangecounty","palmsprings","redding","sacramento","sandiego","sfbay","slo","santabarbara","santamaria","siskiyou","stockton","susanville","ventura","visalia","yubasutter","boulder","cosprings","denver","eastco","fortcollins","rockies","pueblo","westslope","newlondon","hartford","newhaven","nwct","delaware","washingtondc","miami","daytona","keys","fortlauderdale","fortmyers","gainesville","cfl","jacksonville","lakeland","miami","lakecity","ocala","okaloosa","orlando","panamacity","pensacola","sarasota","miami","spacecoast","staugustine","tallahassee","tampa","treasure","miami","albanyga","athensga","atlanta","augusta","brunswick","columbusga","macon","nwga","savannah","statesboro","valdosta","honolulu","boise","eastidaho","lewiston","twinfalls","bn","chambana","chicago","decatur","lasalle","mattoon","peoria","rockford","carbondale","springfieldil","quincy","bloomington","evansville","fortwayne","indianapolis","kokomo","tippecanoe","muncie","richmondin","southbend","terrehaute","ames","cedarrapids","desmoines","dubuque","fortdodge","iowacity","masoncity","quadcities","siouxcity","ottumwa","waterloo","lawrence","ksu","nwks","salina","seks","swks","topeka","wichita","bgky","eastky","lexington","louisville","owensboro","westky","batonrouge","cenla","houma","lafayette","lakecharles","monroe","neworleans","shreveport","maine","annapolis","baltimore","easternshore","frederick","smd","westmd","boston","capecod","southcoast","westernmass","worcester","annarbor","battlecreek","centralmich","detroit","flint","grandrapids","holland","jxn","kalamazoo","lansing","monroemi","muskegon","nmi","porthuron","saginaw","swmi","thumb","up","bemidji","brainerd","duluth","mankato","minneapolis","rmn","marshall","stcloud","gulfport","hattiesburg","jackson","meridian","northmiss","natchez","columbiamo","joplin","kansascity","kirksville","loz","semo","springfield","stjoseph","stlouis","billings","bozeman","butte","greatfalls","helena","kalispell","missoula","montana","grandisland","lincoln","northplatte","omaha","scottsbluff","elko","lasvegas","reno","nh","cnj","jerseyshore","newjersey","southjersey","albuquerque","clovis","farmington","lascruces","roswell","santafe","albany","binghamton","buffalo","catskills","chautauqua","elmira","fingerlakes","glensfalls","hudsonvalley","ithaca","longisland","newyork","oneonta","plattsburgh","potsdam","rochester","syracuse","twintiers","utica","watertown","asheville","boone","charlotte","eastnc","fayetteville","greensboro","hickory","onslow","outerbanks","raleigh","wilmington","winstonsalem","bismarck","fargo","grandforks","nd","akroncanton","ashtabula","athensohio","chillicothe","cincinnati","cleveland","columbus","dayton","limaohio","mansfield","sandusky","toledo","tuscarawas","youngstown","zanesville","lawton","enid","oklahomacity","stillwater","tulsa","bend","corvallis","eastoregon","eugene","klamath","medford","oregoncoast","portland","roseburg","salem","altoona","chambersburg","erie","harrisburg","lancaster","allentown","meadville","philadelphia","pittsburgh","poconos","reading","scranton","pennstate","williamsport","york","providence","charleston","columbia","florencesc","greenville","hiltonhead","myrtlebeach","nesd","csd","rapidcity","siouxfalls","sd","chattanooga","clarksville","cookeville","jacksontn","knoxville","memphis","nashville","tricities","abilene","amarillo","austin","beaumont","brownsville","collegestation","corpuschristi","dallas","nacogdoches","delrio","elpaso","galveston","houston","killeen","laredo","lubbock","mcallen","odessa","sanangelo","sanantonio","sanmarcos","bigbend","texoma","easttexas","victoriatx","waco","wichitafalls","logan","ogden","provo","saltlakecity","stgeorge","burlington","charlottesville","danville","fredericksburg","norfolk","harrisonburg","lynchburg","blacksburg","richmond","roanoke","swva","winchester","bellingham","kpr","moseslake","olympic","pullman","seattle","skagit","spokane","wenatchee","yakima","charlestonwv","martinsburg","huntington","morgantown","wheeling","parkersburg","swv","wv","appleton","eauclaire","greenbay","janesville","racine","lacrosse","madison","milwaukee","northernwi","sheboygan","wausau","wyoming"]
    links = []
    for city in cities:
        full_url = protocol + city + url
        print(full_url)
        output_file_name = generate_filename_from_url(full_url)
        
        # Read file, from cache or remote if needed
        text = fetch(full_url)
        
        listings = process_file(text)
        
        new_links = process_listings(listings)
        
        print(len(new_links))
        # print(links)

        for link in new_links:
            sql = 'INSERT OR IGNORE INTO "links" (url, status) values ("%s", 0)' % (link)
            c.execute(sql)

        links = links + new_links

    print(len(links))
    
    conn.commit()
    conn.close()
