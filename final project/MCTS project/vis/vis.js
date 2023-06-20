var playerOne = document.getElementById('player-one');
var playerTwo = document.getElementById('player-two');
var board = document.getElementById('board');
var state = {
  board: [[]],
  finished: false,
  player: 1,
  gameId: '123'
};
var gameId;
var displayedBoard = [];

for (var i = 0; i < 7; i++) {
  displayedBoard[i] = [];
}

var cellSize = 36;

function render() {
  if (!gameId) {
    gameId = state.gameId;
  }
  if (state.gameId != gameId) {
    return;
  }
  if (state.player === 1) {
    playerOne.classList.add('turn');
    playerTwo.classList.remove('turn');
  } else if (state.player === 0) {
    playerOne.classList.add('turn');
    playerTwo.classList.remove('turn');
  }
  if (state.finished) {
    if (state.player === 1) {
      playerOne.classList.add('win');
      playerTwo.classList.add('lose');
    } else if (state.player === 0) {
      playerOne.classList.add('lose');
      playerTwo.classList.add('win');
    }
  }

  for (var col = 0; col < state.board.length; col++) {
    for (var row = 0; row < state.board[col].length; row++) {
      var newPiece = state.board[col][row];
      var oldPiece = displayedBoard[col][row];
      if (newPiece === oldPiece) {
        continue;
      }
      addPiece(col, row, newPiece);
      displayedBoard[col][row] = newPiece;
    }
  }
}

function addPiece(col, row, pieceType) {
  var x = col * cellSize;
  var y = (5 - row) * cellSize;
  var piece = document.createElement('div');
  piece.classList.add('piece');
  piece.classList.add('piece-' + pieceType);
  piece.style.transform = 'translateX(' + x + 'px) translateY(-50px)';
  board.appendChild(piece);
  setTimeout(function() {
    piece.style.transform = 'translateX(' + x + 'px) translateY(' + y + 'px)';
  }, 33);
}

setInterval(function() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'game-state.json', true);
  xhr.overrideMimeType('text/plain');
  xhr.onload = function() {
    var newState = JSON.parse(xhr.responseText);
    // Hacky deduplication
    if (JSON.stringify(state) === JSON.stringify(newState)) {
      return;
    }
    state = newState;
    render();
  };
  xhr.send();
}, 50);
