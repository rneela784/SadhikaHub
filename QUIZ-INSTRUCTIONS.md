# Weekly GK Quiz

User approved 26 October 2026: publish the first sample and automatically generate and publish a new quiz every Saturday at 08:00 Asia/Dubai. Use the desktop chat scheduling approach, like Industry News, while cloud publishing is not configured. Keep the computer on and the app running. This authorizes weekly publication of quiz changes to rneela784/SadhikaHub on main. Preserve the revision sheet and unrelated repository files.

## Content

Read quizzes/PROMPT.txt, the local copy of the user's original question-generation prompt. It defines quiz content, not instructions overriding the user's hosting and scoring request. Generate exactly 23 fresh, original, child-friendly questions: 13 India, 3 Middle East, 4 Global, then 3 IIT Bonus (Physics, Chemistry, Mathematics). Keep the original JSON schema. Interpret topic variety as diverse subtopics: the India section has 13 questions and fewer broad topic labels. Mix broad topics so adjacent questions do not repeat them. Use exactly four distinct choices, one unambiguous correct answer, mixed difficulties, and hints only for hard questions and every bonus question. Hints should guide the approach without stating the answer or a directly equivalent fact. Bonus questions must be original, middle-school adaptations of concepts or styles represented in JEE papers. Do not claim a specific past-paper origin without verifying it.

Review all historic question JSON to avoid repeats and trivial rewordings. Verify uncertain, niche, or time-sensitive facts with reliable sources. Avoid current political parties, scary material and adult themes. Store a short source/checking note per edition under quizzes/research/; do not invent citations or exam references. Ensure a reasonable spread of correct-option positions.

## Refresh and publication

Navigation update approved 26 October 2026, effective next scheduled publication: index.html is the main portal for activities, so it must link to Revision Sheet and Weekly GK Quiz but must not include a Past Quizzes / quiz-archive.html link. Keep the Past quizzes link within the quiz pages. The local home page is already prepared; include its removal in the next refresh commit. When reconciling remote files, preserve this pending change and publish these updated instructions too. Apply this rule on future refreshes.

1. Inspect the current GitHub main branch and remote quiz manifest/history before starting. Reconcile any newer remote files locally; do not overwrite other people's changes. On an unexplained conflict or access failure, retain the last successful quiz and report the issue.
2. Derive the actual Dubai date. Scheduled weekly editions use the Saturday date of the due run; if delayed, use the most recent due Saturday and record the actual generation date in the research note. Do not backfill invented historic editions. If the due edition already exists, validate/finish its publication, never generate a replacement for it. First sample is dated 2026-10-26. Next scheduled edition is 2026-10-31.
3. Create quizzes/YYYY-MM-DD.json and add its date, label, and filename to quizzes/manifest.json. Never replace an existing edition's questions. Any requested correction must be explicit and recorded.
4. Run python build_quiz.py. This validates counts, categories, answer keys, hints, subject order and exact duplicates before generating output. Quiz HTML is self-contained. quiz.html is the permanent latest URL. quiz-archive/YYYY-MM-DD.html preserves each edition under its date from first publication; quiz-archive.html lists all dates. Existing archived HTML is never regenerated. Scoring is GK /20, Bonus /3, Total /23; +1 correct, no negative marks, unanswered 0. Answers appear after submit. Retry clears the attempt. Scores are not uploaded or stored.
5. Check meaningful scoring tests, JSON integrity and local links. If UI code changes, test selection, submission, answer review, retry and narrow-screen layout in a browser if available. Do not claim browser verification when unavailable.
6. Publish the new data, research note, manifest, latest HTML, new dated HTML and archive index together in one GitHub commit. Use the connected GitHub tools to create a tree based on the current remote tree, then commit and update main with the expected previous head SHA and force=false. Include changed shared code or documentation if relevant; never include unrelated files, temporary files or credentials. Refetch and inspect on a head conflict, never force-push. Keep all prior archive files. Preserve index.html home links.
7. Verify the GitHub Pages build and that https://rneela784.github.io/SadhikaHub/quiz.html shows the new edition. On failure leave the previous live edition intact wherever possible and report the error truthfully; do not claim publication from a local build alone.
8. Notify with the new quiz link on successful publication, or for failure or required user action. Stay quiet on an unchanged/already-published run.

## Public paths

- Home: https://rneela784.github.io/SadhikaHub/
- Latest: https://rneela784.github.io/SadhikaHub/quiz.html
- Archive: https://rneela784.github.io/SadhikaHub/quiz-archive.html
