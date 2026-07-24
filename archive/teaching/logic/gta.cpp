#include <SFML/Graphics.hpp>
#include <vector>

// กำหนดขนาด block (tile)
const int TILE_SIZE = 40;
const int MAP_WIDTH = 15;
const int MAP_HEIGHT = 15;

// แผนที่ (0 = ทางเดิน, 1 = ตึก)
int map[MAP_HEIGHT][MAP_WIDTH] = {
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,0,0,0,0,0,0,1,0,0,0,0,0,0,1},
    {1,0,1,1,1,0,0,1,0,1,1,1,1,0,1},
    {1,0,1,0,1,0,0,1,0,1,0,0,1,0,1},
    {1,0,1,0,1,1,1,1,0,1,0,0,1,0,1},
    {1,0,0,0,0,0,0,0,0,1,1,1,1,0,1},
    {1,0,1,1,1,1,1,1,0,0,0,0,0,0,1},
    {1,0,0,0,0,0,0,1,1,1,1,1,1,0,1},
    {1,1,1,1,1,1,0,1,0,0,0,0,1,0,1},
    {1,0,0,0,0,1,0,1,0,1,1,0,1,0,1},
    {1,0,1,1,0,1,0,1,0,1,0,0,1,0,1},
    {1,0,0,1,0,1,0,0,0,1,0,1,1,0,1},
    {1,0,1,1,0,1,1,1,1,1,0,0,0,0,1},
    {1,0,0,0,0,0,0,0,0,0,0,1,1,0,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}
};

int main() {
    sf::RenderWindow window(sf::VideoMode(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE), "Mini GTA Clone");

    // ตัวละคร
    sf::RectangleShape player(sf::Vector2f(TILE_SIZE - 4, TILE_SIZE - 4));
    player.setFillColor(sf::Color::Green);
    sf::Vector2i playerGridPos(1, 1); // ตำแหน่งเริ่มต้นในแผนที่

    // กล่องตึก
    sf::RectangleShape wall(sf::Vector2f(TILE_SIZE, TILE_SIZE));
    wall.setFillColor(sf::Color(100, 100, 100));

    // กล่องพื้น
    sf::RectangleShape floor(sf::Vector2f(TILE_SIZE, TILE_SIZE));
    floor.setFillColor(sf::Color(30, 30, 30));

    // ความเร็ว
    float moveDelay = 0.1f;
    float moveTimer = 0;

    sf::Clock clock;

    while (window.isOpen()) {
        float dt = clock.restart().asSeconds();
        moveTimer += dt;

        sf::Event event;
        while (window.pollEvent(event))
            if (event.type == sf::Event::Closed)
                window.close();

        // การควบคุม (พร้อมตรวจชน)
        if (moveTimer > moveDelay) {
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up)) {
                sf::Vector2i next = playerGridPos + sf::Vector2i(0, -1);
                if (map[next.y][next.x] == 0) playerGridPos = next;
                moveTimer = 0;
            }
            else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) {
                sf::Vector2i next = playerGridPos + sf::Vector2i(0, 1);
                if (map[next.y][next.x] == 0) playerGridPos = next;
                moveTimer = 0;
            }
            else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left)) {
                sf::Vector2i next = playerGridPos + sf::Vector2i(-1, 0);
                if (map[next.y][next.x] == 0) playerGridPos = next;
                moveTimer = 0;
            }
            else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right)) {
                sf::Vector2i next = playerGridPos + sf::Vector2i(1, 0);
                if (map[next.y][next.x] == 0) playerGridPos = next;
                moveTimer = 0;
            }
        }

        // อัปเดตตำแหน่งผู้เล่นจริง
        player.setPosition(playerGridPos.x * TILE_SIZE + 2, playerGridPos.y * TILE_SIZE + 2);

        // วาดหน้าจอ
        window.clear();

        for (int y = 0; y < MAP_HEIGHT; ++y) {
            for (int x = 0; x < MAP_WIDTH; ++x) {
                if (map[y][x] == 1) {
                    wall.setPosition(x * TILE_SIZE, y * TILE_SIZE);
                    window.draw(wall);
                } else {
                    floor.setPosition(x * TILE_SIZE, y * TILE_SIZE);
                    window.draw(floor);
                }
            }
        }

        window.draw(player);
        window.display();
    }

    return 0;
}