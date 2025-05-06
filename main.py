import sys
import threading
import queue
import pygame
import math
from nlp_tasks import process_input
from text_to_speech import speak
import speech_to_text
import time

class VerticalOvalApp:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        pygame.font.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.display.set_caption("Voice Ganga")
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.oval_width = 50
        self.oval_height = 150
        self.oval_color = (255, 0, 0)
        self.background_color = (50, 50, 50)
        self.text_box_color = (80, 80, 80)
        self.response_box_color = (70, 70, 70)
        self.ripples = []
        self.is_speaking = False
        self.last_spoken_text = ""
        self.bot_response_text = ""
        self.last_ripple_time = 0
        self.add_ripple_interval = 500
        self.ripple_color = (255, 0, 0)
        self.title_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 24)
        self.spoken_text_font = pygame.font.Font(None, 24)
        self.response_text_font = pygame.font.Font(None, 24)
        self.text_color = (255, 255, 255)
        self.project_name = "VoiceGanga"
        self.team_name = "Made by Team KBM1"
        self.project_part = "Minor Project Part 2"
        self.response_line_length = 40

    def start_speaking_animation(self):
        print("Speaking started")
        self.is_speaking = True
        self.last_ripple_time = time.time()

    def stop_speaking_animation(self):
        print("Speaking stopped")
        self.is_speaking = False
        self.ripples = []
        self.last_spoken_text = ""

    def emit_oval_ripples(self):
        if self.is_speaking:
            for angle_deg in range(0, 360, 45):
                angle_rad = math.radians(angle_deg)
                x_offset = (self.oval_width / 2) * math.cos(angle_rad)
                y_offset = (self.oval_height / 2) * math.sin(angle_rad)
                start_x = int(self.center_x + x_offset)
                start_y = int(self.center_y + y_offset)
                initial_radius = 10
                initial_alpha = 200
                self.ripples.append([start_x, start_y, initial_radius, initial_alpha, self.ripple_color])

    def wrap_text(self, text, font, max_width):
        lines = []
        words = text.split(' ')
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] > max_width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line)
        return lines

    def update(self):
        self.screen.fill(self.background_color)

        title_surface = self.title_font.render(self.project_name, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.center_x, self.center_y - self.oval_height // 2 - 90))

        subtitle_surface = self.subtitle_font.render(self.team_name, True, self.text_color)
        subtitle_rect = subtitle_surface.get_rect(center=(self.center_x, self.center_y - self.oval_height // 2 - 55))

        project_part_surface = self.subtitle_font.render(self.project_part, True, self.text_color)
        project_part_rect = project_part_surface.get_rect(center=(self.center_x, self.center_y + self.oval_height // 2 + 60))

        spoken_text_surface = self.spoken_text_font.render(self.last_spoken_text, True, self.text_color)
        spoken_text_rect = spoken_text_surface.get_rect(center=(self.center_x, self.center_y + self.oval_height // 2 + 100))
        text_box_rect = spoken_text_rect.inflate(20, 10)

        response_lines = self.wrap_text(self.bot_response_text, self.response_text_font, self.screen_width - 40)
        response_surfaces = [self.response_text_font.render(line, True, self.text_color) for line in response_lines]
        response_rect = pygame.Rect(20, self.center_y + self.oval_height // 2 + 140, self.screen_width - 40, 0)
        current_y = response_rect.y
        for surface in response_surfaces:
            self.screen.blit(surface, (response_rect.x, current_y))
            current_y += surface.get_height()
        response_rect.height = current_y - response_rect.y
        response_box_rect = response_rect.inflate(20, 10)

        if self.is_speaking:
            pygame.draw.rect(self.screen, self.text_box_color, text_box_rect)
            self.screen.blit(spoken_text_surface, spoken_text_rect)

        pygame.draw.rect(self.screen, self.response_box_color, response_box_rect)
        for surface in response_surfaces:
            self.screen.blit(surface, (response_rect.x, response_rect.y + response_surfaces.index(surface) * surface.get_height()))

        self.screen.blit(title_surface, title_rect)
        self.screen.blit(subtitle_surface, subtitle_rect)
        self.screen.blit(project_part_surface, project_part_rect)

        rect_top = self.center_y - self.oval_height // 2 + (self.oval_width // 2)
        rect_height = self.oval_height - self.oval_width
        rect = pygame.Rect(
            self.center_x - self.oval_width // 2,
            rect_top,
            self.oval_width,
            rect_height
        )
        pygame.draw.rect(self.screen, self.oval_color, rect)

        top_triangle = [
            (self.center_x, self.center_y - self.oval_height // 2),
            (self.center_x - self.oval_width // 2, rect_top),
            (self.center_x + self.oval_width // 2, rect_top)
        ]
        pygame.draw.polygon(self.screen, self.oval_color, top_triangle)

        bottom_triangle = [
            (self.center_x, self.center_y + self.oval_height // 2),
            (self.center_x - self.oval_width // 2, rect_top + rect_height),
            (self.center_x + self.oval_width // 2, rect_top + rect_height)
        ]
        pygame.draw.polygon(self.screen, self.oval_color, bottom_triangle)

        new_ripples = []
        for ripple in self.ripples:
            x, y, r, alpha, color = ripple
            r += 3
            alpha -= 15

            if alpha > 0:
                ripple_color = (*color, int(alpha))
                pygame.draw.circle(self.screen, ripple_color, (int(x), int(y)), int(r), 2)
                new_ripples.append([x, y, r, alpha, color])

        self.ripples = new_ripples

        pygame.display.flip()

        if self.is_speaking and time.time() - self.last_ripple_time >= self.add_ripple_interval / 1000:
            self.emit_oval_ripples()
            self.last_ripple_time = time.time()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

def speech_recognition_worker(query_queue, stop_event, listen_event, app_instance):
    while not stop_event.is_set():
        listen_event.wait()
        try:
            user_query = speech_to_text.listen()
            if user_query:
                query_queue.put(user_query)
        except Exception as e:
            print(f"Error during speech recognition: {e}")

if __name__ == "__main__":
    screen_width = 700
    screen_height = 600
    app = VerticalOvalApp(screen_width, screen_height)

    query_queue = queue.Queue()
    stop_event = threading.Event()
    listen_event = threading.Event()
    listen_event.set()

    speech_thread = threading.Thread(
        target=speech_recognition_worker,
        args=(query_queue, stop_event, listen_event, app),
        daemon=True
    )
    speech_thread.start()

    running = True
    try:
        while running:
            app.update()
            running = not app.handle_events()

            if not query_queue.empty() and not app.is_speaking:
                user_query = query_queue.get()
                if user_query.lower() == "exit":
                    running = False
                    break

                app.start_speaking_animation()
                listen_event.clear()

                bot_response = process_input(user_query)
                print("Bot:", bot_response)
                app.bot_response_text = bot_response
                speak(bot_response)
                app.stop_speaking_animation()

                listen_event.set()

            time.sleep(0.01)

    except Exception as e:
        print(f"An error occurred in main loop: {e}")
        import traceback
        traceback.print_exc()
    finally:
        stop_event.set()
        speech_thread.join(timeout=2)
        pygame.quit()
        sys.exit()
