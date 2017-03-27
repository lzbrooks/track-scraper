import sys

from rest_calls_and_utils import set_up_logging_file, set_up_logging_to_console, get_webpage_soup

logging = set_up_logging_file()
set_up_logging_to_console()


def scraper_practice(possible_proxy_settings):
    logging.info("Starting Scraper Practice")
    # TODO: figure out when to stop scraping infinite scroll pages
    i = 0
    while i < 77:
        webpage_url = "https://8tracks.com/users/dakre/favorite_tracks" + "?page=" + str(i)
        webpage_soup = get_webpage_soup(webpage_url, possible_proxy_settings)
        all_fav_tracks = webpage_soup.find_all("li", class_="track fav_track")
        scrape_section(all_fav_tracks)
        i += 1
    logging.info("Finished Scraper Practice")


def scrape_section(all_fav_tracks):
    for fav_track in all_fav_tracks:
        fav_track_info = fav_track.find(class_="track_info")
        fav_track_title = fav_track_info.find(class_="t").string
        fav_track_artist = fav_track_info.find(class_="a").string
        fav_track_details = fav_track.find(class_="track_details")
        fav_track_album = ""
        if fav_track_details.find(class_="album"):
            if fav_track_details.find(class_="album").find(class_="detail").contents:
                fav_track_album = fav_track_details.find(class_="album").find(class_="detail").string
        fav_track_year = ""
        if fav_track.find(class_="year"):
            fav_track_year = fav_track.find(class_="year").find(class_="detail").string
        logging.info(fav_track_title + " by " + fav_track_artist + " in " + fav_track_album + ", " + fav_track_year)


# Main Function Call
if __name__ == '__main__':
    # TODO: Make manual page for proxy settings input (and user input)
    proxy_settings = {}
    if sys.argv[1]:
        http_proxy = str(sys.argv[1])
        proxy_settings.update({"http": http_proxy})
    if sys.argv[2]:
        https_proxy = str(sys.argv[2])
        proxy_settings.update({"https": https_proxy})
    scraper_practice(proxy_settings)
