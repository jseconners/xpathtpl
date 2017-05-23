######################################################
#
# xpathtpl - simple xpath templating for scraping
# web page content into python dictionary
#
# Written by James Conners (jseconners@gmail.com)
#
######################################################

import lxml.html


def _text(e):
    """ Try to get the text content of this element """
    try:
        text = e.text_content()
    except AttributeError:
        text = e
    return text.strip()


def _apply_tpl(tpl, e):
    """ Apply the template tpl to HTML element e """
    _xpath = tpl.get('_xpath', None)
    _ukeys = tpl.get('_ukeys', False)

    # copy sub templates
    subs = dict([(s, tpl[s].copy()) for s in tpl.keys() if not s.startswith('_')])

    # check if this is just a named container and process sub templates
    # if available. sub templates inherit html element for
    # running xpath expressions
    if _xpath is None:
        container = {}
        if len(subs):
            for sn in subs.keys():
                container[sn] = _apply_tpl(subs[sn], e)
            return container
        else:
            return None

    # initialize container for xpath-matched elements
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

        # no sub templates, get as single text value
        else:
            val = _text(elm)

        # add to container appropriately
        if _ukeys:
            elms[_text(elm)] = val
        else:
            elms.append(val)

    # return single text values without container
    if not _ukeys and (len(elms) == 1) and (type(elms[0]) is not dict):
        return elms[0]
    else:
        return elms


def parse(bcontent, tpl):
    """ Parse page (binary string), applying xpath template """
    page = lxml.html.fromstring(bcontent)
    for top_name in tpl:
        tpl[top_name] = _apply_tpl(tpl[top_name], page)
    return tpl

