/* Each dated page embeds this script so its behaviour stays with that edition. */
function scoreQuiz(questions, answers) {
  let gk = 0, bonus = 0, answered = 0;
  questions.forEach((q, i) => {
    if (Number.isInteger(answers[i]) && answers[i] >= 0 && answers[i] < 4) {
      answered++;
      if (q.options[answers[i]] === q.answer) q.category === 'IIT Bonus' ? bonus++ : gk++;
    }
  });
  return { gk, bonus, total: gk + bonus, answered };
}
if (typeof module !== 'undefined') module.exports = { scoreQuiz };
if (typeof document !== 'undefined') {
  const questions = JSON.parse(document.getElementById('quiz-data').textContent).questions;
  const form = document.getElementById('quiz-form');
  const results = document.getElementById('results');
  const progress = document.getElementById('progress');
  let submitted = false;
  const answers = () => questions.map((_, i) => {
    const selected = form.querySelector(`input[name="q${i}"]:checked`);
    return selected ? Number(selected.value) : null;
  });
  const updateProgress = () => {
    const count = scoreQuiz(questions, answers()).answered;
    progress.value = count;
    document.getElementById('progress-label').textContent = `${count} of 23 answered`;
    document.getElementById('remaining').textContent = count === 23 ? 'Ready when you are!' : `${23 - count} left to explore`;
    document.getElementById('submit-note').textContent = count === 23 ? 'All set! Submit to see your score and review the answers.' : `${23 - count} unanswered. You can still submit; unanswered questions earn 0 marks.`;
  };
  form.addEventListener('change', updateProgress);
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (submitted) return;
    submitted = true;
    const selected = answers();
    const score = scoreQuiz(questions, selected);
    document.getElementById('gk-score').textContent = `${score.gk}/20`;
    document.getElementById('bonus-score').textContent = `${score.bonus}/3`;
    document.getElementById('total-score').textContent = `${score.total}/23`;
    document.getElementById('result-message').textContent = score.total === 23 ? 'A full score — brilliant exploring! Try another edition next time.' : `Every question is a chance to learn. Review the answers below, then try again! ${23 - score.answered} unanswered.`;
    questions.forEach((q, i) => {
      const card = document.getElementById(`question-${i}`);
      const correct = q.options.indexOf(q.answer);
      card.querySelectorAll('input').forEach(input => {
        input.disabled = true;
        if (Number(input.value) === correct) input.closest('label').classList.add('correct');
        else if (input.checked) input.closest('label').classList.add('wrong');
      });
      const feedback = card.querySelector('.feedback');
      const ok = selected[i] === correct;
      feedback.className = `feedback ${ok ? 'good' : 'bad'}`;
      feedback.textContent = ok ? `Correct! +1 mark. ${q.answer}` : `${selected[i] === null ? 'Not answered.' : 'Not quite.'} Correct answer: ${q.answer}`;
      feedback.hidden = false;
    });
    document.getElementById('submit-button').disabled = true;
    results.hidden = false;
    results.focus();
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  document.getElementById('retry-button').addEventListener('click', () => {
    form.reset(); submitted = false;
    form.querySelectorAll('input').forEach(input => { input.disabled = false; });
    form.querySelectorAll('label').forEach(label => label.classList.remove('correct', 'wrong'));
    form.querySelectorAll('.feedback').forEach(el => { el.hidden = true; el.textContent = ''; });
    form.querySelectorAll('details').forEach(el => { el.open = false; });
    document.getElementById('submit-button').disabled = false;
    results.hidden = true;
    updateProgress();
    form.querySelector('input').focus();
  });
  updateProgress();
}
