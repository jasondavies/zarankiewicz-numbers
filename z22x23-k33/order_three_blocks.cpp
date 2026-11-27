#include "order_three_blocks.hpp"

int main(int argc, char** argv) {
    Quotient board;
    if (!(cin >> board.g) || (board.g != 2 && board.g != 5)) return 2;
    if (argc == 2 && string(argv[1]) == "--lift") board.require_phases = true;
    else if (argc != 1) return 2;
    board.load(cin);
    if (!cin) return 2;
    bool possible = board.search(0, 0, board.capacity);
    cout << (possible ? "possible" : "excluded");
    if (possible && board.require_phases) {
        for (auto row : board.fixed_full) cout << ' ' << row;
        for (auto orbit : board.placed) for (auto row : orbit) cout << ' ' << row;
    }
    cout << '\n';
}
