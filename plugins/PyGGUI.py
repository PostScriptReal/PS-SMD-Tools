import pygame

pygame.init()

class Root:

    def __init__(self, width=1280, height=720, name='PyGGUI', bg_color=(232, 232, 232), flags=64, icon=None, tickrate=60):
        """
        Note: flags value must be a valid pygame flag value!
        Default flag is pygame.SCALED which is 64
        Here is a list of other available flags and their values so you can set them properly:
        
        SCALED and FULLSCREEN = -2147483136
        FULLSCREEN = -2147483648
        RESIZABLE = 16
        SCALED and RESIZABLE = 528
        NOFRAME = 32
        HIDDEN = 128

        You can check the pygame docs to see what each flag does
        """
        
        pygame.display.set_caption(name)

        self.width = width
        self.height = height
        self.def_bg = bg_color

        self.tickrate = tickrate

        self.flags = flags

        self.mouse_objs = []

        self.font = pygame.font.Font(None, 24)

        self.game_window = pygame.display.set_mode((self.width, self.height), self.flags)
        self.clock = pygame.time.Clock()

        if not icon == None:
            winIcon = pygame.image.load(icon).convert()
            pygame.display.set_icon(winIcon)

        self.menuWin()
    
    def draw_menu(self):
        txt = "Plugin successfully executed :)"
        self.game_window.fill(self.def_bg)
        self.text = self.font.render(txt, True, (255, 255, 255))
        self.game_window.blit(self.text, (self.font.size(txt)[0] / 6 - 10, self.height / 2.25))

        pygame.display.update()
    
    def menuWin(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
            self.draw_menu()
            self.clock.tick(self.tickrate)