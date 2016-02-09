__author__ = 'mladen'


def correct_punctuation(text, first_capital=True):
    first_was_capital = text[0].isupper()

    def no_space_after(t, p):
        return t.replace(p + ' ', p)

    def no_space_before(t, p):
        return t.replace(' ' + p, p)

    def capitalize_first(t):
        return process_first(t, lambda x: x.capitalize())

    def lowercase_first(t):
        return process_first(t, lambda x: x.lower())

    def process_first(t, procfunc):
        fw = t.split()[0]
        tl = list(fw)
        for ti in tl:
            if ti in string.punctuation:
                return t
        tl = list(t)
        for ti in xrange(len(tl)):
            if tl[ti] not in string.punctuation and tl[ti] != ' ':
                tl[ti] = procfunc(tl[ti])
                break
        return "".join(tl)

    capital_words = ['i']
    tokens = tokenize(text)
    result = "".join([" " + i if (i not in string.punctuation
                                  and not i.startswith("'")) else i
                      for i in tokens])
    for c in ['!', '?', '.', ',', ':', ')', ']', '}', '>']:
        result = no_space_before(result, c)

    for c in ['(', '[', '{', '<']:
        result = no_space_after(result, c)

    result = result.replace('"', ' " ')
    for s in capital_words:
        rgx = re.compile(r'\b(%s)\b' % re.escape(s), re.IGNORECASE)
        result = re.sub(rgx, lambda pat: pat.group(1).capitalize(), result)
    result = " ".join([capitalize_first(s.strip()) for s in sent_tokenize(result)])
    result = re.sub('\s+', ' ', result).strip()
    if first_capital or first_was_capital:
        result = capitalize_first(result)
    elif not first_was_capital:
        result = lowercase_first(result)
    result = result.strip()
    return result



def match_similar(tweets, against, min_ratio=0.95):
    for i in xrange(len(tweets)):
        t = tweets[i]
        sim = {x['tweet']: x['ratio'] for x in t.get('similars', [])}

        for j in xrange(len(against)):
            t2 = against[j]
            if t2['_id'] == t['_id']:
                continue

            ratio = Levenshtein.ratio(strclean(t['text']), strclean(t2['text']))
            if ratio > min_ratio:
                sim[t2['_id']] = ratio
        t['similars'] = list()
        for tkey, tratio in sim.iteritems():
            t['similars'].append({"tweet": tkey, "ratio": tratio})

    return tweets
