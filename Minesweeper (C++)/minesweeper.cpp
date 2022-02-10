// Implementation of the game "Minesweeper" in C++
// Programmed by Noah Kuperberg 2/9/2022

#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <ctime>

using namespace std;

// Class containing the board for minesweeper
class MSBoard {
    public:
        MSBoard(int rows, int cols, int bombs) {
            board = vector<vector<Tile>>(rows, vector<Tile>(cols));
            num_mines = bombs;

            // Randomly assign bombs (shuffle a range to ensure no repeats).
            srand(unsigned(time(0)));
            vector<int> locs(rows*cols);
            iota(locs.begin(), locs.end(), 0);
            random_shuffle(locs.begin(), locs.end());
            for (int i = 0; i < bombs; ++i){
                board[locs[i]/cols][locs[i]%cols].mine = true;
            } // for
            for (int row = 0; row < rows; ++row) {
                for (int col = 0; col < cols; ++col) {
                    if (row > 0) {
                        board[row][col].adjacent_tiles.push_back(&(board[row-1][col]));
                    } // north
                    if (row < (rows-1)) {
                        board[row][col].adjacent_tiles.push_back(&(board[row+1][col]));
                    } // south
                    if (col > 0) {
                        board[row][col].adjacent_tiles.push_back(&(board[row][col-1]));
                    } // west
                    if (col < cols-1) {
                        board[row][col].adjacent_tiles.push_back(&(board[row][col+1]));
                    } // east

                    if (row > 0 && col > 0) {
                        board[row][col].adjacent_tiles.push_back(&(board[row-1][col-1]));
                    } // northwest
                    if (row < (rows-1) && col < cols-1) {
                        board[row][col].adjacent_tiles.push_back(&(board[row+1][col+1]));
                    } // southeast
                    if (col > 0 && row < rows-1) {
                        board[row][col].adjacent_tiles.push_back(&(board[row+1][col-1]));
                    } // southwest
                    if (row > 0 && col < cols-1) {
                        board[row][col].adjacent_tiles.push_back(&(board[row-1][col+1]));
                    } // northeast
                   
                } // for col
            } // for row
        } // Constructor

        // flag determines whether a user has flagged that location.
        // mine indicates whethere there is a bomb at that location.
        // adj_mines is initialized at -1, but is updated when the user
        // selects that location to reflect how many mines are in the tiles 
        // adjacent to the one selected
        struct Tile {
            bool flag = 0;
            bool mine = 0;
            int adj_mines = -1;
            vector<Tile *> adjacent_tiles;
        }; // end Tile

        // Print out the board in its current state
        // '+' represents unclicked, 'F' represents a flag placed by the user
        // whereas an integer represents a revealed tile
        void print_board() {
            // To make sure spacing is even for double digits
            string padding = "    "; 
            // Print column numbers
            cout << "       ";
            for (size_t c = 0; c < board[0].size(); ++c){
                if (c > 9) {
                    padding = "   ";
                }
                cout << c << padding;
            }
            cout << "\n    ____";
            for (size_t c = 0; c < board[0].size() - 1; ++c){
                cout << "_____";
            }
            cout << "\n";
            padding = "   ";
            for (size_t r = 0; r < board.size(); ++r) {
                if (r > 9) {
                    padding = "  ";
                }
                cout << r << padding << "| ";
                for (size_t c = 0; c < board[0].size(); ++c) {
                    if (board[r][c].flag) {
                        cout << " F   ";
                    }
                    else if (board[r][c].adj_mines >= 0) {
                        cout << " " << board[r][c].adj_mines << "   ";
                    }
                    // exclusively for testing, uncomment to show mines
                    else if (board[r][c].mine && game_over){
                        cout << " M   ";
                    }
                    else {
                        cout << " +   ";
                    }
                }
                cout << "\n";
            }
            cout << "\n";
        }

