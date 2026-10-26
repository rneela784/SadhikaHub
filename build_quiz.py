"""Build validated, self-contained quiz editions; never replace an archived edition."""
from pathlib import Path
from collections import Counter
from datetime import date
import html
import json
import os
import re

ROOT = Path(__file__).resolve().parent
def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def validate(data):
    assert set(data) == {'questions'}, 'Expected the original questions JSON schema'
    qs = data['questions']
    assert len(qs) == 23, 'Exactly 23 questions required'
    assert [q['category'] for q in qs] == ['India'] * 13 + ['Middle East'] * 3 + ['Global'] * 4 + ['IIT Bonus'] * 3
    assert len({q['question'].casefold().strip() for q in qs}) == 23, 'Duplicate question'
    for q in qs:
        assert set(q) == {'category', 'question', 'options', 'answer', 'difficulty', 'hint'}
        assert isinstance(q['question'], str) and q['question'].strip()
        assert len(q['options']) == 4 and len(set(q['options'])) == 4
        assert all(isinstance(o, str) and o.strip() for o in q['options'])
        assert q['options'].count(q['answer']) == 1
        assert q['difficulty'] in {'easy', 'medium', 'hard'}
        assert isinstance(q['hint'], str)
        assert bool(q['hint'].strip()) == (q['difficulty'] == 'hard' or q['category'] == 'IIT Bonus')
    assert all(qs[20 + i]['question'].startswith(subject + ':') for i, subject in enumerate(['Physics', 'Chemistry', 'Mathematics']))

def shell(title, body, prefix='', script=''):
    css = (ROOT / 'quiz-assets/quiz.css').read_text(encoding='utf-8')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A weekly adventure in general knowledge: 20 GK questions and 3 science and maths challenges.">
<title>{html.escape(title)} | Sadhika Hub</title><style>{css}</style></head>
<body><div class="wrap"><header class="top"><a class="brand" href="{prefix}index.html">Sadhika Hub <span aria-hidden="true">✦</span></a>
<nav class="nav" aria-label="Main"><a href="{prefix}quiz.html">Latest quiz</a><a href="{prefix}quiz-archive.html">Past quizzes</a></nav></header>
<main>{body}</main><footer>A little curiosity, every week. <span aria-hidden="true">✦</span> New quizzes on Saturdays.<br>One mark per correct answer. No negative marking. Scores stay on this page and are not uploaded.</footer>
</div>{script}</body></html>'''

def render(edition, data, prefix=''):
    esc = html.escape
    readable = date.fromisoformat(edition['date']).strftime('%d %B %Y').lstrip('0')
    sections = {'India':('01 / INDIA','Around India','13 questions · places, people, culture and discoveries'), 'Middle East':('02 / MIDDLE EAST','Neighbourhood discoveries','3 questions · explore the Middle East'), 'Global':('03 / WORLD','A little further afield','4 questions · wonders from around the world'), 'IIT Bonus':('04 / BONUS ROUND','Sneak peak - IIT Bonus Questions','3 original, simplified challenges · Physics, Chemistry, Mathematics. Inspired by JEE-style concepts; not past-paper questions.')}
    cards = []
    last = None
    for i, q in enumerate(data['questions']):
        if q['category'] != last:
            eyebrow, heading, desc = sections[q['category']]
            cards.append(f'<div class="sectionhead"><div class="eyebrow">{eyebrow}</div><h2>{heading}</h2><p>{desc}</p></div>')
            last = q['category']
        options = ''.join(f'<label class="option"><input type="radio" name="q{i}" value="{j}"><span>{esc(o)}</span></label>' for j, o in enumerate(q['options']))
        hint = f'<details><summary>Need a hint?</summary><p>{esc(q["hint"])}</p></details>' if q['hint'] else ''
        cards.append(f'''<section class="card" id="question-{i}" role="group" aria-labelledby="question-title-{i}">
