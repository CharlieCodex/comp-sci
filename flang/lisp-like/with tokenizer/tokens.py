import re


class Rule:
    def __init__(self, name, keyword, sub_rules, recursive_rule=False):
        self.name = name
        self.keyword = keyword

        if recursive_rule:
            sub_rules = Ruleset(sub_rules.append(self))

        self.sub_rules = sub_rules


class Ruleset:
    def __init__(self, rules, break_cond=lambda t: t.isspace()):
        self.rules = rules
        self.break_cond = break_cond
        if rules:
            self.kwmap = {rule.keyword: rule for rule in rules}

    def get(self, token):
        for kw in self.kwmap:
            if(re.fullmatch(kw, token)):
                return self.kwmap[kw]


class Tokenizer:
    def __init__(self, rules, text):
        self.state = [rules]
        self.ast = []
        self.depth = 0
        self.text = text
        self.char_num = 0

    def read(self):
        tokens = []
        while not self.finished():
            print('new token')
            rules = self.state[self.depth]
            self.whitespace()
            rule = None
            cur_token = ''
            while not rule or self.finished():
                while not(rules.break_cond(self.current()) or self.finished()):
                    cur_token += self.next()
                    print(cur_token)
                rule = rules.get(cur_token)
                if rule:
                    print('> > > Matched {}'.format(cur_token))
                    if rule.sub_rules:
                        self.depth = self.state.append(rule.sub_rules)
                    tokens.append(rule.name)
                else:
                    print('> > > no match, adding next atom')
        print(tokens)

    def whitespace(self):
        n = 0
        while self.current().isspace() and not self.finished():
            self.next()
            n += 1
        print('skipped {} chars'.format(n))

    def next(self):
        if len(self.text) <= self.char_num:
            return self.text[-1]
        char = self.text[self.char_num]
        self.char_num += 1
        return char

    def current(self):
        if len(self.text) <= self.char_num:
            return self.text[-1]
        return self.text[self.char_num]

    def finished(self):
        return len(self.text) <= self.char_num


if __name__ == '__main__':
    int_literal = Rule('int_lit', r'\d+', None)
    str_literal = Rule('str_lit', r'"([^"]*\s*)*"',
                       Ruleset(None,
                               break_cond=(lambda x: x == '"')))
    rules = Ruleset((int_literal, str_literal))
    tokener = Tokenizer(rules, '10 "211 20"')
