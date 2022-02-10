#include <iostream>
#include <vector>

using namespace std;

// Function that prints out the board
void printBoard(vector<vector<int>> board) {
    cout << "        " << board[1][0] << endl;
    for (int i = 6; i > 0; --i) {
        cout << i << "      " << board[0][i] << " " << board[1][7-i] << "      " << 7 - i <<  endl;
    }
    cout << "        " << board[0][0] << endl;
}

// Function that sums up a side of a board
int sumSide (vector<int> playerBoard) {
    int totalSum = 0;
    for (int i = 1; i < 7; ++i) {
        totalSum += playerBoard[i];
    }
    return totalSum;
}

void takeTurn (int holeNumber, vector<vector<int>> &board, int &turn) {
    while (board[turn][holeNumber] == 0 || holeNumber > 6 || holeNumber < 1) {
        cout << "Invalid input, please try again: ";
        cin >> holeNumber;
    }
    int stones = board[turn][holeNumber];
    int side = turn;
    board[turn][holeNumber] = 0;
    while (stones > 0) {
        --stones;
        --holeNumber;
        ++board[side][holeNumber];
        if (holeNumber == 0) {
            side = abs(side-1);
            holeNumber = 7;
            if (side == turn) {
                ++stones;
                --board[abs(side-1)][0];
            }
        }
    }
    
    if (holeNumber == 7 && sumSide(board[0]) != 0 && sumSide(board[1]) != 0) {
        int extraHole;
        printBoard(board);
        cout << "Extra turn! Input a new hole: ";
        cin >> extraHole;
        takeTurn(extraHole, board, turn);
    }
    
    else if (side == turn && board[side][holeNumber] == 1 && board[abs(side-1)][7-holeNumber] != 0) {
        cout << "Captured " << board[abs(side-1)][7-holeNumber] << " stones from hole " << 7 - holeNumber << endl;
        board[side][0] += board[abs(side-1)][7-holeNumber] + 1;
        board[side][holeNumber] = 0;
        board[abs(side-1)][7-holeNumber] = 0;
    }
}

void playGame (vector<vector<int>> &board, int &turn) {
    while (sumSide(board[0]) != 0 && sumSide(board[1]) != 0) {
        printBoard(board);
        cout << "Player " << turn + 1 << " take your turn: ";
        int holeNumber;
        cin >> holeNumber;
        takeTurn(holeNumber, board, turn);
        turn = abs(turn-1);
    }
}

int main() {
    // Initialize the board
    vector <int> playerBoard(7,4);
    playerBoard[0] = 0;
    vector<vector<int>> board;
    board.push_back(playerBoard);
    board.push_back(playerBoard);
    int turn = 0;
    
    playGame(board, turn);
    printBoard(board);

    if (sumSide(board[0]) == 0) {
        board[1][0] += sumSide(board[1]);
        for (int i = 6; i > 0; --i) {
            board[1][i] = 0;
        }
    }

    else if (sumSide(board[1]) == 0) {
        board[0][0] += sumSide(board[0]);
        for (int i = 6; i > 0; --i) {
            board[0][i] = 0;
        }
    }

    printBoard(board);
    if (board[0][0] > board[1][0]) {
        cout << "Player 1 wins!" << endl;
    }
    else if (board[1][0] > board[0][0]) {
        cout << "Player 2 wins!" << endl;
    }
    else {
        cout << "It's a draw." << endl;
    }
}