<div class="meta"><span>QUESTION {i+1:02d} / 23</span><span class="difficulty {q['difficulty']}">{q['difficulty']}</span></div>
<h3 class="question-title" id="question-title-{i}">{esc(q['question'])}</h3><div class="options">{options}</div>{hint}<p class="feedback" hidden></p></section>''')
    body = f'''<div class="eyebrow">THE WEEKLY QUIZ · {esc(edition['label'])}</div><h1>Hello, curious mind.</h1>
<p class="intro">From India's stories to the wonders of the world. Pick your answers, follow your curiosity, and finish with a little science and maths adventure.</p>
<div class="pills"><span class="pill">{readable}</span><span class="pill">20 GK + 3 bonus</span><span class="pill">No timer · take your time</span></div>
<div class="progressbox"><div class="progressline"><span id="progress-label">0 of 23 answered</span><span id="remaining">23 left to explore</span></div><progress id="progress" max="23" value="0" aria-label="Questions answered"></progress></div>
<noscript><p>Please enable JavaScript to submit answers and see your score.</p></noscript>
<section id="results" class="results" aria-labelledby="results-title" tabindex="-1" hidden><h2 id="results-title">Your results</h2>
<div class="scores"><div class="score"><span>General knowledge</span><strong id="gk-score"></strong></div><div class="score"><span>Bonus round</span><strong id="bonus-score"></strong></div><div class="score"><span>Total marks</span><strong id="total-score"></strong></div></div><p id="result-message"></p><button id="retry-button" type="button" class="secondary">Try again</button></section>
<form id="quiz-form">{''.join(cards)}<div class="submitbox"><h2>Ready for the reveal?</h2><p id="submit-note" class="fine"></p><button class="primary" id="submit-button" type="submit">Submit my answers →</button><p class="fine">Your score and the correct answers appear after you submit.</p></div></form>'''
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    script = (ROOT / 'quiz-assets/quiz.js').read_text(encoding='utf-8')
    return shell(f'Weekly GK Quiz · {readable}', body, prefix, f'<script id="quiz-data" type="application/json">{payload}</script><script>{script}</script>')

def main():
    editions = read_json(ROOT / 'quizzes/manifest.json')['editions']
    assert editions and len({e['date'] for e in editions}) == len(editions), 'Invalid edition dates'
    editions = sorted(editions, key=lambda e: e['date'])
    prepared = {}
    seen = set()
    for e in editions:
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', e['date'])
        date.fromisoformat(e['date'])
        assert e['file'] == e['date'] + '.json'
        data = read_json(ROOT / 'quizzes' / e['file'])
        validate(data)
        texts = {q['question'].strip().casefold() for q in data['questions']}
        assert not seen.intersection(texts), 'Question repeated in another edition'
        seen.update(texts)
        archived = ROOT / 'quiz-archive' / (e['date'] + '.html')
        if archived.exists():
            match = re.search(r'<script id="quiz-data" type="application/json">(.*?)</script>', archived.read_text(encoding='utf-8'), re.S)
            assert match and json.loads(match[1]) == data, 'Archived questions cannot be silently changed'
        else:
            prepared[archived] = render(e, data, '../')
        if e == editions[-1]:
            prepared[ROOT / 'quiz.html'] = render(e, data)
    links = ''.join(f'<li><a href="quiz-archive/{e["date"]}.html"><span>{date.fromisoformat(e["date"]).strftime("%d %B %Y")} · {html.escape(e["label"])}</span><span aria-hidden="true">→</span></a></li>' for e in reversed(editions))
    prepared[ROOT / 'quiz-archive.html'] = shell('Past quizzes', f'<div class="eyebrow">THE QUIZ COLLECTION</div><h1>Keep exploring.</h1><p class="intro">Every edition has a home here. Revisit a favourite, try a missed week, or take the latest challenge.</p><p><a href="quiz.html">Take the latest quiz →</a></p><ul class="archive-list">{links}</ul>')
    # Prepare and validate every edition before replacing any published output.
    for path, content in prepared.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        stage = path.with_suffix(path.suffix + '.tmp')
        stage.write_text(content, encoding='utf-8')
        os.replace(stage, path)
    print(f'Validated {len(editions)} edition(s), {len(seen)} questions; wrote {len(prepared)} pages.')

if __name__ == '__main__':
    main()
