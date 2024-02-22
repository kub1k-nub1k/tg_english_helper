from translate import Translator


def translate(disc):
    trans = Translator(from_lang="en", to_lang="uk")
    trdisc = trans.translate(disc)
    return trdisc
