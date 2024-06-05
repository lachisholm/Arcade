# Import the Arcade library, necessary for game development
import arcade

# Constants for window dimensions and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer"

# Constants for player movement, gravity, and jump speed
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Main game class that inherits from Arcade's Window class
class MyGame(arcade.Window):
    """ Main application class for the platform game. """

    def __init__(self):
        # Initialize the game window with specified width, height, and title
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Initialize sprite lists for players, walls, and coins
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        # Initialize the player sprite
        self.player_sprite = None

        # Initialize the physics engine
        self.physics_engine = None

        # Initialize the score
        self.score = 0

        # Set the background color to Amazon green
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game, initialize variables, and create game sprites. """
        
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player sprite with an image and scale
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", 0.5)
        self.player_sprite.center_x = 50  # Initial x position
        self.player_sprite.center_y = 100  # Initial y position
        self.player_list.append(self.player_sprite)

        # Create the ground using a loop to place tiles
        for x in range(0, 1250, 64):  # Range and step determine where and how many tiles to place
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Create coins
        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)

        # Set up the physics engine with gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def on_draw(self):
        """ Render the game screen, called for each frame. """
        arcade.start_render()  # Start rendering
        self.wall_list.draw()  # Draw wall sprites
        self.player_list.draw()  # Draw player sprites
        self.coin_list.draw()  # Draw coin sprites

        # Draw the score on the screen
        arcade.draw_text(f"Score: {self.score}", 10, 10, arcade.color.WHITE, 18)

    def on_key_press(self, key, modifiers):
        """ Handle user keyboard input for movement and jumping. """
        if key == arcade.key.UP:
            # Check if the player can jump and then execute the jump
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            # Move left
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            # Move right
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called when the user releases a key, stopping horizontal movement. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Update game logic for movement and game state for each frame. """
        self.physics_engine.update()  # Update physics engine calculations

        # Check for collisions between player and coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        
        # Update the score and remove the collected coins
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

# Main execution point of the script
if __name__ == "__main__":
    window = MyGame()  # Create game window instance
    window.setup()  # Set up the game
    arcade.run()  # Start the game loop
