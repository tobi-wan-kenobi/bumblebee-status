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
import os
import tempfile
import logging
import random
import re

import bumblebee.input
import bumblebee.output
import bumblebee.engine


# pylint: disable=too-many-instance-attributes
class Module(bumblebee.engine.Module):
    REFRESH_DELAY = 600
    SCROLL_SPEED = 3
    LAYOUT_STYLES_ITEMS = [[1,1,1],[3,3,2],[2,3,3],[3,2,3]]
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.ticker_update if DEPENDENCIES_OK else self._show_error)
        )
        # Use BBC newsfeed as demo:
        self._feeds = self.parameter('feeds', 'https://www.espn.com/espn/rss/news').split(" ")
        self._refresh_countdown = 0
        self._feeds_to_update = []

        self._max_title_length = int(self.parameter("length", 60))

        self._items = []
        self._current_item = None

        self._ticker_offset = 0
        self._pre_delay = 0
        self._post_delay = 0

        self._state = []
        
        self._newspaper_filename = tempfile.mktemp('.html')

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd=self._open)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=self._create_newspaper)

    def _open(self, _):
        if self._current_item:
            webbrowser.open(self._current_item['link'])

    def _check_for_image(self, entry):
        image = next(iter([l['href'] for l in entry['links'] if l['rel']=='enclosure']), None)
        if not image and 'media_content' in entry:
            try:
                media = sorted(entry['media_content'], key=lambda i: i['height'] if 'height' in i else 0, reverse=True)
                image = next(iter([i['url'] for i in media if i['medium']=='image']), None)
            except Exception:
                pass
        if not image:
            match = re.search('<img[^>]*src\s*=["\']*([^\s^>^"^\']*)["\']*', entry['summary'])
            if match:
                image=match.group(1)
        return image if image else ''

    def _remove_tags(self, txt):
        return re.sub('<[^>]*>', '', txt)

    def _create_item(self, entry, url, feed):
        return {'title': self._remove_tags(entry['title'].replace('\n', ' ')),
                'link': entry['link'],
                'new': all([i['title'] != entry['title'] for i in self._items]),
                'source': url,
                'summary': self._remove_tags(entry['summary']),
                'feed': feed,
                'image': self._check_for_image(entry),
                'published': time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0}

    def _update_items_from_feed(self, url):
        parser = feedparser.parse(url)
        new_items = [self._create_item(entry, url, parser['feed']['title']) for entry in parser['entries']]
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

    def _create_news_element(self, item, overlay_title):
        try:
            timestr = "" if item['published'] == 0 else str(time.ctime(item['published']))
        except Exception as e:
            logging.error(str(e))
            raise e
        element = "<div class='item' onclick=window.open('"+item['link']+"')>"
        element += "<div class='titlecontainer'>"
        element += "  <img "+("" if item['image'] else "class='noimg' ")+"src='"+item['image']+"'>"
        element += "  <div class='title"+(" overlay" if overlay_title else "")+"'>"+item['title']+"</div>"
        element += "</div>"
        element += "<div class='summary'>"+item['summary']+"</div>"
        element += "<div class='info'><span class='author'>"+item['feed']+"</span><span class='published'>"+timestr+"</span></div>"
        element += "</div>"
        return element

    def _create_news_section(self, newspaper_items):
        style = random.randint(0, 3)
        section = "<table><tr class='style"+str(style)+"'>"
        for i in range(0, 3):
            section += "<td><div class='itemcontainer'>"
            for j in range(0, self.LAYOUT_STYLES_ITEMS[style][i]):
                if newspaper_items:
                    section += self._create_news_element(newspaper_items[0], self.LAYOUT_STYLES_ITEMS[style][i]!=3)
                    del newspaper_items[0]
            section += "</div></td>"
        section += "</tr></table>"
        return section
         
    def _create_newspaper(self, _):
        content = ""
        newspaper_items = self._items[:]
        while newspaper_items:
            content += self._create_news_section(newspaper_items)
        open(self._newspaper_filename, "w").write(HTML_TEMPLATE.replace("[[CONTENT]]", content))
        webbrowser.open("file://"+self._newspaper_filename)
        
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<style>
    body {background: #eee; font-family: Helvetica neue;}
    td {background: #fff; height: 100%;}
    tr.style0 td {width: 33%;}
    tr.style1 td {width: 20%;}
    tr.style1 td:last-child {width: 60%;}
    tr.style2 td {width: 20%;}
    tr.style2 td:first-child {width: 60%;}
    tr.style3 td {width: 20%;}
    tr.style3 td:nth-child(2) {width: 60%;}
    img {width: 100%; display: block; }
    img.noimg {min-height:250px; background: #1299c8;}
    #content {width: 1500px; margin: auto; background: #eee; padding: 1px;}
    #newspapertitle {text-align: center; font-size: 60px; font-family: Arial Black; background: #1299c8; font-style: Italic; padding: 10px; color: #fff; }
    .section {display: flex;}
    .column {display: flex;}
    .itemcontainer {width: 100%; height: 100%; position: relative; display: inline-table;}
    .item {cursor: pointer; }
    .titlecontainer {position: relative;}
    .title.overlay {font-family: Arial; position: absolute; bottom: 10px; color: #fff; font-weight: bold; text-align: right; max-width: 75%; right: 10px; font-size: 23px; text-shadow: 1px 0 0 #000, 0 -1px 0 #000, 0 1px 0 #000, -1px 0 0 #000;}
    .title:not(.overlay) {font-weight: bold; padding: 0px 10px;}
    .summary {color: #444; padding: 10px 10px 0px 10px; font-family: Times new roman; font-size: 18px; flex: 1;max-height: 105px; overflow: hidden;}
    .info {color: #aaa; font-family: arial; font-size: 13px; padding: 10px;}
    .published {float: right;}
</style>
<body>
  <div id='content'>
  <div id='newspapertitle'>Bumblebee Daily</div>
    [[CONTENT]]
  </div>
</body>
</html>"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
