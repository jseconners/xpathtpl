xpathtpl
====================================================


Simple xpath templating for scraping website data into
python dictionary

Examples
-------------------------------------------
Grab the Digg headlines
::

    import xpathtpl
    import requests

    template = {
        'headlines': {
            '_xpath': '//header[@class="digg-story__header"]//h2[@itemprop="headline"]',
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
    >     'How To Run Like A Pro In 8 Weeks'
    >   ]
    > }


Author
------

-  James Conners


