import pygame


def title(text, x, y, screen, color=(229, 217, 156)):
    font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 40)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    screen.blit(text, (x - text_rect.width // 2, y - text_rect.height // 2))



class Button:
    def __init__(self, text, x, y, width, height, img):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.img = pygame.transform.scale2x(pygame.image.load(f"assets/images/buttons/{img}.png"))
        self.rect.centerx = x
        self.rect.centery = y
        self.clicked = True
        self.click_sound = pygame.mixer.Sound("assets/sounds/effects/click.wav")

    def draw(self, screen, volume, scaled_mouse_pos):
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(scaled_mouse_pos):
            if mouse_pressed:
                if not self.clicked:
                    self.click_sound.set_volume(volume)
                    self.click_sound.play()
                    return self.normal_draw(True, screen)
                self.clicked = True
            else:
                self.clicked = False
            return self.hover_draw(screen)
        else:
            self.clicked = bool(mouse_pressed)
            return self.normal_draw(False, screen)


    def hover_draw(self, screen):
        draw_surf = pygame.transform.scale_by(self.img, 1.1)
        screen.blit(draw_surf, (self.rect.centerx - draw_surf.get_width() / 2, self.rect.centery - draw_surf.get_height() / 2))

        self.draw_text(screen)
        return False

    def normal_draw(self, pressed, screen):
        result = pressed
        screen.blit(self.img, (self.rect.x, self.rect.y))

        self.draw_text(screen)
        return(result)

    def draw_text(self, screen):
        font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 20)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect()
        screen.blit(
            text,
            (
                self.rect.centerx - text_rect.width // 2,
                self.rect.centery - text_rect.height // 2,
            ),
        )


class PromptBox:
    def __init__(self, message):
        self.rect = pygame.Rect(290, 110, 700, 500)
        self.message = message
        self.input = ""
        self.prompted = False
        self.text_box_rect = pygame.Rect(self.rect.x + 50, self.rect.y + 200, 600, 50)
        self.clicked_in = False

    def prompt(self):
        self.prompted = False
        self.input = ""

    def handle_input(self, event):
        if not self.prompted:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked_in = bool(self.text_box_rect.collidepoint(pygame.mouse.get_pos()))
            if self.clicked_in and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.prompted = True
                elif event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                elif event.key == pygame.K_SPACE:
                    self.input = f"{self.input} "
                else:
                    self.input += event.unicode

    def draw(self, screen):
        if self.prompted:
            return self.input
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        title(self.message, self.rect.centerx, self.rect.top + 50, screen)
        pygame.draw.rect(screen, (255, 255, 255), self.text_box_rect)
        text_rect = self.draw_text(screen, self.input, self.text_box_rect.left + 5, self.text_box_rect.top + 5)
        if self.clicked_in:
            if len(self.input) > 0:
                pygame.draw.rect(screen, (0, 0, 0), (text_rect.right + 5, text_rect.top, 5, 40))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (self.text_box_rect.left + 5, self.text_box_rect.top + 5, 5, 40))

    def draw_text(self, screen, text, x, y, center=False):
        font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 40)
        text = font.render(text, True, (0, 0, 0))
        if center:
            text_rect = text.get_rect()
            screen.blit(text, (x - text_rect.width / 2, y - text_rect.height / 2))
        else:
            screen.blit(text, (x, y))
            return pygame.Rect(x, y, text.get_rect().width, text.get_rect().height)


class Slider:
    def __init__(self, x, y, text, value, scale):
        self.rect = pygame.Rect(0, 0, 320, 50)
        self.rect.center = [x, y]
        self.text = text
        self.value = value
        self.scale = scale
        self.dial = pygame.Rect(0, 0, 25, 25)
        self.dial.center = [self.rect.left + 25 + (270 / self.scale * self.value), y]
        self.clicked = False

    def handle_input(self, scaled_mouse_pos):
        self.clicked = bool(pygame.mouse.get_pressed()[0] and self.dial.collidepoint(scaled_mouse_pos[0], scaled_mouse_pos[1]))
        if self.clicked:
            if scaled_mouse_pos[0] - self.rect.left <= 50:
                self.dial.centerx = max(scaled_mouse_pos[0], self.rect.left + 24)
            else:
                self.dial.centerx = min(scaled_mouse_pos[0], self.rect.right - 24)

    def draw(self, screen, scaled_mouse_pos):
        self.handle_input(scaled_mouse_pos)
        pygame.draw.rect(screen, (229, 217, 156), self.rect)
        scale = pygame.draw.line(screen, (30, 36, 74), (self.rect.left + 25, self.rect.centery), (self.rect.right - 25, self.rect.centery), 5)
        pygame.draw.circle(screen, (96, 153, 116), self.dial.center, self.dial.width / 2)
        self.value = int((self.dial.centerx - scale.x) / scale.width * self.scale)
        return self.value


class KeybindChanger:
    def __init__(self, x, y, text, value):
        self.rect = pygame.Rect(x, y, 1280, 50)
        self.rect.center = ((x, y))
        self.text = text
        self.value = value
        self.value_display = pygame.key.name(value)
        self.active = False

    def handle_input(self, event, scaled_mouse_pos):
        if self.rect.collidepoint(scaled_mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.active = True

        if self.active and event.type == pygame.KEYDOWN:
            self.value = event.key
            self.value_display = pygame.key.name(self.value)
            self.active = False
        return self.value

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (229, 217, 156), self.rect)
        else:
            pygame.draw.rect(screen, (214, 169, 126), self.rect)
        title(f"{self.text}      {self.value_display}", self.rect.centerx, self.rect.centery, screen)


class Popup:
    def __init__(self, text, x=608, y=480):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.draw_y = 720
        self.text = text
        self.img = pygame.image.load("assets/images/buttons/popup.png")
        self.pop = True

    def draw(self, screen):
        if self.pop:
            self.draw_y = min(self.draw_y + 5, self.rect.y)
        else:
            self.draw_y = max(self.draw_y - 5, 720)
        screen.blit(self.img, (self.rect.x, self.draw_y))
        title(self.text, self.rect.centerx, self.draw_y + 32, screen, color=(30, 36, 74))
