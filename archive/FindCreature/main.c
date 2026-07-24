#include <stdio.h>
#include <limits.h>

void findCreature(int guess, int deltas) {
    int row = guess / 10;
    int col = guess % 10;

    int d1 = deltas / 10;
    int d2 = deltas % 10;

    int minCell = INT_MAX;
    int maxCell = INT_MIN;

    int v[2] = { d1, d2 };
    int h[2] = { d2, d1 };

    for (int i = 0; i < 2; i++) {
        for (int vr = -1; vr <= 1; vr += 2) {
            for (int hc = -1; hc <= 1; hc += 2) {
                int r = row + vr * v[i];
                int c = col + hc * h[i];

                if (r >= 0 && r <= 9 && c >= 0 && c <= 9) {
                    int cell = r * 10 + c;
                    if (cell < minCell) minCell = cell;
                    if (cell > maxCell) maxCell = cell;
                }
            }
        }
    }

    printf("%d %d\n", minCell, maxCell);
}

int main() {
    int guess, deltas;
    scanf("%d %d", &guess, &deltas);
    findCreature(guess, deltas);
    return 0;
}