        // Prompt the user to take an action, returns false if the user loses
        bool take_turn() {
            cout << "Flags remaining " << num_mines - num_flags << " out of "
            << num_mines << ".\n";
            cout << "Enter <row number> (SPACE) <column number> (SPACE)" <<
            " then 'F' to place or remove a flag at that location or 'R'" <<
            " to reveal that tile.\n";
            cout << "<row_num> <col_num> <F|R>: ";
            int row;
            int col;
            char action;
            cin >> row >> col >> action;
            // Catch invalid input without crashing.
            while(true){
                if (cin.fail()){
                    cin.clear();
                    cin.ignore();
                }
                else if (!(row < 0 || unsigned(row) >= board.size() 
                || col < 0 || unsigned(col) >= board[0].size() 
                || !(action == 'F' || action == 'R'))) {
                    break;
                }
                cout << "Invalid input. Usage:\n";
                cout << "<row_num> <col_num> <F|R>: ";
                cin >> row >> col >> action;
                
            }

            // Add or remove a flag.
            if (action == 'F') {
                if (board[row][col].adj_mines >= 0 && !(board[row][col].flag)){
                    cout << "This tile has been revealed." <<
                    " Are you sure you want to place a flag? (y/n): ";
                    char ans;
                    while (true) {
                        cin >> ans;
                        if (ans == 'y') {
                            break;
                        }
                        else if (ans == 'n') {
                            return true;
                        }
                        cout << "(y/n): ";
                    }
                }
                board[row][col].flag = !(board[row][col].flag);
                ++num_flags;
            }
            else {
                return reveal(row, col);
            }
            
            // If the user has used all their flags, 
            // return false and begin endgame
            return (num_mines-num_flags);
        }

        // Checks to see if the player has won.
        // Does nothing if the player has already hit a loss condition.
        void check_win(){
            if (game_over) {
                return;
            }
            for (size_t r = 0; r < board.size(); ++r) {
                for (size_t c = 0; c < board[0].size(); ++c) {
                    if (board[r][c].mine && !(board[r][c].flag)){
                        game_over = true;
                        print_board();
                        cout << "BOOM! Unflagged mine at row "
                        << r << ", col " << c << "\n"
                        << "GAME OVER\n";
                        return;
                    }
                }
            }
            print_board();
            cout << "YOU WIN!!!!!\n";
        }

    private:
        vector<vector<Tile>> board;
        int num_mines;
        int num_flags = 0;
        bool game_over = false; // set to true for testing.

        // Count how many tiles with mines are next to the revealed tile
        void count_adj(Tile * tile) {
            int sum = 0;
            for (auto it = tile->adjacent_tiles.begin(); 
            it != tile->adjacent_tiles.end(); ++it){
                if ((*it)->mine) {
                    ++sum;
                }
            }
            tile->adj_mines = sum;
            // If there are no bombs around the revealed tile,
            // reveal the empty tiles next to it as well.
            if (!sum){
                for (auto it = tile->adjacent_tiles.begin(); 
                it != tile->adjacent_tiles.end(); ++it){
                    if ((*it)->adj_mines < 0 && !((*it)->flag)) {
                        count_adj(*it);
                    }
                } 
            }
        }

        // Reveal the tile at (row, col).
        bool reveal(int row, int col) {
            if (board[row][col].flag) {
                cout << "This tile has a flag." <<
                " Are you sure you want to reveal it? (y/n): ";
                char ans;
                while (true) {
                    cin >> ans;
                    if (ans == 'y') {
                        board[row][col].flag = false;
                        break;
                    }
                    else if (ans == 'n') {
                        return true;
                    }
                    cout << "(y/n): ";
                }
            }
            if (board[row][col].mine) {
                game_over = true;
                print_board();
                cout << "BOOM! Mine at row " << row << ", col " << col << "\n";
                cout << "GAME OVER\n";
                return false;
            }
            count_adj(&board[row][col]);
            return true;
        }
};

// Main accepts one argument specifying difficulty
// easy: 9x9 board, 10 mines; medium: 16x16 board, 40 mines; 
// hard: 16x30 board, 99 mines.
int main(int argc, char*argv[]) {
    // Checks to see if there are the proper number of arguments
    if (argc != 2) {
        cerr << "Improper input. Usage: " << argv[0]  << " e|m|h\n" <<
        "e: easy (9x9 board, 10 mines).\n" <<
        "m: medium (16x16 board, 40 mines).\n" <<
        "h: hard (16x30 board, 99 mines).\n";
        
        exit(1);
    }
    
    char mode = argv[1][0];

    int rows;
    int cols;
    int bombs;
    switch (mode) {
        case 'e':
            cout << "Easy difficulty selected.\n";
            rows = 9;
            cols = 9;
            bombs = 10;
            break;

        case 'm':
            cout << "Medium difficulty selected.\n";
            rows = 16;
            cols = 16;
            bombs = 40;
            break;

        case 'h':
            cout << "Hard difficulty selected.\n";
            rows = 30;
            cols = 16;
            bombs = 99;
            break;
        
        default:
            cerr << "Improper input. Usage: " << argv[0]  << " e|m|h\n" <<
            "e: easy (9x9 board, 10 mines).\n" <<
            "m: medium (16x16 board, 40 mines).\n" <<
            "h: hard (30x16 board, 99 mines).\n";
            exit(1);
    } // switch

    MSBoard master(rows, cols, bombs);
    
    do {
        master.print_board();
    }
    while (master.take_turn());

    master.check_win();
    
} // end main()
