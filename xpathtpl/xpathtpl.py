######################################################
#
# craigdata - pull post data from craiglist from the
# command line.
# Written by James Conners (jseconners@gmail.com)
#
######################################################

import requests
import lxml.html
import json


BASE_URL = 'https://www.craigslist.org/about/sites'

TEST_TEMPLATES = {
    'craigslist-sites': {
        'countries': {
            '_xpath': '//section[@class="body"]/h1',
            'states': {
                '_xpath': './following-sibling::div[1]/div/h4',
                '_ukeys': True,

                'cities': {
                    '_xpath': './following-sibling::ul[1]/li/a'
                }
            }
        }
    },
    'github-showcases1': {
        'showcases': {
            '_xpath': '//h3[@class="exploregrid-item-title"]',
        }
    },
    'github-showcases2': {
        'showcases': {
            '_xpath': '//ul[@class="exploregrid gut-md"]//a',
            'href': {
                '_xpath': './@href'
            },
            'title': {
                '_xpath': './h3[1]/text()'
            },
        }
    }
}

def _page_obj(url):
    content = requests.get(url).content
    return lxml.html.fromstring(content)


def _text(e):
    """ Try to get the text content of this element """
    try:
        text = e.text_content()
    except AttributeError:
        text = str(e)
    return text.strip()


def _apply_tpl(tpl, e):
    """ Apply the template tpl to HTML element e """
    # remove processing instruction attributes
    # xpath expression to build from
    _xpath = tpl.get('_xpath', None)
    _ukeys = tpl.get('_ukeys', False)

    # get sub templates
    subs = dict([(s, tpl[s].copy()) for s in tpl.keys() if not s.startswith('_')])

    # check if this is just a named container and process sub templates
    # if available. sub templates inherit html element for
    # running xpath expressions
    if _xpath is None:
        container = {}
        if len(subs):
            for sn in subs.keys():
                container[sn] = _apply_tpl(e, subs[sn])
            return container
        else:
            return None

    # if _ukeys is True, you always get an dictionary
    # container with return element values as keys
    if _ukeys:
        elms = {}
    else:
        elms = []

    for elm in e.xpath(_xpath):
        # has sub templates. Needs to be in a
        # dictionary container
        if len(subs):
            val = {}
            for sn in subs.keys():
                val[sn] = _apply_tpl(subs[sn], elm)

        # no sub templates, so this could possibly
        else:
            val = _text(elm)

        # add to container appropriately
        if _ukeys:
            elms[_text(elm)] = val
        else:
            elms.append(val)

    # if this is a single-item list, just
    # return that item without the container
    if not _ukeys and (len(elms) == 1):
        return elms[0]
    else:
        return elms


def _template_page(page, tpl):
    for top_name in tpl:
        tpl[top_name] = _apply_tpl(tpl[top_name], page)
    return tpl


def parse_page(url, tpl):
    page = _page_obj(url)
    return _template_page(page, tpl)


#obj = parse_page(BASE_URL, template)
obj = parse_page('https://github.com/explore', TEST_TEMPLATES['github-showcases2'])
print json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
