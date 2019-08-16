# pylint: disable=C0111,R0903

"""RSS news ticker

Fetches rss news items and shows these as a news ticker.
Left-clicking will open the full story in a browser.
New stories are highlighted.

Parameters:
    * rss.feeds : Space-separated list of RSS URLs
    * rss.length : Maximum length of the module, default is 60
"""

try:
    import feedparser
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False

import webbrowser
import time

import bumblebee.input
import bumblebee.output
import bumblebee.engine


# pylint: disable=too-many-instance-attributes
class Module(bumblebee.engine.Module):
    REFRESH_DELAY = 600
    SCROLL_SPEED = 3

    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.ticker_update if DEPENDENCIES_OK else self._show_error)
        )
        # Use BBC newsfeed as demo:
        self._feeds = self.parameter('feeds', 'http://feeds.bbci.co.uk/news/rss.xml').split(" ")
        self._refresh_countdown = 0
        self._feeds_to_update = []

        self._max_title_length = int(self.parameter("length", 60))

        self._items = []
        self._current_item = None

        self._ticker_offset = 0
        self._pre_delay = 0
        self._post_delay = 0

        self._state = []
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd=self._open)

    def _open(self, _):
        if self._current_item:
            webbrowser.open(self._current_item['link'])

    def _create_item(self, entry, url):
        return {'title': entry['title'].replace('\n', ' '),
                'link': entry['link'],
                'new': all([i['title'] != entry['title'] for i in self._items]),
                'source': url,
                'published': time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0}

    def _update_items_from_feed(self, url):
        parser = feedparser.parse(url)
        new_items = [self._create_item(entry, url) for entry in parser['entries']]
        # Remove the previous items
        self._items = [i for i in self._items if i['source'] != url]
        # Add the new items
        self._items.extend(new_items)
        # Sort the items on publish date
        self._items.sort(key=lambda i: i['published'], reverse=True)

    def _check_for_refresh(self):
        if self._feeds_to_update:
            # Update one feed at a time to not overload this update cycle
            url = self._feeds_to_update.pop()
            self._update_items_from_feed(url)

            if not self._current_item:
                self._next_item()
        elif self._refresh_countdown == 0:
            # Populate the list with feeds to update
            self._feeds_to_update = self._feeds[:]
            # Restart the update countdown timer
            self._refresh_countdown = self.REFRESH_DELAY
        else:
            self._refresh_countdown -= 1

    def _next_item(self):
        self._ticker_offset = 0
        self._pre_delay = 2
        self._post_delay = 4

        if not self._items:
            return

        # Index of the current element
        idx = self._items.index(self._current_item) if self._current_item in self._items else - 1

        # First show new items, else show next
        new_items = [i for i in self._items if i['new']]
        self._current_item = next(iter(new_items), self._items[(idx+1) % len(self._items)])

    def _check_scroll_done(self):
        # Check if the complete title has been shown
        if self._ticker_offset + self._max_title_length > len(self._current_item['title']):
            # Do not immediately show next item after scroll
            self._post_delay -= 1
            if self._post_delay == 0:
                self._current_item['new'] = False
                # Mark the previous item as 'old'
                self._next_item()
        else:
            # Increase scroll position
            self._ticker_offset += self.SCROLL_SPEED

    def _show_error(self, _):
        return "Please install feedparser first"

    def ticker_update(self, _):
        self._check_for_refresh()

        # If no items were retrieved, return an empty string
        if not self._current_item:
            return " "*self._max_title_length

        # Prepare a substring of the item title
        response = self._current_item['title'][self._ticker_offset:self._ticker_offset+self._max_title_length]
        # Add spaces if too short
        response = response.ljust(self._max_title_length)

        # Do not immediately scroll
        if self._pre_delay > 0:
            # Change state during pre_delay for new items
            if self._current_item['new']:
                self._state = ['warning']
            self._pre_delay -= 1
            return response

        self._state = []
        self._check_scroll_done()

        return response

    def update(self, widgets):
        pass

    def state(self, _):
        return self._state

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
