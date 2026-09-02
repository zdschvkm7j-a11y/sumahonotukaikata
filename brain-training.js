(() => {
  const TOTAL_QUESTIONS = 10;
  const BEST_SCORE_KEY = 'smartphone-guide-brain-training-best-score';
  const difficultyDefinitions = {
    easy: {
      label: '簡単',
      createNumbers() {
        return { left: randomInteger(1, 9), right: randomInteger(1, 9) };
      },
    },
    normal: {
      label: 'ふつう',
      createNumbers() {
        return { left: randomInteger(1, 9), right: randomInteger(10, 99) };
      },
    },
    hard: {
      label: 'むずかしい',
      createNumbers() {
        return { left: randomInteger(10, 99), right: randomInteger(10, 99) };
      },
    },
  };

  const difficultyButtons = document.querySelectorAll('[data-difficulty]');
  const gameContainer = document.getElementById('game-container');
  const problemText = document.getElementById('problem-text');
  const score = document.getElementById('score');
  const levelDisplay = document.getElementById('level-display');
  const streakDisplay = document.getElementById('streak-display');
  const bestScoreDisplay = document.getElementById('best-score-display');
  const answerInput = document.getElementById('answer-input');
  const submitButton = document.getElementById('submit-btn');
  const quitButton = document.getElementById('quit-btn');
  const resultMessage = document.getElementById('result-message');

  if (!difficultyButtons.length || !gameContainer || !problemText || !score || !answerInput || !submitButton || !quitButton) {
    return;
  }

  const state = {
    difficulty: 'easy',
    score: 0,
    answeredQuestions: 0,
    streak: 0,
    bestScore: readBestScore(),
    currentAnswer: null,
    isPlaying: false,
  };

  function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function readBestScore() {
    try {
      const savedScore = Number(window.localStorage.getItem(BEST_SCORE_KEY));
      return Number.isInteger(savedScore) && savedScore >= 0 && savedScore <= TOTAL_QUESTIONS ? savedScore : 0;
    } catch (error) {
      return 0;
    }
  }

  function saveBestScore() {
    try {
      window.localStorage.setItem(BEST_SCORE_KEY, String(state.bestScore));
    } catch (error) {
      // Private browsing can disable localStorage without affecting the game.
    }
  }

  function updateScoreboard() {
    score.textContent = String(state.score);
    streakDisplay.textContent = `連続正解: ${state.streak}`;
    bestScoreDisplay.textContent = `最高記録: ${state.bestScore}`;
  }

  function setActiveDifficulty() {
    difficultyButtons.forEach((button) => {
      const isActive = button.dataset.difficulty === state.difficulty;
      button.classList.toggle('active', isActive);
      button.setAttribute('aria-pressed', String(isActive));
    });

    const definition = difficultyDefinitions[state.difficulty];
    if (definition && levelDisplay) {
      levelDisplay.textContent = `レベル: ${definition.label}`;
    }
  }

  function createQuestion() {
    const definition = difficultyDefinitions[state.difficulty];
    const numbers = definition.createNumbers();
    state.currentAnswer = numbers.left + numbers.right;
    problemText.textContent = `${state.answeredQuestions + 1}問目：${numbers.left} ＋ ${numbers.right} ＝ ?`;
    answerInput.value = '';
    answerInput.focus();
    updateScoreboard();
  }

  function startGame(difficulty) {
    if (!difficultyDefinitions[difficulty]) {
      return;
    }

    state.difficulty = difficulty;
    state.score = 0;
    state.answeredQuestions = 0;
    state.streak = 0;
    state.currentAnswer = null;
    state.isPlaying = true;
    gameContainer.style.display = 'block';
    resultMessage.textContent = '';
    submitButton.disabled = false;
    answerInput.disabled = false;
    setActiveDifficulty();
    createQuestion();
  }

  function finishGame() {
    state.isPlaying = false;
    state.currentAnswer = null;
    submitButton.disabled = true;
    answerInput.disabled = true;
    problemText.textContent = '10問できました！';
    resultMessage.textContent = `おわり！ ${state.score}問せいかいしました。`;

    if (state.score > state.bestScore) {
      state.bestScore = state.score;
      saveBestScore();
    }
    updateScoreboard();
  }

  function submitAnswer() {
    if (!state.isPlaying) {
      return;
    }

    const answerText = answerInput.value.trim();
    if (!answerText) {
      resultMessage.textContent = 'こたえを入力してください。';
      answerInput.focus();
      return;
    }

    const answer = Number(answerText);
    if (!Number.isFinite(answer) || answer !== state.currentAnswer) {
      state.streak = 0;
      resultMessage.textContent = 'ちがいます。もう一度考えてみよう。';
      updateScoreboard();
      answerInput.select();
      return;
    }

    state.score += 1;
    state.answeredQuestions += 1;
    state.streak += 1;
    resultMessage.textContent = 'せいかい！';
    updateScoreboard();

    if (state.answeredQuestions >= TOTAL_QUESTIONS) {
      finishGame();
      return;
    }

    createQuestion();
  }

  function quitGame() {
    state.isPlaying = false;
    state.currentAnswer = null;
    gameContainer.style.display = 'none';
    resultMessage.textContent = '';
    submitButton.disabled = false;
    answerInput.disabled = false;
  }

  difficultyButtons.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.difficulty === state.difficulty));
    button.addEventListener('click', () => startGame(button.dataset.difficulty));
  });

  submitButton.addEventListener('click', submitAnswer);
  quitButton.addEventListener('click', quitGame);
  answerInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      submitAnswer();
    }
  });

  setActiveDifficulty();
  updateScoreboard();
})();
