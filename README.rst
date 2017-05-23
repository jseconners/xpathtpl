xpathtpl
====================================================


Simple xpath templating for scraping website data into python dictionary.


Examples
-------------------------------------------

Grab headlines from Digg
::

    import xpathtpl
    import requests

    template = {
        'headlines': {
            '_xpath': '//h2[@itemprop="headline"]',
        }
    }
    content = requests.get('http://digg.com', template).content
    headlines = xpathtpl.parse(content, template)
    print headlines

    > {
    >   'headlines': [
    >     'How Anker Is Beating Apple And Samsung At Their Own Accessory Game',
    >     'Trump Asked Top Intelligence Officials To Push Back Against FBI Investigation',
    >     'To Get A Sense Of How Fast Maglev Trains Travel, Watch This',
    >     'How To Run Like A Pro In 8 Weeks',
    >     ...
    >   ]
    > }

Get some additional story fields using sub-templates. Below, we grab the containing divs for each story
and then use relative expressions to fill the dictionary. Templates without sub-templates
will return a single value or an array of values. Templates with sub-templates act as loops
and run sub-templates for each element returned by containing xpath. You can also run absolute
expressions from sub-templates.
::

    import xpathtpl
    import requests

    template = {
      'stories': {
        '_xpath': '//div[@class="digg-story__content"]',
        'title': {
            '_xpath': './/h2[@itemprop="headline"]'
        },
        'alt-title': {
            '_xpath': './/div[@itemprop="alternativeHeadline"]'
        },
        'description': {
            '_xpath': './/div[@itemprop="description"]'
        },
        'digg-count': {
            '_xpath': './/span[@class="js--digg-count"]'
        }
      }
    }
    content = requests.get('http://digg.com', template).content
    headlines = xpathtpl.parse(content, template)
    print headlines

    > {
    >   'stories': [
    >     {
    >       'description': u'Steven\xa0Yang and his team started a company with the sole purpose of selling...',
    >       'digg-count': '18',
    >       'alt-title': 'PACKING A PUNCH',
    >       'title': 'How Anker Is Beating Apple And Samsung At Their Own Accessory Game'
    >     },
    >     ...
    >   ]
    > }

Templates without _xpath keys act as simple containers
::

    import xpathtpl
    import requests

    template = {
      'latest-headline': {
        'title': {
            '_xpath': '(//h2[@itemprop="headline"])[1]'
        }
      }
    }
    content = requests.get('http://digg.com', template).content
    headlines = xpathtpl.parse(content, template)
    print headlines

    > {
    >   'latest-headline': {
    >     'title': 'How Anker Is Beating Apple And Samsung At Their Own Accessory Game'
    >   }
    > }

One more thing. You can specify to use the text values from the elements returned
by the containing xpath template as keys for the evaluated sub-templates, using
the _ukeys key.

::

    import xpathtpl
    import requests

    template = {
      'stories': {
          '_xpath': '//h2[@itemprop="headline"]'
          '_ukeys': True
          'href': {
              '_xpath': './a/@href'
          }
      }
    }
    content = requests.get('http://digg.com', template).content
    headlines = xpathtpl.parse(content, template)
    print headlines

    > {
    >   'stories': {
    >     'Why American Workers Now Dress So Casually': {
    >       'url': 'https://www.theatlantic.com/business/archive/2017/05/history-of-business-casual/526014/'
    >     },
    >     'The World Is Running Out Of Sand': {
    >       'url': 'http://www.newyorker.com/magazine/2017/05/29/the-world-is-running-out-of-sand?mbid=synd_digg'
    >     },
    >     'Clown Tries To Show Off In His Fancy Supercar, Immediately Wrecks It': {
    >       'url': 'http://digg.com/2017/audi-r8-crash-wreck-idiot'
    >     },
    >     ...
    > }



Author
------

-  James Conners


